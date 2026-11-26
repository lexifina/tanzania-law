"""Shared helpers for the Tanzania v2 build: paths, slugs, noon dates (Africa/Dar_es_Salaam), fast-import append."""
from __future__ import annotations

import datetime as dt
import hashlib
import re
import subprocess
import unicodedata
from pathlib import Path

W = Path(r'C:\Users\alany\Documents\tanzania-law-work')
REPO = W / 'repo'
CACHE = W / 'cache'
NOWIN = 0x08000000

# Chapter numbers of the Revised Laws (R.E. 2019/2023) for the acts already held as TanzLII consolidations.
CAPS = {
    'interpretation-of-laws': 1, 'evidence': 6, 'law-of-the-child': 13, 'penal-code': 16, 'legal-aid': 21,
    'law-of-marriage': 29, 'civil-aviation': 80, 'land': 113, 'village-land': 114, 'cotton-industry': 203,
    'ward-tribunals': 206, 'judiciary-administration': 237, 'community-service': 291, 'land-registration': 334,
    'law-of-contract': 345, 'statistics': 351, 'probate-administration-estates': 352, 'extradition': 368,
    'public-audit': 418, 'national-irrigation': 427, 'national-prosecutions-service': 430,
}


def fold(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c)).lower()


def slugify(s: str, n: int = 60) -> str:
    s = fold(s).replace('&', ' and ').replace("'", '').replace('\u2019', '')
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s[:n].rstrip('-') or 'act'


def act_slug(title: str) -> str:
    """'The Labour Laws (Amendments) Act, 2025 (No. 4 of 2025)' -> 'labour-laws-amendments-act'."""
    t = re.sub(r'\s*\((?:No|Na)\.?\s*\d+\s+(?:of|ya)\s+\d{4}\)\s*$', '', title.strip(), flags=re.I)
    t = re.sub(r'[,\s]*(?:of\s+|ya\s+(?:mwaka\s+)?)?(?:19|20)\d\d\.?\s*$', '', t, flags=re.I)
    t = re.sub(r'^(?:the|sheria\s+ya)\s+', lambda m: '' if m.group(0).lower().startswith('the') else m.group(0), t,
               flags=re.I)
    return slugify(t)


def noon(d: dt.date | str) -> str:
    """git raw date: noon in Dar es Salaam (UTC+3)."""
    if isinstance(d, str):
        d = dt.date.fromisoformat(d)
    t = dt.datetime(d.year, d.month, d.day, 9, 0, 0, tzinfo=dt.timezone.utc)
    # git cannot store dates before 1970: earlier days are clamped to 1 January 1970 (noon); the In-force trailer
    # carries the true day
    return f'{max(int(t.timestamp()), 32400)} +0300'


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git(*a, check=True) -> str:
    r = subprocess.run(['git', '-C', str(REPO), *a], capture_output=True, text=True, encoding='utf-8',
                       creationflags=NOWIN)
    if check and r.returncode:
        raise RuntimeError(f'git {a}: {r.stderr}')
    return r.stdout


class FastImport:
    """Append commits to refs/heads/main with one git fast-import process."""

    def __init__(self, parent: str, committer=('Lexifina', 'tanzania-law@lexifina.com')):
        self.p = subprocess.Popen(['git', '-C', str(REPO), 'fast-import', '--quiet', '--done'],
                                  stdin=subprocess.PIPE, creationflags=NOWIN)
        self.parent = parent
        self.committer = committer
        self.n = 0

    def _w(self, s):
        self.p.stdin.write(s if isinstance(s, bytes) else s.encode('utf-8'))

    def commit(self, author: tuple[str, str], date: str, message: str, files: dict[str, str | None]):
        self.n += 1
        self._w('commit refs/heads/main\n')
        self._w(f'mark :{self.n}\n')
        self._w(f'author {author[0]} <{author[1]}> {date}\n')
        self._w(f'committer {self.committer[0]} <{self.committer[1]}> {date}\n')
        b = message.encode('utf-8')
        self._w(f'data {len(b)}\n')
        self._w(b)
        self._w(b'\n')
        if self.n > 1:
            self._w(f'from :{self.n - 1}\n')
        elif self.parent:
            self._w(f'from {self.parent}\n')
        for path, text in files.items():
            if text is None:
                self._w(f'D {path}\n')
            else:
                b = text.encode('utf-8')
                self._w(f'M 100644 inline {path}\ndata {len(b)}\n')
                self._w(b)
                self._w(b'\n')
        self._w(b'\n')

    def close(self):
        self._w(b'done\n')
        self.p.stdin.close()
        if self.p.wait():
            raise RuntimeError('fast-import failed')
