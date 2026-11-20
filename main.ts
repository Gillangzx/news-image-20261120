// main.ts — news-image-20261120 entry runner.
//
// The entry image is pre-rendered and committed as entry.png (Pillow,
// render.py in this repo). This script's only job is to deliver that exact
// committed file to the grader's output directory.
//
// Contract (grader): runs `node main.ts` with no network, a read-only repo
// directory, a writable output directory, 60 s. Output dir comes from
// $MAKEFUN_OUTPUT_DIR, falling back to /output.
//
// Fallback chain for the source file, in order:
//   1. entry.png next to this script (the committed file)
//   2. entry.png in the current working directory
//   3. entry.png in /bot (the mounted repo path used by the grader)
// If the direct copy fails, retry once via a read/write round-trip.
// The output is verified after the copy: it must exist, be non-empty, and
// start with the PNG magic bytes. Nothing is rendered here on purpose —
// rendering at grade time would risk a different image than the one that
// was reviewed and committed.
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

// __dirname exists when node loads this file as CommonJS; under ESM
// detection it is undefined, so fall back to the working directory.
const SCRIPT_DIR: string =
  typeof __dirname !== "undefined" ? __dirname : process.cwd();

const OUT_DIR: string = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const OUT_PATH: string = join(OUT_DIR, "entry.png");

function candidateSources(): string[] {
  const seen = new Set<string>();
  const list: string[] = [];
  for (const p of [
    join(SCRIPT_DIR, "entry.png"),
    join(process.cwd(), "entry.png"),
    join("/bot", "entry.png"),
  ]) {
    if (!seen.has(p)) {
      seen.add(p);
      list.push(p);
    }
  }
  return list;
}

function isValidPng(path: string): boolean {
  try {
    const st = statSync(path);
    if (st.size < 100) return false;
    const head = readFileSync(path).subarray(0, 8);
    return head.equals(PNG_MAGIC);
  } catch {
    return false;
  }
}

function main(): void {
  mkdirSync(OUT_DIR, { recursive: true });

  const sources = candidateSources();
  let used: string | null = null;
  let lastError: unknown = null;

  for (const src of sources) {
    if (!existsSync(src) || !isValidPng(src)) continue;
    try {
      copyFileSync(src, OUT_PATH);
      used = src;
      break;
    } catch (err) {
      lastError = err;
      // Fallback: read the bytes and write them out by hand.
      try {
        writeFileSync(OUT_PATH, readFileSync(src));
        used = src;
        break;
      } catch (err2) {
        lastError = err2;
      }
    }
  }

  if (used === null) {
    throw new Error(
      `entry.png not found or invalid in any candidate location (${sources.join(", ")}). ` +
        `Last error: ${lastError instanceof Error ? lastError.message : String(lastError)}`
    );
  }
  if (!isValidPng(OUT_PATH)) {
    throw new Error(`copied output at ${OUT_PATH} failed PNG validation`);
  }
  const bytes = statSync(OUT_PATH).size;
  console.log(`entry.png: copied ${bytes} bytes from ${used} to ${OUT_PATH}`);
}

main();
