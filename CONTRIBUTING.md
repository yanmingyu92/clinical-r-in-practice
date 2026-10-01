# Contributing

Thank you for helping improve *Clinical R in Practice*. This repository has one
unusual rule that shapes every contribution: **chapter bodies are not edited
here**.

## Content corrections (chapter prose)

The text of `chapters/*.qmd` and `preface.qmd` originates from the *Clinical R
in Practice* series on [jaimeyan.com](https://jaimeyan.com) and is regenerated
by the site repository's `series-to-book.mjs`. Direct edits to chapter prose in
this repo will be overwritten by the next sync.

- **Typos, factual errors, outdated tool claims** → open an
  [issue](https://github.com/yanmingyu92/clinical-r-in-practice/issues) with
  the chapter and the offending passage; the fix lands in the series source and
  syncs into the book. Frontier chapters (12–15) carry a last-verified date —
  reports of stale claims there are especially welcome.
- **Book-only sections** (`## Exercises`, `## Case study`) live in this repo
  and survive syncs; PRs improving them are welcome.

## Book apparatus (this repo's own files)

PRs are welcome for the parts the book owns directly:

- `_quarto.yml`, `index.qmd`, `reading-guide.qmd`, `part-*.qmd`,
  `further-reading.qmd`, `acknowledgments.qmd` — layout, metadata, and
  front/back matter (never overwritten by syncs)
- `assets/` — theme, cover, favicon
- `tools/` — the sync tooling
- `.github/` — workflows and repository images

## Local checks

```bash
quarto render               # must complete without new warnings
python scripts/qa_book.py   # structural QA: chapters, assets, metadata
```

Pushing to `main` triggers the GitHub Actions render-and-deploy; generated
HTML (`_book/`) stays out of version control.

## Ground rules

- No patient data, ever. Examples use simulated data only.
- Keep the three-layer framing honest: mark volatile tool claims with a
  verification date.
- License: contributions are published under
  [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
