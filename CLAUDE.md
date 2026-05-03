# CLAUDE.md — Seven Koi project brief

This file lets a fresh AI agent (Claude, Cursor, etc.) recreate the current state of the Seven Koi project from a clean checkout. Read this first, then read `PLAN.md` for the publication roadmap.

## Project

**Seven Koi** is a matching card game around XOR / parity matches. The **standard** deck has **seven** listed koi; a **beginner** mode uses exactly **six** of those seven (one koi omitted) and **half** as many cards (32)—the printable deck can carry both halves on shared artwork with a mechanical way to partition (see Open decisions). Cards are sized as Magic-style (2.5" × 3.5").

## Repo state (as of this writing)

- `README.md` — 3 lines: project name and the tagline "Matching card game".
- `.gitignore` — the standard GitHub Python template (suggests Python tooling is fine for math verification and any card-layout scripts).
- `ThirteenKoi.png` — reference grid of 13 popular koi varieties with English/Japanese names and one-line descriptions. The 13 varieties are: Kohaku, Showa, Asagi, Shusui, Ogon, Chagoi, Utsurimono, Tancho, Kumonryu, Hariwake, Sanke, Bekko, Utsuri. Seven of these will be selected for the game (see Open Decisions).
- `PLAN.md` — 12-phase publication roadmap.
- `CLAUDE.md` — this file.
- `math/NOTES.md` — math claims with corrected status; includes **[CP24]** bibliography (Sidon sets / codes).
- `math/RESULTS.md` — Monte Carlo simulation report falsifying two of the original spec's claims.
- `math/verify.py` — Python verifier with sanity asserts and Mode A / Mode B Monte Carlo (`python3 math/verify.py --help`).
- `math/layout_stall_sweep.py` — Mode B stall rates vs layout size **`L`** across odd-weight decks (`n = 4`…`7`); see `math/RESULTS.md` §2.1.
- `math/explore_sidon_odd_restricted/` — Rust CLI for strict Sidon maxima on odd / even / ambient slices (`cargo run --release` after `cd` there).
- `bonus_web/` — Rust → WebAssembly stub for the Kickstarter digital bonus (`wasm-pack` build). See [bonus_web/README.md](bonus_web/README.md).

## Game spec (verbatim from designer)

- **Total cards**: 64, sized as Magic: The Gathering cards (2.5" x 3.5" / 63 x 88 mm).
- **7 single-koi cards**: each of the 7 chosen koi featured prominently on one card with English name, Japanese name, and a large picture.
- **35 triple-koi cards** = C(7, 3): every 3-koi combination, with the three koi swimming toward each other in roughly the shape of a Reuleaux triangle.
- **21 quintuple-koi cards** = C(7, 5): every 5-koi combination, arranged in some interesting five-fold pattern.
- **1 all-seven card**: all 7 koi together.
- **Card count check**: 7 + 35 + 21 + 1 = 64. ✓

- **Beginner variant**: 32-card subdeck = odd-weight subsets of **six** koi once one canonical koi has been omitted (see Open decisions): C(6,1) + C(6,3) + C(6,5) = 32. Same card size.

## Rules (current working — standard + beginner)

The designer's earliest spec overstated splitting the residual; details in `math/RESULTS.md` §4.

**Choose a version before setup.** Same turn structure for both unless noted.

### Shared mechanics

1. **Prepare the deck.** Use only cards legal for that version (64 standard / 32 beginner)—see Open decisions about physically splitting a single print run.

2. **Shuffle.**

3. **Layout baseline and replenishment (version-specific)** — **`L₀`** = face-up count you restore toward **after each successful claim**, drawing from the deck until that count is reached or the deck empties (**partial replenish** OK). **Mid-game escalation** (after everyone agrees **no** match is visible but stock remains): flip **exactly one** facedown card onto the tableau per unanimous deadlock — never several at once to “skip” toward the tabletop cap (**`13`** standard / **`10`** beginner). Replenishment after claims may draw **multiple** cards in one refresh to refill toward **`L₀`**; escalation is strictly **single-card**.
   - **Standard (`|D| = 64`, seven active koi).** **`L₀ = 10`**. Lay out ten cards initially. Between claims: if **all players unanimously agree** that **no legal 4-card match** is showing, flip **one** extra card from the facedown pile (**escalation**); repeat until someone claims or the spread reaches **13**. Per **[CP24]** (`math/NOTES.md` References), **13** arbitrary cards in **`GF(2)^7`** force **some** 4-card XOR match. *Separately,* deck-specific math yields **every 10-card** layout from **`D`** contains a match **conditional on** `max Sidon = 9` (`math/NOTES.md` §6). After any claim remove the scored four cards, then replenish from the deck toward **`L₀`** again.
   - **Beginner (`|D| = 32`, six active koi).** **`L₀ = 8`**. Recommended from Mode B empirical sweep on the **`n = 6`** odd-weight deck (`math/layout_stall_sweep.py`, summarized in **`math/RESULTS.md`**): **`L = 7` stalls badly in simulation**, **`L ≥ 8` did not stall** under the same random-play model. Replenish toward **eight** when the deck has stock. (**`32 − L₀ = 24`** is divisible by **4**; **`|spread| < L₀`** still occurs after a scored match once facedown stock is depleted—same endgame mechanic as standard.) Use the **same** unanimous-deadlock rule: flip **one** extra card face up until someone claims **or** the spread reaches **`10`** — **`[CP24]`** backs **`|layout| ≥ 10`** inside **`GF(2)^6`** as a deterministic existential ceiling, analogous to **13** in standard.

4. **Match:** four distinct active cards XOR to **0** ↔ every depicted koi appears **0 / 2 / 4** times (minimum four cards holds on odd-only decks — `math/NOTES.md` §2).

5. **Claim:** shout **"Koi!"**, then touch **four distinct cards** in order. Invalid claim — caller is locked out until **another** player claims a valid 4-card match (mid-game lockout clears with the next replenishment).

6. **Endgame:** when replenishing hits an **empty** deck, put **every** remaining facedown card onto the tableau in **one sweep** (**not** the one-card-at-a-time escalation rule) (**`|spread| < L₀`** is OK — **no facedown stubs** besides cards players already claimed). XOR conservation still matches Lemma E (**`math/NOTES.md` §7.1**); unnoticed legal matches can still lurk (**`math/RESULTS.md` §3**). Keep claiming while anyone spots a legal 4-card match. Once **everyone agrees** **no matches remain**, **end**.
7. **Score:** **fish / koi** = tally **every koi depiction** printed on cards **you claimed** (single = 1, triple = 3, quint = 5, all-koi = 7 standard / 6 beginner). Cards **left on the tableau** add **nothing** — they are effectively discarded for scoring.

8. **Tiebreakers** (still apply when totals tie): most cards claimed, then most **all-koi** cards (`|K|=7` / `|K|=6`), then **highest-weight single card among active species**.

### Standard — seven koi

- **`|D| = 64`:** all odd-weight bit vectors over the seven chosen koi (`C(7,1) + C(7,3) + C(7,5) + C(7,7)`).

### Beginner — six koi

- **`|D| = 32`:** fix one omitted koi; keep only cards that **never** depict that species. Equivalently, all odd-cardinality subsets drawn from the other six (`C(6,1)+C(6,3)+C(6,5)=32`).
- Glyph row on templates uses **six** filled circles plus one muted column for the dormant species—or omit that column entirely once the omission is finalized.
- Graphic production still needs an **inventory split aid** so players can sort a unified print run quickly (corner **dot / icon / color nib** proposals live in Open decisions).

## Math claims (status table)

Applies **as written** to the **seven-koi standard deck.** The **six-koi beginner deck** inherits the XOR / parity lemmas on its own affine slice; extend **`verify.py`** / **`layout_stall_sweep.py`** if you tighten formal **`max Sidon`** claims for **`|D| = 32`**.
Detail in [math/NOTES.md](math/NOTES.md); empirical justification in [math/RESULTS.md](math/RESULTS.md). Two of the original spec's claims have been falsified by Monte Carlo simulation.

| Claim                                                                                | Status |
|--------------------------------------------------------------------------------------|--------|
| Deck = 64 odd-weight vectors of F_2^7.                                               | Trivially true. |
| Minimum match size = 4.                                                              | **Proven** (`math/NOTES.md` §2). |
| Match-finding reduces to a 4-cycle / Sidon condition.                                | **Proven** (`math/NOTES.md` §3-§4). |
| Maximum Sidon set in our deck = 9 (was previously claimed = 8).                      | **Proven lower bound**, **upper bound 9** with very high empirical confidence (50k random greedy trials, all max ≤ 9). |
| Any 9-card layout contains a 4-card match.                                           | **FALSE.** Counterexample: `{25, 28, 35, 47, 55, 70, 73, 100, 110}` is a 9-element Sidon set in our deck. |
| Any **10**-card layout contains a 4-card match.                                      | **Conditionally true** assuming max-Sidon = 9 in **`D`** (and Mode B **`L = 10`** trials never stalled). Published play uses **baseline 10 + one-card-at-a-time escalation toward ≤ 13 tableau** (`PLAN.md` Phase 0); **[CP24]** backs the existential cap at **13**. |
| Σ R = 0 for the residual after the deck empties.                                     | **Proven** (`math/NOTES.md` §7.1). |
| The residual splits into two 4-card matches.                                         | **FALSE ~50% of the time.** Mode A: 51.7% unsplittable across 50k trials. Mode B at L=10: 47.4% unsplittable across 20k trials. |

The cited classical bound `max Sidon in F_2^k = 2^⌊k/2⌋` is wrong for our setup. Authoritative Sidon/code bounds and constructions in vector spaces appear in Ingo Czerwinski & Alexander Pott, *Sidon sets, sum-free sets and linear codes*, **Advances in Mathematics of Communications** 18 (2024), no. 2, 549–566 ([DOI](https://doi.org/10.3934/amc.2023054), [arXiv](https://arxiv.org/abs/2304.07906)) — summarized as **[CP24]** in [math/NOTES.md](math/NOTES.md). The headline consequences flow into the Rules section above and `PLAN.md` Phases 0, 2, 3.

## Open decisions (must be resolved before later phases)

1. ~~**Publication route**~~ — **resolved**: **Kickstarter** (crowdfunding). Pre-launch, campaign, pledge manager, fulfillment — details in `PLAN.md` Phase 10.
2. **Dealing / endgame** — **Standard:** **`L₀ = 10`**, then deadlock **→ exactly one stock flip** (**repeat**) until a claim lands **or** tableau reaches **`13`**. **Beginner:** **`L₀ = 8`**, same (**one flip per deadlock**) up to tableau **`10`**. When replenishment drains the pile, flip **every** remnant (**max tableau** — **not** escalation). **Stop** when everyone agrees **no legal 4-match** remains. **Score** = tally **every fish / koi** on **cards you claimed** only. **`L = 9, F = 8`** on **`|D|=64`** stays invalid.
3. ~~**Final 7-of-13 koi selection**~~ — **resolved**: Kohaku, Showa, Asagi, Ogon, Chagoi, Tancho, Kumonryu. See [koi_selection.md](koi_selection.md) for English/Japanese names, flavor blurbs, and the primary-color palette.
4. **Player count and turn structure** — turn structure **resolved: real-time call-out**. Call protocol: shout **"Koi!"** and then touch the four cards in order. Invalid-claim penalty: caller is locked out until another player claims a valid 4-card match (in mid-game this usually aligns with the next baseline replenishment; in the endgame it ends when anyone claims a legal 4-match on the residual). Player count still TBD (suggested 2–6); see `PLAN.md` Phase 3.
5. ~~**Art pipeline**~~ — **resolved**: **AI-generated**. Keep prompt logs, confirm commercial license, follow Phase 5 + Phase 8 (copyright / Kickstarter disclosure).
6. ~~**Digital bonus**~~ — **resolved**: **Rust** compiled to **WebAssembly** (`bonus_web/`) for in-browser play; Kickstarter stretch / add-on tier (ship both modes in rules + UI toggles eventually).
7. **Beginner mode (future)** — (**a**) which of the seven koi is **excluded** from the 32-card subdeck (pedagogy + table presence); (**b**) **manufacturing cue** to separate standard vs beginner piles from one print run (e.g. small **dot or icon in the upper corner** of the card front, color stripe, or distinct card back ring—decide in `design/style_guide.md`).

## Pointer

See `PLAN.md` for the full 12-phase publication roadmap and `ThirteenKoi.png` for the koi reference sheet.
