"""One pure-rename commit: flat top-level folders -> acts/<year>/<NNN>-<slug>/ and revised-laws/cap-NNN-<slug>/."""
import re
import subprocess
import sys

sys.path.insert(0, __import__('os').path.dirname(__file__))
from common import CAPS, REPO, act_slug, git  # noqa: E402

moves = []
for d in sorted(p.name for p in REPO.iterdir() if p.is_dir() and p.name != '.git'):
    m = re.fullmatch(r'act-(\d{4})-(\d{3})', d)
    if m:
        head = (REPO / d / 'README.md').read_text('utf-8').splitlines()[0].lstrip('# ').strip()
        moves.append((d, f'acts/{m.group(1)}/{m.group(2)}-{act_slug(head)}'))
    elif d in CAPS:
        moves.append((d, f'revised-laws/cap-{CAPS[d]:03d}-{d}'))
for a, b in moves:
    (REPO / b).parent.mkdir(parents=True, exist_ok=True)
    git('mv', a, b)
    print(a, '->', b)
if '--commit' in sys.argv:
    env = dict(__import__('os').environ, GIT_AUTHOR_NAME='Lexifina', GIT_AUTHOR_EMAIL='tanzania-law@lexifina.com',
               GIT_COMMITTER_NAME='Lexifina', GIT_COMMITTER_EMAIL='tanzania-law@lexifina.com')
    subprocess.run(['git', '-C', str(REPO), 'commit', '-q', '-m',
                    'Layout: Acts of Parliament under acts/<year>/<number>-<short title>/, consolidated acts under '
                    'revised-laws/cap-<chapter>-<short title>/ (renames only, no text changed)'], env=env, check=True,
                   creationflags=0x08000000)
