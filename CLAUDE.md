# CLAUDE.md — Koi project brief

This file lets a fresh AI agent (Claude, Cursor, etc.) recreate the current state of the **Koi** project from a clean checkout. Read this first, then read `PLAN.md` for the publication roadmap.

## Base game (retail **Koi**)

**Koi** is a matching card game around XOR / parity matches. **Retail** play uses **six breeds** and a **32-card** deck (odd-sized subsets only: singles, triples, quints — no “all six” card). Baseline tableau **`L₀ = 8`**. Cards are sized as Magic-style (2.5" × 3.5"). Player-facing rules: `rules/RULES.md`. Breed roster: `koi_selection.md`. Glyph row: `design/glyphs/six_crests.svg`.

**Branding and production** target this **32-card** universe as the **default product**.

## Expansion (seven-species **Koi**, optional, documented only)

A **possible future expansion** (seven breeds including Kumonryu, **64** odd-weight cards including the **all-seven** card, **`L₀ = 10`**) lives under **`expansion/seven_koi/`** (`README.md` + `DECK_AND_RULES.md`). It is **not** the primary campaign narrative or boxed default.

The repository still contains **`GF(2)^7`** math, verification crates, and simulations for that slice; treat them as **expansion / legacy tooling**, not as instructions for the base SKU.

## Repo state (as of this writing)

- `README.md` — project name, tagline, link to [koi_selection.md](koi_selection.md).
- `.gitignore` — the standard GitHub Python template (suggests Python tooling is fine for math verification and any card-layout scripts).
- `ThirteenKoi.png` — reference grid of 13 popular koi varieties with English/Japanese names and one-line descriptions. The 13 varieties are: Kohaku, Showa, Asagi, Shusui, Ogon, Chagoi, Utsurimono, Tancho, Kumonryu, Hariwake, Sanke, Bekko, Utsuri. The **six** in the retail deck are locked in [koi_selection.md](koi_selection.md) (Phase 1 complete for publication).
- `PLAN.md` — 12-phase publication roadmap.
- `koi_selection.md` — Phase 1 deliverable: final **six breeds**, names, blurbs, primary-color palette.
- `rules/RULES.md` — player-facing rules (v0.2+); Phase 3 deliverable.
- `design/style_guide.md` — print, palette, **six segment crests** (glyph row), illustration tiers; Phase 4. `design/glyphs/six_crests.svg` — canonical **base game** crest row. `design/glyphs/seven_crests.svg` — **archival** seven-breed row (expansion reference; see `expansion/seven_koi/README.md`). `design/mocks/` — art direction mocks.
- `expansion/seven_koi/` — optional **Koi** expansion draft — seven species, 64-card deck, `L₀ = 10`, full seven breeds.
- `CLAUDE.md` — this file.
- `math/NOTES.md` — math claims with corrected status; includes **[CP24]** bibliography (Sidon sets / codes).
- `math/RESULTS.md` — Monte Carlo simulation report falsifying two of the original spec's claims.
- `math/verify.py` — Python verifier with sanity asserts and Mode A / Mode B Monte Carlo (`python3 math/verify.py --help`).
- `math/layout_stall_sweep.py` — Mode B stall rates vs layout size **`L`** across odd-weight decks (`n = 4`…`7`); see `math/RESULTS.md` §2.1.
- `math/explore_sidon_odd_restricted/` — Rust CLI for strict Sidon maxima on odd / even / ambient slices; **`cargo run --release -- --prove-odd-n 6`** exhaustively certifies **`s_max(O_6)=7`** on the **base** six-breed odd slice (`cd` there first). **`--prove-odd-n 7`** certifies **`s_max(O_7)=9`** on the seven-species **Koi** expansion’s seven-bit odd slice (`expansion/seven_koi/`).
- `math/weight3_no4dep/` — Rust exact search on the **35** weight-3 vectors in **GF(2)^7** (seven-species expansion deck geometry); `cargo run --release` after `cd` there.
- `math/weight5_no4dep/` — same question on all **21** weight-5 vectors in **GF(2)^7`; `cargo run --release` after `cd` there.
- `bonus_web/` — Rust → WebAssembly stub for the Kickstarter digital bonus (`wasm-pack` build). See [bonus_web/README.md](bonus_web/README.md).

## Game spec (base retail deck)

- **Total cards**: **32**, sized as Magic: The Gathering cards (2.5" x 3.5" / 63 x 88 mm).
- **6** single-koi cards: each of the six chosen koi featured prominently on one card with English name, Japanese name, and a large picture.
- **20** triple-koi cards = C(6, 3): every 3-koi combination, with the three koi swimming toward each other in roughly the shape of a Reuleaux triangle.
- **6** quintuple-koi cards = C(6, 5): every 5-koi combination, arranged in some interesting five-fold pattern.
- **No all-six card** — only **odd** subset sizes appear on cards (required for the XOR match structure).
- **Card count check**: 6 + 20 + 6 = 32. ✓

**Expansion deck (not default print):** the same combinatorics on seven species gives **`C(7,1)+C(7,3)+C(7,5)+C(7,7)=64`** cards; see `expansion/seven_koi/DECK_AND_RULES.md`. Math and simulations in `math/` still discuss this **`GF(2)^7`** slice explicitly.

## Rules (current working — base retail)

The designer's earliest spec overstated splitting the residual; details in `math/RESULTS.md` §4.

### Mechanics

1. **Prepare the deck.** Use all **32** cards.

2. **Shuffle.**

3. **Layout baseline and replenishment** — **`L₀ = 8`** = face-up count you restore toward **after each successful claim**, drawing from the deck until that count is reached or the deck empties (**partial replenish** OK). **No mid-game escalation:** whenever the tableau holds **`L₀`** face-up cards drawn only from this deck, a **legal 4-card match is guaranteed to exist** on the table (not merely in the deck). There is **no** rule to flip extra stock cards after a unanimous “no match” — if the group agrees nothing is visible, someone missed a match; keep scanning. On the six-bit odd universe, **`--prove-odd-n 6`** gives **`s_max(O_6) = 7`**, so **every** 8-card layout from the deck contains a 4-card XOR match. **`32 − L₀ = 24`** is divisible by **4**; **`|spread| < L₀`** can still occur after a scored match once facedown stock is depleted.

4. **Match:** four distinct cards XOR to **0** ↔ every depicted koi appears **0 / 2 / 4** times (minimum four cards holds on odd-only decks — `math/NOTES.md` §2).

5. **Claim:** shout **"Koi!"**, then touch **four distinct cards** in order. Invalid claim — caller is locked out until **another** player successfully claims **any** valid 4-card match.

6. **Endgame:** when replenishing hits an **empty** deck, put **every** remaining facedown card onto the tableau in **one sweep** (bulk reveal, not incremental dealing between claims) (**`|spread| < L₀`** is OK — **no facedown stubs** besides cards players already claimed). XOR conservation still matches Lemma E (`math/NOTES.md` §7.1); unnoticed legal matches can still lurk (`math/RESULTS.md` §3). Keep claiming while anyone spots a legal 4-card match. Once **everyone agrees** **no matches remain**, **end**.

7. **Score:** **fish / koi** = tally **every koi depiction** printed on cards **you claimed** (single = 1, triple = 3, quint = 5). Cards **left on the tableau** add **nothing** — they are effectively discarded for scoring.

8. **Tiebreakers** (see `rules/RULES.md` v0.2): most cards claimed, then most quintuple cards claimed, then deterministic fallback among singles.

### Glyph row (base game)

Templates use **six** horizontal segment crests (one per breed, left to right in bit order). Canonical art: `design/glyphs/six_crests.svg`. Seven-breed expansion reference: `expansion/seven_koi/README.md` + `design/glyphs/seven_crests.svg`.

## Math claims (status table)

**Published deck:** **six breeds**, **`|D| = 32`**, odd-weight vectors in **`GF(2)^6`** — exactly the sets of sizes 1, 3, and 5 drawn from the six labels. **`s_max(O_6)=7`** is certified in **`math/explore_sidon_odd_restricted`** (**`--prove-odd-n 6`**), so every **8-card** layout contains a 4-match at **`L₀ = 8`**.

The table below still lists the **seven-bit odd deck `D`** (`|D|=64`, seven-species **Koi** expansion geometry) because `math/NOTES.md` and Monte Carlo reports are written against it; the **six-breed base** column of the same tools proves the retail guarantee.

Detail in [math/NOTES.md](math/NOTES.md); empirical justification in [math/RESULTS.md](math/RESULTS.md). Two of the original spec's claims have been falsified by Monte Carlo simulation.

| Claim                                                                                | Status |
|--------------------------------------------------------------------------------------|--------|
| Published deck = 32 odd-weight vectors of **`F_2^6`** (sizes 1, 3, 5 only).          | Definition of retail product. |
| Deck = 64 odd-weight vectors of **`F_2^7`** (seven-species **Koi** expansion slice).          | Trivially true of that optional design (see `expansion/seven_koi/`). |
| Minimum match size = 4.                                                              | **Proven** (`math/NOTES.md` §2). |
| Match-finding reduces to a 4-cycle / Sidon condition.                                | **Proven** (`math/NOTES.md` §3-§4). |
| Maximum Sidon set in **`|D|=64`** (seven-species **Koi** expansion / seven-bit odd slice) = 9 (was previously claimed = 8). | **Proven** (Lemma D lower bound; **`s_max(O_7)=9`** certified, **`--prove-odd-n 7`**). |
| Any **10**-card layout from that **`D`** contains a 4-card match.                      | **Proven** from **`s_max(O_7)=9`**. |
| Any **8**-card layout from the **32-card** retail deck contains a 4-card match.    | **Proven** from **`s_max(O_6)=7`** (**`--prove-odd-n 6`**). **`L₀ = 8`**. |
| Σ R = 0 for the residual after the deck empties.                                     | **Proven** (`math/NOTES.md` §7.1). |
| The residual splits into two 4-card matches.                                       | **FALSE ~50% of the time.** Mode A: 51.7% unsplittable across 50k trials. Mode B at L=10 on legacy sims: 47.4% unsplittable among tested residuals. |

The cited classical bound `max Sidon in F_2^k = 2^⌊k/2⌋` is wrong for our setup. Authoritative Sidon/code bounds and constructions in vector spaces appear in Ingo Czerwinski & Alexander Pott, *Sidon sets, sum-free sets and linear codes*, **Advances in Mathematics of Communications** 18 (2024), no. 2, 549–566 ([DOI](https://doi.org/10.3934/amc.2023054), [arXiv](https://arxiv.org/abs/2304.07906)) — summarized as **[CP24]** in [math/NOTES.md](math/NOTES.md). The headline consequences flow into the Rules section above and `PLAN.md` Phases 0, 2, 3.

## Open decisions (must be resolved before later phases)

1. ~~**Publication route**~~ — **resolved**: **Kickstarter** (crowdfunding). Pre-launch, campaign, pledge manager, fulfillment — details in `PLAN.md` Phase 10.
2. ~~**Dealing / endgame**~~ — **resolved:** retail **`L₀ = 8`** on the **32-card** deck; **no** facedown flips on unanimous deadlock. When replenishment drains the pile, flip **every** remnant (**max tableau**). **Stop** when everyone agrees **no legal 4-match** remains. **Score** = tally **every fish / koi** on **cards you claimed** only.
3. ~~**Final koi selection (retail)**~~ — **resolved**: Kohaku, Karasu, Asagi, Ogon, Chagoi, Tancho — see [koi_selection.md](koi_selection.md). **Kumonryu** is **not** in the base box; it is reserved for the optional seven-species **Koi** expansion ([expansion/seven_koi/README.md](expansion/seven_koi/README.md)).
4. **Player count and turn structure** — turn structure **resolved: real-time call-out**. Call protocol: shout **"Koi!"** and then touch the four cards in order. Invalid-claim penalty: caller is locked out until another player claims a valid 4-card match. Player count still TBD (suggested 2–6); see `PLAN.md` Phase 3.
5. ~~**Art pipeline**~~ — **resolved**: **AI-generated**. Keep prompt logs, confirm commercial license, follow Phase 5 + Phase 8 (copyright / Kickstarter disclosure).
6. ~~**Digital bonus**~~ — **resolved**: **Rust** compiled to **WebAssembly** (`bonus_web/`) for in-browser play; Kickstarter stretch / add-on tier (align UI with **32-card** rules).

## Pointer

See `PLAN.md` for the full 12-phase publication roadmap and `ThirteenKoi.png` for the koi reference sheet.
