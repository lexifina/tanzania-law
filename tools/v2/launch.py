"""Start a script detached: no console window, below-normal priority. Prints the PID (also written to <script>.pid)."""
import subprocess
import sys
from pathlib import Path

W = Path(r'C:\Users\alany\Documents\tanzania-law-work')
name = Path(sys.argv[1]).stem
p = subprocess.Popen([sys.executable, '-X', 'utf8'] + sys.argv[1:],
                     creationflags=0x08000000 | 0x00000008 | 0x00004000,
                     stdout=open(W / f'{name}.out', 'a'), stderr=subprocess.STDOUT, close_fds=True, cwd=str(W))
(W / f'{name}.pid').write_text(str(p.pid))
print(p.pid)
