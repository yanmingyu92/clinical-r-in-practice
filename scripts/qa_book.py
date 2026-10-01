#!/usr/bin/env python3
"""Structural QA for the Clinical R in Practice book.

Checks (stdlib only, no third-party deps):
  1. every file listed in _quarto.yml exists on disk
  2. every chapter keeps the book-only `## Exercises` section (sync marker)
  3. required site metadata is present and repo-url points at GitHub
  4. visual assets exist and book.css styles the era-callout component
  5. generated output (_book/, .quarto/) is git-ignored

Exit code 0 = all checks passed; 1 = at least one failure.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
failures = []
checks = 0


def check(ok, label):
    global checks
    checks += 1
    if not ok:
        failures.append(label)
    print(f"{'PASS' if ok else 'FAIL'}  {label}")


quarto = (ROOT / "_quarto.yml").read_text(encoding="utf-8")

# 1. every qmd referenced in _quarto.yml exists
listed = re.findall(r"-\s+(?:part:\s*)?([\w./-]+\.qmd)", quarto)
for rel in sorted(set(listed)):
    check((ROOT / rel).is_file(), f"listed file exists: {rel}")

# 2. chapters keep the ## Exercises marker used by tools/sync-from-series.mjs
chapters = sorted((ROOT / "chapters").glob("*.qmd"))
check(len(chapters) == 15, f"15 chapters present (found {len(chapters)})")
for ch in chapters:
    check("\n## Exercises" in ch.read_text(encoding="utf-8"),
          f"sync marker '## Exercises' present: {ch.name}")

# 3. required metadata
for key in ["site-url", "description", "cover-image", "favicon", "image",
            "page-footer", "open-graph", "twitter-card", "lang", "callout-icon"]:
    check(re.search(rf"^\s*{re.escape(key)}:", quarto, re.M),
          f"_quarto.yml sets {key}")
check(re.search(r'repo-url:\s*"?https://github\.com/yanmingyu92/clinical-r-in-practice"?', quarto),
      "repo-url points at the GitHub repository")

# 4. visual assets
for asset in ["assets/book.css", "assets/cover.svg", "assets/cover.png",
              "assets/favicon.svg"]:
    check((ROOT / asset).is_file(), f"asset exists: {asset}")
css = (ROOT / "assets/book.css").read_text(encoding="utf-8") \
    if (ROOT / "assets/book.css").is_file() else ""
check(".era-callout" in css, "book.css styles the .era-callout component")

# 5. generated output ignored
gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8") \
    if (ROOT / ".gitignore").is_file() else ""
check("_book/" in gitignore, ".gitignore covers _book/")
check(".quarto/" in gitignore, ".gitignore covers .quarto/")

print(f"\n{checks - len(failures)}/{checks} checks passed")
if failures:
    print("FAILURES:")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
