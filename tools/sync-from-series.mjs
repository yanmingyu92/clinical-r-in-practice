#!/usr/bin/env node
// Sync book chapters with freshly regenerated series content while preserving
// the book-only sections (## Exercises, ## Case study) that series-to-book.mjs
// does not generate.
//
// Usage:
//   node tools/sync-from-series.mjs --fresh <dir-of-fresh-book> [--book <book-dir>]
// Typical flow:
//   node <site>/scripts/series-to-book.mjs --series clinical-r-in-practice --out %TEMP%/clinical-r-book-fresh
//   node tools/sync-from-series.mjs --fresh %TEMP%/clinical-r-book-fresh
import { readFileSync, writeFileSync, readdirSync, existsSync, copyFileSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const bookDir = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const arg = (name) => {
	const i = process.argv.indexOf(`--${name}`);
	return i !== -1 && process.argv[i + 1] ? process.argv[i + 1] : undefined;
};
const freshDir = arg('fresh');
if (!freshDir || !existsSync(join(freshDir, 'chapters'))) {
	console.error('error: --fresh <dir> with a chapters/ subfolder is required');
	process.exit(1);
}

const MARKER = '\n## Exercises';
let synced = 0;
for (const f of readdirSync(join(bookDir, 'chapters')).filter(f => f.endsWith('.qmd'))) {
	const freshPath = join(freshDir, 'chapters', f);
	const bookPath = join(bookDir, 'chapters', f);
	if (!existsSync(freshPath)) { console.warn(`skip (no fresh counterpart): ${f}`); continue; }
	const current = readFileSync(bookPath, 'utf8');
	const cut = current.indexOf(MARKER);
	if (cut === -1) { console.warn(`skip (no "## Exercises" section): ${f}`); continue; }
	const fresh = readFileSync(freshPath, 'utf8').trimEnd();
	const tail = current.slice(cut).trimEnd();
	writeFileSync(bookPath, `${fresh}\n${tail}\n`, 'utf8');
	synced++;
}

// Front matter and project file track the series too; copy them over.
for (const f of ['preface.qmd', 'index.qmd', '_quarto.yml']) {
	const src = join(freshDir, f);
	if (existsSync(src)) copyFileSync(src, join(bookDir, f));
}
console.log(`synced ${synced} chapter(s) from ${freshDir}; preface/index/_quarto.yml refreshed`);
