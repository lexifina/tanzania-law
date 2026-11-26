"""Every ~15 minutes: append what the fetcher has cached since the last pass (build.py) and push main fast-forward;
the first pass runs at once. Stops after the pass that follows the fetcher's DONE line. Log: progress.log"""
import os
import subprocess
import sys
import time
from pathlib import Path

H = Path(__file__).parent
sys.path.insert(0, str(H))
from common import NOWIN, REPO, W  # noqa: E402

os.environ.setdefault('GIT_SSH_COMMAND', 'C:/Windows/System32/OpenSSH/ssh.exe -o BatchMode=yes -o ServerAliveInterval=15 -o ServerAliveCountMax=4 '
                                         '-o ConnectTimeout=30')


def log(m):
    with open(W / 'progress.log', 'a', encoding='utf-8') as f:
        f.write(time.strftime('%H:%M:%S ') + 'runner: ' + m + '\n')


def run(*a):
    try:   # a stalled push or ls-remote must not hold the loop: give up after 15 minutes and retry next pass
        return subprocess.run(list(a), capture_output=True, text=True, encoding='utf-8', creationflags=NOWIN,
                              timeout=900)
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(a, 124, '', 'timed out')


def one():
    r = run(sys.executable, '-X', 'utf8', str(H / 'build.py'))
    log((r.stdout + r.stderr).strip().replace('\n', ' | ')[-400:])
    if (W / 'docs.flag').exists():
        d = run(sys.executable, '-X', 'utf8', str(H / 'docs.py'))
        log('docs: ' + (d.stdout + d.stderr).strip().replace('\n', ' | ')[-300:])
    p = run('git', '-C', str(REPO), 'push', 'origin', 'main')
    sha = run('git', '-C', str(REPO), 'ls-remote', 'origin', 'main').stdout.split()[:1]
    local = run('git', '-C', str(REPO), 'rev-parse', 'main').stdout.strip()
    log(f'push rc={p.returncode} remote main={sha} local={local[:12]} {p.stderr.strip()[-200:] if p.returncode else ""}')


def main():
    while True:
        marker = sys.argv[1] if len(sys.argv) > 1 else 'fetch: DONE'   # e.g. 'oag: DONE'
        done = marker in (W / 'progress.log').read_text(encoding='utf-8')
        if (W / 'STOP').exists():
            log('STOP file: exiting')
            return
        one()
        if done:
            log('finished')
            return
        time.sleep(900)


if __name__ == '__main__':
    main()
