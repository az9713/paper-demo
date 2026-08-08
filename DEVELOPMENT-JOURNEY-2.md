# Development Journey — "The Tactile Collection" in Paper (Design No. 2)

**Date:** 2026-08-07
**Deliverable:** https://app.paper.design/file/01KZFRSRW9S9G8QY3EA8JSVDCF ("Paper Texture Gallery")
**Brief:** "Create something like the designs in https://www.neenahpaper.com/paper/gallery" — Neenah's showcase of specialty paper stocks.
**Final render:** `paper-texture-gallery-canvas.png` (1440px artboard)

---

## 1. The brief — a gallery of paper, made of paper primitives

Neenah's gallery shows photographs: paper stocks in editorial compositions, each labeled with the product name, the finish (Linen, Felt, Plike, metallic), and credits for the designer and the printer. The layout is a masonry grid.

An agent in Paper has no photographs. That constraint set the whole project: every texture had to be **built from Paper's own primitives** — HTML frames, SVG shapes, and type. The design question became: how much tactility can flat vectors fake?

## 2. Cold start — reconnect without re-deriving

The first design session left a memory file (`paper-desktop-mcp.md`) and `paper_mcp.py`. This session started from zero anyway: app closed, port dead.

1. Probe `http://127.0.0.1:29979/mcp` → connection refused. Launch `%LOCALAPPDATA%\Programs\Paper\Paper.exe`, poll until `initialize` returns 200 (~12 s).
2. `get_basic_info` still said "Open a Paper file to use this tool" — the server runs when the app runs, but every tool needs an open file. `create_file` worked without one; `open_file` on the new ID unlocked the rest.
3. New lesson: **every Python process is a fresh MCP session.** The "sticky file" from `open_file` does not survive across script runs. Rule: call `open_file` (or pass `fileId`) at the top of every batch.

## 3. Design decisions

**Sources:** Paper's `get_guide` (`paper-mcp-instructions`, mandatory review checkpoints) plus the anti-slop rules from the YC Design Review transcript, carried over from design No. 1.

**The brief that came out:**

- **Mood candidates:** bookish, gallery, mineral, candlelit.
- **Mood chosen:** *bookish*. First instinct for a gallery is gallery-white; Paper's guide says the first-instinct mood regresses to the predictable answer. A swatch library lives among plaster, oak, and ink — the warm ground lets the paper colors carry the room.
- **Palette:** plaster `#F5F1E8` ground · ink `#1C1A17` · stone `#8B8578` muted labels. The six swatches supply all other color: linen white `#F2ECDE`, stardream silver `#C9CAD3`, bottle green `#20453A`, kraft `#C7B394`, epic black `#191613`, felt red `#A63A2B`.
- **Type:** Fraunces (variable, weight 340 display / 500 card names) — a serif with real print heritage, correct for a paper mill. Inter 500–600 at 11–12px letter-spaced caps for labels. Both verified with `get_font_family_info` before any typography (the guide makes this mandatory, and the check is two lines).
- **Layout:** a 1440px artboard, one oversized serif headline ("The Tactile Collection") with a small right-aligned intro — asymmetry over symmetry. The grid is **three flex columns**, middle column offset 64px down; masonry without CSS grid (Paper forbids grid). Swatch heights vary (320–460px) so the wall does not read as a spreadsheet.
- **Labels as museum wall text:** finish tag inside the swatch (bottom-left, small caps), name in Fraunces below, credits line "DESIGN: … · PRINT: …" — the exact information hierarchy of Neenah's gallery cards.
- **Content:** six real Neenah stocks (Classic Linen Natural White, Stardream Silver, Plike Bottle Green, Environment Desert Storm, Classic Crest Epic Black, Royal Sundance Warm Red) with fictional but plausible studio credits.

## 4. The texture problem — the core of this session

Three rendering approaches failed before one worked. The sequence matters because the failure evidence was misleading.

1. **CSS `background-image` gradients** (repeating-linear-gradient crosshatch for linen): parsed silently to nothing. `get_computed_styles` proved it — only `backgroundColor` survived. Paper's HTML parser **drops `background-image` entirely.**
2. **SVG `<pattern>` fill:** the `<rect fill="url(#linen)">` node was created but rendered invisible. Pattern defs are dead too.
3. **SVG `<linearGradient>` + stroked `<path>`:** the artboard screenshot still showed a flat swatch — but a **direct screenshot of the SVG node** showed the gradient and the lines rendering perfectly. The artboard shot was ~2 s stale. Wrong conclusion nearly drawn from a lagging screenshot; rule learned: **re-shoot before concluding something did not render.**

**The working recipe:** one inline `<svg>` per swatch — gradient-filled rect as the base, plus multi-segment `<path>` strokes for texture. A single path element holds hundreds of `M/L` segments and becomes **one** Paper node, so texture density costs nothing in layer count:

- **Linen:** ~260 horizontal + vertical hairlines at 3px pitch, two cream tones — reads as a weave.
- **Kraft / Felt:** seeded-random speckle, ~200–260 tiny strokes per tone (dark flecks + light flecks). `random.seed(n)` keeps reruns reproducible.
- **Stardream Silver:** four-stop diagonal gradient plus two wide-stroke sheen bands. (First pass was too literal — bright white ribbons; softened both strokes toward the base tones at review.)
- **Plike:** radial gradient vignette only — soft-touch coating is smooth, so restraint *is* the texture.
- **Epic Black:** near-black vertical gradient with 6px-pitch laid lines at 4% contrast.

The paths were generated in Python (f-strings building `d` attributes), not hand-written — the design lives in ~30 lines of generator code.

## 5. Paper features used

| Paper MCP tool | What it did this session |
|---|---|
| `create_file` / `open_file` | New file "Paper Texture Gallery"; `open_file` re-run per Python process (fresh session each time) |
| `get_guide` | Reloaded house style + mandatory review checkpoints |
| `get_font_family_info` | Verified Fraunces and Inter, weights 100–900, before any type styles |
| `create_artboard` | 1440px, flex column, plaster ground, 96px padding |
| `write_html` | One visual group per call: eyebrow, headline row, grid shell, then one card per call |
| `get_computed_styles` | Proved `background-image` was dropped (only `backgroundColor` survived) |
| `get_screenshot` | Review checkpoints; also the stale-screenshot lesson — direct node shots beat artboard shots for "did it render?" |
| `get_tree_summary` | Found the silver sheen path node IDs for the softening fix |
| `update_styles` | Artboard `height: fit-content`; swatch padding fix; silver stroke softening |
| `delete_nodes` | Removed the two failed texture attempts and the layout placeholder texts |
| `finish_working_on_nodes` | Released the working indicator (still worked after the rate limit hit) |

## 6. What went wrong, and the fixes

1. **`background-image` dropped by the parser.** Fix: inline SVG (see §4).
2. **SVG `<pattern>` fills render as nothing.** Fix: gradients + multi-segment paths.
3. **Stale screenshots.** Artboard shots lag writes by ~2 s; two shots in a row showed a texture "missing" that had rendered fine. Fix: sleep 2 s before shooting, and screenshot the specific node when verifying a specific change.
4. **An in-flow SVG squeezed its sibling label** into a one-character-per-line column. Fix: swatch frame gets `padding: 0`, SVG fills it in flow, label becomes `position: absolute; left: 20px; bottom: 20px`.
5. **Empty `<div>` = childless Rectangle** (repeat gotcha from design No. 1). The three masonry columns were created with throwaway 1px text children, deleted after the cards landed.
6. **The weekly MCP limit.** The second-to-last mutation — the footer — failed with *"Weekly MCP limit reached. It resets in 7 days. Upgrade to Paper Pro."* So the answer to "do I have enough credits" was discovered empirically: **Paper's free plan meters MCP calls weekly** (~two design sessions' worth). Design work by an external agent burns no Paper AI credits — the agent is the AI — but every MCP call counts against the cap. Read calls (screenshots, `finish_working_on_nodes`) still worked after the limit. The footer is the one casualty; the design stands without it.

## 7. Verification

- Screenshot checkpoint per phase, judged against Paper's checklist (spacing, typography, contrast, alignment, artboard fit, repetition).
- Card 1 verified at 2× zoom before replicating the pattern across five more cards — proving the texture recipe on one card first saved five rounds of rework when the first two recipes failed.
- Final artboard shot confirms: headline asymmetry, three balanced columns, six distinct textures, labels in lane, no clipping (`height: fit-content`).

## 8. Where things stand

- File: **Paper Texture Gallery** — https://app.paper.design/file/01KZFRSRW9S9G8QY3EA8JSVDCF (Simon's Team, free plan).
- **MCP is rate-limited until ~2026-08-14.** No further agent-driven edits this week without Paper Pro.
- New durable knowledge saved to project memory: the weekly limit, the texture recipe, the stale-screenshot rule.
- Possible next steps once the limit resets: add the missing footer, `export` the artboard as PNG/PDF, or rebuild the gallery as a standalone HTML file like `regimebot-landing.html`.
