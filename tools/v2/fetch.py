"""Fetch the Tanzanian sources into tanzania-law-work/cache/<sha256(url)> (+ index.jsonl).

Hosts: polis.bunge.go.tz (Parliament Acts list + PDFs), www.osg.go.tz (Revised Laws R.E. 2023 chapters and Acts),
www.zanzibarassembly.go.tz (Zanzibar Acts). No stated rate limit on any: 3 in flight per host, ~1 s apart, back
off on 429/503 and stop the host after repeated refusals; 403 or a challenge page stops the host (never worked round).
"""
from __future__ import annotations

import json
import re
import ssl
import sys
import threading
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, __import__('os').path.dirname(__file__))
from common import CACHE, W, sha  # noqa: E402

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE   # several .go.tz hosts serve incomplete chains
LOCK = threading.RLock()
STOPPED: dict[str, str] = {}
LAST: dict[str, float] = {}
GAP = 1.0


def log(m):
    with LOCK, open(W / 'progress.log', 'a', encoding='utf-8') as f:
        f.write(time.strftime('%H:%M:%S ') + 'fetch: ' + m + '\n')


def path(url):
    return CACHE / sha(url.encode())


def get(url: str, referer: str | None = None) -> bytes | None:
    p = path(url)
    if p.exists():
        return p.read_bytes()
    host = urllib.parse.urlsplit(url).hostname
    if host in STOPPED:
        return None
    for attempt in range(5):
        with LOCK:
            wait = LAST.get(host, 0) + GAP - time.time()
            LAST[host] = max(time.time(), LAST.get(host, 0) + GAP)
        if wait > 0:
            time.sleep(wait)
        try:
            h = {'User-Agent': UA}
            if referer:
                h['Referer'] = referer
            sp = urllib.parse.urlsplit(url)
            q = sp._replace(path=urllib.parse.quote(urllib.parse.unquote(sp.path), safe='/')).geturl()
            r = urllib.request.urlopen(urllib.request.Request(q, headers=h), timeout=300, context=CTX)
            b = r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                log(f'{e.code} {host}: backing off ({attempt})')
                time.sleep(30 * (attempt + 1))
                continue
            if e.code == 403:
                STOPPED[host] = '403'
                log(f'STOP {host}: 403 on {url}')
                return None
            log(f'{e.code} {url}')
            return None
        except Exception as e:  # noqa: BLE001
            log(f'error {type(e).__name__} {url}: {str(e)[:100]}')
            time.sleep(5 * (attempt + 1))
            continue
        if b[:5] != b'%PDF-' and re.search(rb'cf-chl|challenge-platform|<title>\s*(?:Just a moment|Attention Required)|'
                                                rb'id="captcha|class="captcha', b[:20000], re.I):
            STOPPED[host] = 'challenge'
            log(f'STOP {host}: challenge page on {url}')
            return None
        CACHE.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix('.tmp')
        tmp.write_bytes(b)
        tmp.replace(p)
        with LOCK, open(CACHE / 'index.jsonl', 'a', encoding='utf-8') as f:
            f.write(json.dumps({'url': url, 'bytes': len(b), 'sha256': sha(b), 'at': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}) + '\n')
        return b
    STOPPED[host] = 'repeated 429/503'
    log(f'STOP {host}: repeated 429/503')
    return None


POLIS = 'https://polis.bunge.go.tz'


def polis_catalogue() -> list[dict]:
    b = get(POLIS + '/api/acts/async?draw=1&start=0&length=5000', 'https://www.parliament.go.tz/acts')
    return json.loads(b)['data'] if b else []


def polis_pdf(row) -> str:
    return POLIS + urllib.parse.quote(row['file_url'])


def osg_list() -> list[str]:
    out = []
    for pg in (1, 2, 3, 4):
        b = get(f'https://www.osg.go.tz/publications/acts?page={pg}')
        if not b:
            break
        for u in re.findall(r'href="(https://www\.osg\.go\.tz/uploads/documents/[^"]+\.pdf)"', b.decode('utf-8', 'replace')):
            if u not in out:
                out.append(u)
    for extra in ('https://www.osg.go.tz/publications/constitution',):
        b = get(extra)
        if b:
            for u in re.findall(r'href="(https://www\.osg\.go\.tz/uploads/documents/[^"]+\.pdf)"', b.decode('utf-8', 'replace')):
                if u not in out:
                    out.append(u)
    return out


ZNZ = 'https://www.zanzibarassembly.go.tz'


def znz_list() -> list[tuple[str, str]]:
    """[(year, pdf url)] from the House of Representatives' Acts index pages, every year it links."""
    years, seen, out = ['2026'], set(), []
    while years:
        y = years.pop()
        if y in seen:
            continue
        seen.add(y)
        b = get(f'{ZNZ}/en/acts.index/{y}')
        if not b:
            continue
        h = b.decode('utf-8', 'replace')
        years += [x for x in re.findall(r'acts\.index/(\d{4})', h) if x not in seen]
        for u in re.findall(r'href="(' + re.escape(ZNZ) + r'/storage/documents/acts/[^"]+\.pdf)"', h):
            if (y, u) not in out:
                out.append((y, u))
    return out


def main():
    log('start')
    rows = polis_catalogue()
    log(f'polis catalogue: {len(rows)} rows')
    osg = osg_list()
    log(f'osg: {len(osg)} pdfs')
    znz = znz_list()
    log(f'zanzibar: {len(znz)} pdfs')
    (W / 'lists.json').write_text(json.dumps({'osg': osg, 'znz': znz}, indent=1), 'utf-8')
    jobs = [u for u in osg] + [u for _, u in znz]
    rows = [r for r in rows if not r.get('deleted_at') and str(r.get('file_url', '')).lower().endswith('.pdf')]
    rows.sort(key=lambda r: -(int(r['posted']) if re.fullmatch(r'\d{4}', r['posted'] or '') else 0))
    jobs += [polis_pdf(r) for r in rows]
    todo = [u for u in jobs if not path(u).exists()]
    log(f'{len(jobs)} documents, {len(todo)} to fetch')
    n = [0, 0]

    def one(u):
        b = get(u)
        with LOCK:
            n[0] += 1
            n[1] += len(b or b'')
            if n[0] % 50 == 0:
                log(f'{n[0]}/{len(todo)} fetched, {n[1] >> 20} MB')

    with ThreadPoolExecutor(5) as ex:
        list(ex.map(one, todo))
    log(f'DONE {n[0]} fetched; stopped hosts: {STOPPED}')


if __name__ == '__main__':
    main()
