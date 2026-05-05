# CLAUDE.md — Seven Koi project brief

This file lets a fresh AI agent (Claude, Cursor, etc.) recreate the current state of the Seven Koi project from a clean checkout. Read this first, then read `PLAN.md` for the publication roadmap.

## Project

**Seven Koi** is a matching card game around XOR / parity matches. **Standard** play uses **six** listed koi (one of the seven omitted everywhere) and **32** cards; **Expert** play uses all **seven** koi and **64** cards. A single print run can carry both tiers on shared artwork with a mechanical way to partition (see Open decisions). Cards are sized as Magic-style (2.5" × 3.5").

## Repo state (as of this writing)

- `README.md` — project name, tagline, link to [koi_selection.md](koi_selection.md).
- `.gitignore` — the standard GitHub Python template (suggests Python tooling is fine for math verification and any card-layout scripts).
- `ThirteenKoi.png` — reference grid of 13 popular koi varieties with English/Japanese names and one-line descriptions. The 13 varieties are: Kohaku, Showa, Asagi, Shusui, Ogon, Chagoi, Utsurimono, Tancho, Kumonryu, Hariwake, Sanke, Bekko, Utsuri. The seven in play are locked in [koi_selection.md](koi_selection.md) (Phase 1 complete).
- `PLAN.md` — 12-phase publication roadmap.
- `koi_selection.md` — Phase 1 deliverable: final seven koi, names, blurbs, primary-color palette.
- `rules/RULES.md` — player-facing rules (v0.1+); Phase 3 deliverable.
- `design/style_guide.md` — print, palette, **seven segment crests** (glyph row), illustration tiers; Phase 4. `design/glyphs/seven_crests.svg` — canonical crest row reference. `design/mocks/` — art direction mocks.
- `CLAUDE.md` — this file.
- `math/NOTES.md` — math claims with corrected status; includes **[CP24]** bibliography (Sidon sets / codes).
- `math/RESULTS.md` — Monte Carlo simulation report falsifying two of the original spec's claims.
- `math/verify.py` — Python verifier with sanity asserts and Mode A / Mode B Monte Carlo (`python3 math/verify.py --help`).
- `math/layout_stall_sweep.py` — Mode B stall rates vs layout size **`L`** across odd-weight decks (`n = 4`…`7`); see `math/RESULTS.md` §2.1.
- `math/explore_sidon_odd_restricted/` — Rust CLI for strict Sidon maxima on odd / even / ambient slices; **`cargo run --release -- --prove-odd-n 7`** (resp. **`6`**) exhaustively certifies **`s_max(O_7)=9`** on the Expert (64-card) slice and **`s_max(O_6)=7`** on the Standard six-koi odd slice (`cd` there first).
- `math/weight3_no4dep/` — Rust exact search: max subset of the **35** weight-3 vectors in **GF(2)^7** with **no linearly dependent 4-set** (answer **9**); `cargo run --release` after `cd` there.
- `math/weight5_no4dep/` — same question on all **21** weight-5 vectors (answer **9**); `cargo run --release` after `cd` there.
- `bonus_web/` — Rust → WebAssembly stub for the Kickstarter digital bonus (`wasm-pack` build). See [bonus_web/README.md](bonus_web/README.md).

## Game spec (verbatim from designer)

- **Total cards**: 64, sized as Magic: The Gathering cards (2.5" x 3.5" / 63 x 88 mm).
- **7 single-koi cards**: each of the 7 chosen koi featured prominently on one card with English name, Japanese name, and a large picture.
- **35 triple-koi cards** = C(7, 3): every 3-koi combination, with the three koi swimming toward each other in roughly the shape of a Reuleaux triangle.
- **21 quintuple-koi cards** = C(7, 5): every 5-koi combination, arranged in some interesting five-fold pattern.
- **1 all-seven card**: all 7 koi together.
- **Card count check**: 7 + 35 + 21 + 1 = 64. ✓

- **Standard (six-koi) variant**: 32-card subdeck = odd-weight subsets of **six** koi once one canonical koi has been omitted (see Open decisions): C(6,1) + C(6,3) + C(6,5) = 32. Same card size.

## Rules (current working — Standard + Expert)

The designer's earliest spec overstated splitting the residual; details in `math/RESULTS.md` §4.

**Choose a version before setup.** Same turn structure for both unless noted.

### Shared mechanics

1. **Prepare the deck.** Use only cards legal for that version (32 Standard / 64 Expert)—see Open decisions about physically splitting a single print run.

2. **Shuffle.**

3. **Layout baseline and replenishment (version-specific)** — **`L₀`** = face-up count you restore toward **after each successful claim**, drawing from the deck until that count is reached or the deck empties (**partial replenish** OK). **No mid-game escalation:** whenever the tableau holds **`L₀`** face-up cards drawn only from that version’s deck, a **legal 4-card match is guaranteed to exist** on the table (not merely in the deck). So there is **no** rule to flip extra stock cards after a unanimous “no match” — if the group agrees nothing is visible, someone missed a match; keep scanning. Replenishment after claims may still draw **multiple** cards in one refresh to refill toward **`L₀`**.
   - **Standard (`|D| = 32`, six active koi).** **`L₀ = 8`**. Lay out eight cards initially. On the six-bit odd universe, **`--prove-odd-n 6`** gives **`s_max(O_6) = 7`**, so **every** 8-card layout from the Standard deck contains a 4-card XOR match. Mode B simulation (`math/layout_stall_sweep.py`, **`math/RESULTS.md`**) previously motivated **`L₀ = 8`** vs smaller **`L`**. Replenish toward **eight** when the deck has stock. (**`32 − L₀ = 24`** is divisible by **4**; **`|spread| < L₀`** still occurs after a scored match once facedown stock is depleted—same endgame mechanic as Expert.) **No** stock flips on deadlock.
   - **Expert (`|D| = 64`, seven active koi).** **`L₀ = 10`**. Lay out ten cards initially. Exhaustive strict-Sidon search on **`O_7 ⊂ GF(2)^7`** (`math/explore_sidon_odd_restricted`, **`--prove-odd-n 7`**) certifies **`s_max(O_7) = 9`**, so **every** 10-card subset of the Expert deck **`D`** contains a 4-card XOR match (`math/NOTES.md` §6 Corollary). Larger ambient **`GF(2)^7`** guarantees (**`|L| ≥ 13`**, **[CP24]**) are stronger than needed for published play. After any claim, remove the scored four cards, then replenish from the deck toward **`L₀`** again. **No** stock flips on deadlock.

4. **Match:** four distinct active cards XOR to **0** ↔ every depicted koi appears **0 / 2 / 4** times (minimum four cards holds on odd-only decks — `math/NOTES.md` §2).

5. **Claim:** shout **"Koi!"**, then touch **four distinct cards** in order. Invalid claim — caller is locked out until **another** player successfully claims **any** valid 4-card match.

6. **Endgame:** when replenishing hits an **empty** deck, put **every** remaining facedown card onto the tableau in **one sweep** (bulk reveal, not incremental dealing between claims) (**`|spread| < L₀`** is OK — **no facedown stubs** besides cards players already claimed). XOR conservation still matches Lemma E (**`math/NOTES.md` §7.1**); unnoticed legal matches can still lurk (**`math/RESULTS.md` §3**). Keep claiming while anyone spots a legal 4-card match. Once **everyone agrees** **no matches remain**, **end**.
7. **Score:** **fish / koi** = tally **every koi depiction** printed on cards **you claimed** (single = 1, triple = 3, quint = 5, all-koi = 6 Standard / 7 Expert). Cards **left on the tableau** add **nothing** — they are effectively discarded for scoring.

8. **Tiebreakers** (still apply when totals tie): most cards claimed, then most **all-koi** cards (`|K|=6` / `|K|=7`), then **highest-weight single card among active species**.

### Standard — six koi

- **`|D| = 32`:** fix one omitted koi; keep only cards that **never** depict that species. Equivalently, all odd-cardinality subsets drawn from the other six (`C(6,1)+C(6,3)+C(6,5)=32`).
- Glyph row on templates uses **six** filled segment crests plus one **muted** slot for the dormant species—or omit that column entirely once the omission is finalized.
- Graphic production still needs an **inventory split aid** so players can sort a unified print run quickly (corner **dot / icon / color nib** proposals live in Open decisions).

### Expert — seven koi

- **`|D| = 64`:** all odd-weight bit vectors over the seven chosen koi (`C(7,1) + C(7,3) + C(7,5) + C(7,7)`).

## Math claims (status table)

Applies **as written** to the **Expert (seven-koi, 64-card) deck `D`**. The **Standard (six-koi, 32-card) deck** inherits the XOR / parity lemmas on its own affine slice; **`s_max(O_6)=7`** is certified in **`math/explore_sidon_odd_restricted`** (**`--prove-odd-n 6`**), so every **8-card** layout from the Standard deck contains a 4-match at **`L₀ = 8`**.
Detail in [math/NOTES.md](math/NOTES.md); empirical justification in [math/RESULTS.md](math/RESULTS.md). Two of the original spec's claims have been falsified by Monte Carlo simulation.

| Claim                                                                                | Status |
|--------------------------------------------------------------------------------------|--------|
| Deck = 64 odd-weight vectors of F_2^7.                                               | Trivially true. |
| Minimum match size = 4.                                                              | **Proven** (`math/NOTES.md` §2). |
| Match-finding reduces to a 4-cycle / Sidon condition.                                | **Proven** (`math/NOTES.md` §3-§4). |
| Maximum Sidon set in our deck = 9 (was previously claimed = 8).                      | **Proven** (Lemma D lower bound; **`s_max(O_7)=9`** certified by exhaustive search in `math/explore_sidon_odd_restricted`, **`--prove-odd-n 7`**). |
| Any **10**-card layout from **`D`** contains a 4-card match.                         | **Proven** from **`s_max(O_7)=9`** (`math/NOTES.md` §6 Corollary). Expert published play uses **fixed `L₀ = 10`** with **no** mid-game stock escalation. |
| Any **8**-card layout drawn only from the **Standard** deck (**six** active koi, **`|D| = 32`**, odd-weight vectors in **`F_2^6`** after fixing one omitted species) contains a 4-card match. | **Proven** from **`s_max(O_6)=7`** (`math/explore_sidon_odd_restricted`, **`--prove-odd-n 6`**). **`L₀ = 8`** Standard. |
| Σ R = 0 for the residual after the deck empties.                                     | **Proven** (`math/NOTES.md` §7.1). |
| The residual splits into two 4-card matches.                                         | **FALSE ~50% of the time.** Mode A: 51.7% unsplittable across 50k trials. Mode B at L=10: 47.4% unsplittable across 20k trials. |

The cited classical bound `max Sidon in F_2^k = 2^⌊k/2⌋` is wrong for our setup. Authoritative Sidon/code bounds and constructions in vector spaces appear in Ingo Czerwinski & Alexander Pott, *Sidon sets, sum-free sets and linear codes*, **Advances in Mathematics of Communications** 18 (2024), no. 2, 549–566 ([DOI](https://doi.org/10.3934/amc.2023054), [arXiv](https://arxiv.org/abs/2304.07906)) — summarized as **[CP24]** in [math/NOTES.md](math/NOTES.md). The headline consequences flow into the Rules section above and `PLAN.md` Phases 0, 2, 3.

## Open decisions (must be resolved before later phases)

1. ~~**Publication route**~~ — **resolved**: **Kickstarter** (crowdfunding). Pre-launch, campaign, pledge manager, fulfillment — details in `PLAN.md` Phase 10.
2. ~~**Dealing / endgame**~~ — **resolved:** **Standard `L₀ = 8`**, **Expert `L₀ = 10`**; **no** facedown flips on unanimous deadlock (tableau at **`L₀`** always contains a 4-match by Sidon bounds above). When replenishment drains the pile, flip **every** remnant (**max tableau**). **Stop** when everyone agrees **no legal 4-match** remains. **Score** = tally **every fish / koi** on **cards you claimed** only. **`L = 9, F = 8`** on **`|D|=64`** stays invalid.
3. ~~**Final 7-of-13 koi selection**~~ — **resolved**: Kohaku, Showa, Asagi, Ogon, Chagoi, Tancho, Kumonryu. See [koi_selection.md](koi_selection.md) for English/Japanese names, flavor blurbs, and the primary-color palette.
4. **Player count and turn structure** — turn structure **resolved: real-time call-out**. Call protocol: shout **"Koi!"** and then touch the four cards in order. Invalid-claim penalty: caller is locked out until another player claims a valid 4-card match (in mid-game this usually aligns with the next baseline replenishment; in the endgame it ends when anyone claims a legal 4-match on the residual). Player count still TBD (suggested 2–6); see `PLAN.md` Phase 3.
5. ~~**Art pipeline**~~ — **resolved**: **AI-generated**. Keep prompt logs, confirm commercial license, follow Phase 5 + Phase 8 (copyright / Kickstarter disclosure).
6. ~~**Digital bonus**~~ — **resolved**: **Rust** compiled to **WebAssembly** (`bonus_web/`) for in-browser play; Kickstarter stretch / add-on tier (ship both modes in rules + UI toggles eventually).
7. **Standard mode (future)** — (**a**) which of the seven koi is **excluded** from the 32-card subdeck (pedagogy + table presence); (**b**) **manufacturing cue** to separate Expert vs Standard piles from one print run (e.g. small **dot or icon in the upper corner** of the card front, color stripe, or distinct card back ring—decide in `design/style_guide.md`).

## Pointer

See `PLAN.md` for the full 12-phase publication roadmap and `ThirteenKoi.png` for the koi reference sheet.
