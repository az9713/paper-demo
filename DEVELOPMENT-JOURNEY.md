# Development Journey — "RegimeBot Landing" in Paper

**Date:** 2026-08-07
**Deliverable:** https://app.paper.design/file/01KZFQ0VWFCCX9Y39GDEJ7S0MQ
**Tool:** Paper (paper.design), driven by its local MCP server
**Final render:** session scratchpad `shot_final.png` (1440px artboard, full page)

---

## 1. Discovery — what is Paper, and how does an agent use it?

1. I read `https://paper.design/llms.txt`. Paper renders **real HTML and CSS on a canvas** — no proprietary vector format. Agents read and write designs through MCP with no translation loss.
2. I read `https://paper.design/docs/mcp`. The MCP server is **local**: `http://127.0.0.1:29979/mcp`. The **Paper Desktop app** serves it, and only while the app runs with a file open.
3. I read the official plugin repo `paper-design/agent-plugins`. It confirmed the endpoint and added one rule: "Paper Desktop must be running with a file open."

**Dead end found early:** the Pencil app already on this PC is from **High Agency** (`app-update.yml` says `owner: highagency`). It is not Paper. I verified this before I built anything on the wrong surface.

## 2. Setup — install, launch, sign in

1. Paper Desktop was not installed. `https://paper.design/downloads` listed a Windows x64 NSIS build (v0.5.3).
2. I downloaded it and ran a silent install: `paper-setup.exe /S` → `%LOCALAPPDATA%\Programs\Paper\Paper.exe`.
3. On launch, the app opened a sign-in page (`login.paper.design`) in Chrome. Authentication is the user's job, and Simon completed it live — a "Verify your email address" mail from Paper landed in Yahoo Mail at 8:08 PM and the magic link finished the flow.
4. I polled port 29979 until `initialize` returned HTTP 200. Verification rule: probe the port, do not trust "the window is visible."

## 3. Plumbing — a 60-line MCP client instead of a registered server

Claude Code cannot register a new MCP server mid-session. Paper's MCP is plain HTTP, so I wrote `paper_mcp.py` (scratchpad) and spoke JSON-RPC directly:

- Capture the **`Mcp-Session-Id` response header** on `initialize`; echo it on every later POST. Without it, every call fails.
- Responses may arrive as **SSE** (`data:` lines), so the client parses both JSON and event-stream bodies.
- One Python process per batch of calls — Git Bash process spawns are slow on this machine, so batching matters.

## 4. Design decisions

**Inputs:** the YC Design Review transcript in this folder (`transcript.txt`), where Paper's founder Stephen Haney lists the tells of AI-generated design, plus Paper's own `get_guide` topic `paper-mcp-instructions` (17,795 chars of house style).

**Rules I committed to, from the video:**
- Pull font weights back — no bold; light display weights look "more designed."
- Maximum **three font sizes** (I used 68 / 17 / 13 px).
- No cards for everything, no purple, no gradients, no glows, no all-caps letter-spaced kickers, no meaningless numbers or icon pills.
- "A lot of design is deleting."

**Rules from Paper's guide:**
- Commit to a **mood word** before any hex value; derive every color from objects in that scene.
- Do not pick the first-instinct mood — it regresses to the predictable answer.
- One intense color moment beats five.
- Swiss editorial typography; information on surfaces, not boxed in cards.

**The brief that came out:**
- **Subject:** landing page for RegimeBot (Simon's shipped market-regime trading bot) — a real product, not lorem ipsum.
- **Mood candidates:** terminal/phosphor, vehicle dashboard, overcast, maritime, mineral.
- **Mood chosen:** *maritime*. First instinct for a trading bot is terminal-green; the sea-state metaphor (calm, swell, storm, fog) maps directly onto market regimes, so the visual centerpiece explains the product.
- **Palette (all from the maritime scene):** fog `#F3F5F6` ground · deep-water ink `#142A38` · weathered slate `#56707E` · deep navy `#0F3D5C` accent · buoy orange `#E05B2B`, used exactly once · chart tints `#CBD9E0` / `#8FA9B8` / `#E2E8EB`.
- **Type:** Newsreader 300 for display, Inter 400/500 for body and labels, IBM Plex Mono for dates and figures. Exactly three sizes: 68 / 17 / 13 px.
- **Direction:** Swiss-editorial nautical chart. One large light serif headline ("Markets have weather. Trade the season, not the storm."), hairline rules instead of cards, and one full-width **regime strip** as the single visual moment.

## 5. Implementation — Paper features used

| Paper MCP tool | What I used it for |
|---|---|
| `get_guide` | Loaded `paper-mcp-instructions` — mandatory review checkpoints and style rules |
| `list_files`, `create_file`, `open_file` | Created "RegimeBot Landing" in Simon's Team (free plan, first file) |
| `get_basic_info` | Confirmed empty file, page `1-0`, no tokens, no fonts |
| `get_font_family_info` | Verified Fraunces, Newsreader, Inter, Space Grotesk, IBM Plex Mono availability and weights before writing any typography (guide makes this mandatory) |
| `create_artboard` | 1440×900 artboard, flex column, fog background |
| `write_html` | Every visual group as its own call: nav, headline, sub+CTA, strip label row, strip container, 6 regime segments, "now" marker, 3 columns, proof line, footer — the user watches the canvas build in real time |
| `get_screenshot` | Review checkpoint after each phase (4 screenshots total) |
| `get_tree_summary` | Located exact node IDs when fixes were needed |
| `find_nodes` | Searched text nodes (learned: the filter is `textValue`, not `textContent`) |
| `update_styles` | Widened the headline to 1150px; set artboard `height: fit-content` |
| `set_text_content` | Fixed the wrapping Fog date (schema wants `textContent`) |
| `delete_nodes` | Removed a failed container (see gotcha below) |
| `finish_working_on_nodes` | Released the working indicator when done (guide: mandatory) |

**Layout system:** flex + padding + gap only. Paper forbids margins, CSS grid, and tables. Absolute positioning used once — the orange "now" tick anchored to the strip's right edge.

**The regime strip** is plain divs: six flex children with proportional `flex-grow` widths (duration) and varied bar heights (sea state), labels in fixed vertical lanes beneath, `align-items: flex-end` so bars sit on a shared baseline. No chart library, no image — it is editable Paper layers.

## 6. What went wrong, and the fixes

1. **Headline wrapped to three lines.** `max-width: 900px` was too narrow for line two. Screenshot caught it; `update_styles` → 1150px fixed it.
2. **Empty `<div>` became a Rectangle.** Paper parses a childless div as a Rectangle, and Rectangles cannot hold children — all six segment inserts failed with "cannot have children." Fix: delete the node, recreate the container **with its first child inside**, then append the rest.
3. **Fog date wrapped and broke the label lane.** "Jun 25 – Aug 25" did not fit a narrow segment. Fix: `set_text_content` → "Jun–Aug 25".
4. **Schema mismatches, three times.** `get_font_family_info` wants `familyNames` (array); `find_nodes` wants `textValue`; `update_styles` wants `updates:[{nodeIds:[…]}]`; `set_text_content` wants `textContent`. Rule learned: read the tool schema before the first call, not after the error.
5. **A nested styled span flattened.** The navy `−11.4%` inside the proof line lost its color on parse. Decision: leave it slate — orange already owns the page's single color moment, and a second accent would dilute it.
6. **Windows console encoding.** Tool output with `→` crashed `print` under cp1252. Fix: run Python with `-X utf8`.

## 7. Verification

Per the standing rule — verify by observing effects, never from a clean exit:

- Screenshot checkpoint after every phase, judged against Paper's checklist (spacing, typography, contrast, alignment, artboard fit, repetition).
- Final screenshot confirms: two-line headline, three font sizes, light weights, labels in lane, one orange moment, no cards, no clipping (`height: fit-content`).

## 8. Where things stand

- File: **RegimeBot Landing** — https://app.paper.design/file/01KZFQ0VWFCCX9Y39GDEJ7S0MQ (Simon's Team, free plan).
- Paper Desktop 0.5.3 installed and signed in; MCP reachable while the app runs with a file open.
- Reusable client: `paper_mcp.py` pattern, saved to project memory (`paper-desktop-mcp.md`).
- Standalone package: `regimebot-landing.html` in this folder — the same design as one self-contained HTML file (Google Fonts via CDN), verified pixel-faithful in Chrome.
- Possible next steps: export the artboard as image/PDF (`export`), pull the design into code with `get_jsx` (Tailwind or inline styles), or iterate by leaving comments in Paper and letting the agent resolve them.
