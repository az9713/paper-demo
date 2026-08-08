# paper-demo — agent-first design experiments in Paper

Two designs built end-to-end by a coding agent (Claude Code) driving [Paper](https://paper.design) through its local MCP server — no human clicks on the canvas.

The experiments follow the YC **Design Review** episode with Paper founder Stephen Haney and YC's Aaron Epstein: [*How to fix AI design slop*](https://www.youtube.com/watch?v=P06RgnUKX_I). The episode demos Paper's agent-native workflow and lists the biggest tells of AI-generated design (bold-everything typography, cards for everything, purple gradients, meaningless icon pills). Both designs here treat that list as hard rules; the transcript lives in `transcript.txt`.

## Design No. 1 — RegimeBot Landing

A landing page for a real market-regime trading bot. Maritime mood ("markets have weather"), Newsreader 300 display, exactly three font sizes, one orange moment, and a regime strip built from plain flex divs instead of a chart library.

- Live file: https://app.paper.design/file/01KZFQ0VWFCCX9Y39GDEJ7S0MQ
- Write-up: [`DEVELOPMENT-JOURNEY.md`](DEVELOPMENT-JOURNEY.md)
- Render: `regimebot-landing-paper-canvas.png` · standalone: `regimebot-landing.html`

## Design No. 2 — The Tactile Collection

A recreation of the feel of [Neenah's paper gallery](https://www.neenahpaper.com/paper/gallery): six specialty paper stocks on a swatch wall, with museum-style credits. No photographs — every texture (linen weave, metallic sheen, kraft speckle, felt stipple) is generated SVG: gradient rects plus multi-segment paths, hundreds of strokes packed into single Paper nodes.

- Live file: https://app.paper.design/file/01KZFRSRW9S9G8QY3EA8JSVDCF
- Write-up: [`DEVELOPMENT-JOURNEY-2.md`](DEVELOPMENT-JOURNEY-2.md)
- Render: `paper-texture-gallery-canvas.png`

## The `dev-journey` skill

The experience of writing these journey docs is distilled into a reusable Claude Code skill: [`skills/dev-journey/SKILL.md`](skills/dev-journey/SKILL.md). It defines the warts-and-all method — mine the live transcript before it is summarized away, quote the initial prompt verbatim, name the session's crux as its own section, and walk a completeness checklist that covers what nobody thinks to ask for: invisible constraints, near-misses, fragility and luck, costs and limits hit, human-in-the-loop moments, descoped work, and verification gaps. To install, copy the folder to `~/.claude/skills/dev-journey/`.

## Repo contents

| File | What it is |
|---|---|
| `DEVELOPMENT-JOURNEY.md` / `DEVELOPMENT-JOURNEY-2.md` | Full write-ups: design decisions, Paper MCP tools used, gotchas, fixes |
| `paper_mcp.py` | ~60-line JSON-RPC client for Paper's local MCP (`http://127.0.0.1:29979/mcp`) — session-header echo + SSE parsing |
| `regimebot-landing.html` | Design No. 1 as one self-contained HTML file |
| `*.png` / `*.jpg` | Canvas renders |
| `transcript.txt` | The YC Design Review episode transcript (design-rule source) |
| `HANDOFF.md` | Session resume point |
| `skills/dev-journey/` | Reusable Claude Code skill for writing docs like these |

## Hard-won facts about Paper's MCP

- The server runs only while Paper Desktop is open **with a file open**; every client process is a fresh session (`open_file` per batch).
- The HTML parser drops CSS `background-image`; SVG `<pattern>` fills render as nothing. Textures = SVG gradients + multi-segment stroked paths.
- Empty `<div>`s parse as childless Rectangles — create containers with a child inside.
- The free plan has a **weekly MCP call limit** (~two design sessions); design No. 2's footer died on it.
