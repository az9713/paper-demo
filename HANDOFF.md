# HANDOFF — resume point for paper_YC (Paper design experiments)

**Read this first each new session.** No `CLAUDE.md` here. Git repo: https://github.com/az9713/paper-demo (this folder, branch `main`).

## Current state (as of 2026-08-07, session 2)
- **Done:** "The Tactile Collection" (Paper Texture Gallery) — Neenah-style swatch wall, six SVG-textured paper stocks.
  Live file: https://app.paper.design/file/01KZFRSRW9S9G8QY3EA8JSVDCF · write-up: `DEVELOPMENT-JOURNEY-2.md` · render: `paper-texture-gallery-canvas.png`.
- **BLOCKED until ~2026-08-14:** Paper free plan hit its WEEKLY MCP call limit. Mutating calls fail; the gallery footer never landed. Details in `DEVELOPMENT-JOURNEY-2.md` §6.
- **Done:** repo created and pushed via gh; `README.md` links both designs and the YC video.

## Prior state (session 1)
- **Done:** "RegimeBot Landing" designed in Paper (paper.design) and verified by screenshot.
  Live file: https://app.paper.design/file/01KZFQ0VWFCCX9Y39GDEJ7S0MQ (Simon's Team, free plan).
- **Done:** standalone package `regimebot-landing.html` — same design as one self-contained HTML file (Google Fonts CDN only), verified pixel-faithful in Chrome.
- **Done:** `DEVELOPMENT-JOURNEY.md` — full write-up: design decisions, Paper MCP tools used, gotchas, fixes.
- `regimebot-landing-paper-canvas.png` — final render of the Paper canvas.
- Paper Desktop 0.5.3 installed (`%LOCALAPPDATA%\Programs\Paper\Paper.exe`), signed in. Its MCP serves at `http://127.0.0.1:29979/mcp` only while the app runs with a file open.
- User-added inputs, not produced by the agent: `transcript.txt` (YC Design Review episode with Paper founder), `cc1_paper.txt`, `paper_my_first_design.jpg`.

## Next task
- **None pending — the request is complete.** If work resumes, likely follow-ups: export the artboard (`export` / `export_combined_pdf`), pull the design into a codebase via `get_jsx`, design more pages in the same file, or apply the transcript's anti-slop rules to another design. The user's ask takes precedence.

## How to reconnect to Paper (do not re-derive)
1. Start `%LOCALAPPDATA%\Programs\Paper\Paper.exe`; a file must be open.
2. Use `paper_mcp.py` (this folder): `python -X utf8 paper_mcp.py list | schema <tool> | call <tool> '<json>'`.
   It handles the `Mcp-Session-Id` echo and SSE parsing. If calls fail with a session error, delete the stale `paper_mcp.py.session` sidecar and retry.
3. Read `get_guide {topic:"paper-mcp-instructions"}` before designing; check fonts with `get_font_family_info {familyNames:[...]}`.
4. Gotchas (details in `DEVELOPMENT-JOURNEY.md` §6): empty `<div>` parses as a childless Rectangle; `update_styles` wants `updates:[{nodeIds:[...],styles:{...}}]`; `set_text_content` wants `textContent`; `find_nodes` wants `textValue`; finish with `finish_working_on_nodes`.

## Where to read things
- `DEVELOPMENT-JOURNEY.md` — the full story and tool table.
- Project memory `paper-desktop-mcp.md` (auto-loaded via MEMORY.md) — cross-session Paper setup facts.
- `transcript.txt` — the design rules source (3 font sizes, light weights, no cards/purple/gradients/pills).

## Session-transient scratch (already preserved)
- `paper_mcp.py` was built in the session scratchpad and is now committed to this folder — nothing else from the scratchpad is load-bearing (build1–4.py were one-shot canvas writers; the canvas itself is the durable record).
