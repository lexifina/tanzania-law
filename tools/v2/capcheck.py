"""Check the chapter numbers of the consolidated acts against the Acts of Parliament as passed in the repo
(Parliament of Tanzania copies): count every "<Act name> ... (Cap. N)" citation."""
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import CAPS, REPO  # noqa: E402

NAMES = {
    'interpretation-of-laws': 'Interpretation of Laws Act', 'evidence': 'Evidence Act',
    'law-of-the-child': 'Law of the Child Act', 'penal-code': 'Penal Code', 'legal-aid': 'Legal Aid Act',
    'law-of-marriage': 'Law of Marriage Act', 'civil-aviation': 'Civil Aviation Act', 'land': 'Land Act',
    'village-land': 'Village Land Act', 'cotton-industry': 'Cotton Industry Act', 'ward-tribunals': 'Ward Tribunals Act',
    'judiciary-administration': 'Judiciary Administration Act', 'community-service': 'Community Service Act',
    'land-registration': 'Land Registration Act', 'law-of-contract': 'Law of Contract Act',
    'statistics': 'Statistics Act', 'probate-administration-estates': 'Probate and Administration of Estates Act',
    'extradition': 'Extradition Act', 'public-audit': 'Public Audit Act', 'national-irrigation': 'National Irrigation Act',
    'national-prosecutions-service': 'National Prosecutions Service Act'}
text = subprocess.run(['git', '-C', str(REPO), 'grep', '-h', '-i', '-A2', '-E', '|'.join(re.escape(n) for n in NAMES.values()), 'main', '--', 'acts/', 'revised-laws/'],
                      capture_output=True, text=True, encoding='utf-8').stdout
text = re.sub(r'\s+', ' ', text)
out = {}
for slug, name in NAMES.items():
    # the name, not preceded by a longer name ("Village Land Act" for "Land Act"), then within 15 chars "Cap. N"
    pat = r'(?<!Village )(?<!Registration )\b' + re.escape(name) + r'[^.;:]{0,25}?\bCap(?:ter)?\.?\s*(\d{1,3})\b'
    c = Counter(int(m) for m in re.findall(pat, text, re.I))
    out[slug] = {'ours': CAPS[slug], 'found': c.most_common(4)}
    print(slug, CAPS[slug], c.most_common(4))
Path(r'C:\Users\alany\Documents\tanzania-law-work\capcheck.json').write_text(json.dumps(out, indent=1), 'utf-8')
