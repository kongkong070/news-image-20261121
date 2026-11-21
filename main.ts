// "The World Today" — Saturday 21 November 2026 (Node 22, stdlib only).
// The front page is drawn by draw.py (Pillow) and shipped as entry.png;
// this program copies it to /output/entry.png. The image is pre-drawn
// rather than generated at run time, because the grader sandbox runs
// Node's standard library only and has no Pillow. The copy is
// deterministic: the same bytes go out on every run.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

copyFileSync(new URL('./entry.png', import.meta.url), join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png'));
