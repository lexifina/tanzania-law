"""Build Tanzania's corpus from the cache only.

    python -X utf8 scripts/tanzania-law/parse.py

- corpus.json: the TanzLII acts (acts.json), through the shared Peachjam adapter (scripts/africa-law/peachjam.py,
  read-only; a byte-identical copy is kept in this folder so the repository ships the exact adapter it was built with).
- corpus.d/10-constitution.json: the Constitution in English, from the official revised English version published
  by the Ministry of Constitutional and Legal Affairs (constitution.py); TanzLII has only the Kiswahili text.
Also writes verification.json (the checks) and repo/README.md, repo/LICENSE. Deterministic: same cache, same bytes.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARED = HERE.parent / "africa-law"
sys.path.insert(0, str(HERE))
if (SHARED / "peachjam.py").exists():
    sys.path.insert(0, str(SHARED))
import peachjam  # noqa: E402

peachjam.vendor(HERE)
corpus, report = peachjam.parse(HERE)
peachjam.write_corpus(HERE, corpus)
peachjam.write_docs(HERE, corpus)
(HERE / "verification.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8",
                                        newline="\n")
print(json.dumps(peachjam.summary(corpus, report), indent=1))
