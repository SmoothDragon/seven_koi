# Koi — seven-species expansion (optional)

This folder documents a **possible future expansion** for the base game **Koi** (six breeds, 32 cards — see the repository root [README.md](../../README.md)) — not the default retail SKU, Kickstarter core pledge, or primary rules path. Treat it as a **designer-facing draft** for an optional SKU, add-on, or stretch goal that could ship later if math, production, and playtesting all line up.

## What it adds relative to base **Koi**

| | Base **Koi** (retail) | Seven-species expansion (this folder) |
|---|------------------------|--------------------------------|
| Breeds | Six (see [koi_selection.md](../../koi_selection.md)) | **Seven** — the same six plus **Kumonryu** (九紋竜) as the seventh bit / badge |
| Deck | **32** cards — every **odd-sized** subset of six breeds **except** the all-six card | **64** cards — every **odd-sized** subset of **seven** breeds, **including** the **all-seven** card once |
| Baseline tableau `L₀` | **8** | **10** |
| “Omit one species” dealing | N/A (full six always) | **Not** required — the expansion assumes the **full seven** on every card type, same as the combinatorial deck |

**Match logic** is unchanged from the base game: a legal claim is **four distinct face-up cards** whose depicted breeds XOR-cancel (equivalently, every breed appears **0, 2, or 4** times across the four cards). Formal background: [math/NOTES.md](../../math/NOTES.md).

## Glyph row (seven breeds)

For artwork and layout, the **seven-segment** horizontal crest reference row is the archival sheet [design/glyphs/seven_crests.svg](../../design/glyphs/seven_crests.svg). Base-game print uses [design/glyphs/six_crests.svg](../../design/glyphs/six_crests.svg) only.

## Rules draft

Self-contained dealing, endgame, scoring (including the all-seven card and tiebreakers): [DECK_AND_RULES.md](DECK_AND_RULES.md).

## Math and simulations (legacy / seven-bit slice)

The repository’s **`GF(2)^7`** odd-weight deck geometry powers certificates and Monte Carlo paths that are **not** part of the published six-breed product narrative, but they remain **accurate tools** for this expansion concept:

- **Exhaustive Sidon certificate on the seven-breed odd slice:** `math/explore_sidon_odd_restricted` — `cargo run --release -- --prove-odd-n 7` certifies **`s_max(O_7) = 9`**, so every **10-card** layout from the legal **64-card** deck contains a **4-card** XOR match (hence **`L₀ = 10`** in the draft rules).
- **Write-ups and empirical tables:** [math/NOTES.md](../../math/NOTES.md), [math/RESULTS.md](../../math/RESULTS.md) (including residual splittability — do **not** assume the endgame residual partitions into two clean four-card matches).

## Relationship to the base repo

- **Base game** rules for the **32-card** deck: [rules/RULES.md](../../rules/RULES.md).
- **Project brief** (base vs expansion pointers): [CLAUDE.md](../../CLAUDE.md).
