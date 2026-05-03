# CLAUDE.md — Seven Koi project brief

This file lets a fresh AI agent (Claude, Cursor, etc.) recreate the current state of the Seven Koi project from a clean checkout. Read this first, then read `PLAN.md` for the publication roadmap.

## Project

**Seven Koi** is a 64-card matching card game built around XOR/parity matches across 7 koi varieties. Cards correspond to the 64 odd-weight binary vectors of length 7 (i.e. all subsets of size 1, 3, 5, or 7 from a 7-element set: 7 + 35 + 21 + 1 = 64). A "match" is a set of cards whose XOR is zero — every koi appears an even number of times.

## Repo state (as of this writing)

- `README.md` — 3 lines: project name and the tagline "Matching card game".
- `.gitignore` — the standard GitHub Python template (suggests Python tooling is fine for math verification and any card-layout scripts).
- `ThirteenKoi.png` — reference grid of 13 popular koi varieties with English/Japanese names and one-line descriptions. The 13 varieties are: Kohaku, Showa, Asagi, Shusui, Ogon, Chagoi, Utsurimono, Tancho, Kumonryu, Hariwake, Sanke, Bekko, Utsuri. Seven of these will be selected for the game (see Open Decisions).
- `PLAN.md` — 12-phase publication roadmap.
- `CLAUDE.md` — this file.
- `math/NOTES.md` — math claims with corrected status; includes **[CP24]** bibliography (Sidon sets / codes).
- `math/RESULTS.md` — Monte Carlo simulation report falsifying two of the original spec's claims.
- `math/verify.py` — Python verifier with sanity asserts and Mode A / Mode B Monte Carlo (`python3 math/verify.py --help`).
- `bonus_web/` — Rust → WebAssembly stub for the Kickstarter digital bonus (`wasm-pack` build). See [bonus_web/README.md](bonus_web/README.md).

## Game spec (verbatim from designer)

- **Total cards**: 64, sized as Magic: The Gathering cards (2.5" x 3.5" / 63 x 88 mm).
- **7 single-koi cards**: each of the 7 chosen koi featured prominently on one card with English name, Japanese name, and a large picture.
- **35 triple-koi cards** = C(7, 3): every 3-koi combination, with the three koi swimming toward each other in roughly the shape of a Reuleaux triangle.
- **21 quintuple-koi cards** = C(7, 5): every 5-koi combination, arranged in some interesting five-fold pattern.
- **1 all-seven card**: all 7 koi together.
- **Card count check**: 7 + 35 + 21 + 1 = 64. ✓

## Rules (current working version, after math correction)

The original spec said "lay out 9 cards" and "the final 8 cards split into two 4-card matches". Both are mathematically false; see `math/RESULTS.md` §4. The current working rules are:

1. Shuffle the deck.
2. **Lay out 10 cards** (was 9). Smaller layouts can stall — `math/RESULTS.md` §2 shows L=9 stalls 40% of trials, L=8 stalls 96%.
3. **Match definition**: a *match* is 4 cards in which every koi appears an even number of times (equivalently, the 4 cards XOR to 0). The minimum match size is 4 (proven in `math/NOTES.md` §2). With L=10 every layout is guaranteed to contain at least one 4-card match (`math/NOTES.md` §6, conditional on the empirical max-Sidon = 9).
4. **Real-time call-out** (locked, decision #4): all players scan simultaneously; the first to shout "Koi!" and touch four cards in order claims them. Invalid claim → caller is locked out until another player claims a valid match.
5. After a successful claim, deal 4 cards from the deck to bring the layout back to 10. Repeat.
6. **Endgame**: when the deck empties, 10 cards remain on the table (with `L=10, F=10` dealing; `M=11` mid-game matches). The residual XORs to 0 (Lemma E in `math/NOTES.md` §7.1) but does **not** reliably split into clean 4-card pieces (~50% of residuals are unsplittable per `math/RESULTS.md` §3). Real-time play simply continues on the residual until either (a) successful claims reduce it to 0, 2, or 6 cards, or (b) no player can find a match within a 60-second silence. Any cards left at the end are split evenly.
7. **Score** = total number of koi (across all collected cards) for each player. Tiebreakers: most cards collected, then most all-seven cards, then highest-weight single card.

## Math claims (status table)

Detail in [math/NOTES.md](math/NOTES.md); empirical justification in [math/RESULTS.md](math/RESULTS.md). Two of the original spec's claims have been falsified by Monte Carlo simulation.

| Claim                                                                                | Status |
|--------------------------------------------------------------------------------------|--------|
| Deck = 64 odd-weight vectors of F_2^7.                                               | Trivially true. |
| Minimum match size = 4.                                                              | **Proven** (`math/NOTES.md` §2). |
| Match-finding reduces to a 4-cycle / Sidon condition.                                | **Proven** (`math/NOTES.md` §3-§4). |
| Maximum Sidon set in our deck = 9 (was previously claimed = 8).                      | **Proven lower bound**, **upper bound 9** with very high empirical confidence (50k random greedy trials, all max ≤ 9). |
| Any 9-card layout contains a 4-card match.                                           | **FALSE.** Counterexample: `{25, 28, 35, 47, 55, 70, 73, 100, 110}` is a 9-element Sidon set in our deck. |
| Any **10**-card layout contains a 4-card match.                                      | **Conditionally true** assuming max-Sidon = 9 (and consistent with 0 stalls in 20k Mode B trials at L=10). |
| Σ R = 0 for the residual after the deck empties.                                     | **Proven** (`math/NOTES.md` §7.1). |
| The residual splits into two 4-card matches.                                         | **FALSE ~50% of the time.** Mode A: 51.7% unsplittable across 50k trials. Mode B at L=10: 47.4% unsplittable across 20k trials. |

The cited classical bound `max Sidon in F_2^k = 2^⌊k/2⌋` is wrong for our setup. Authoritative Sidon/code bounds and constructions in vector spaces appear in Ingo Czerwinski & Alexander Pott, *Sidon sets, sum-free sets and linear codes*, **Advances in Mathematics of Communications** 18 (2024), no. 2, 549–566 ([DOI](https://doi.org/10.3934/amc.2023054), [arXiv](https://arxiv.org/abs/2304.07906)) — summarized as **[CP24]** in [math/NOTES.md](math/NOTES.md). The headline consequences flow into the Rules section above and `PLAN.md` Phases 0, 2, 3.

## Open decisions (must be resolved before later phases)

1. ~~**Publication route**~~ — **resolved**: **Kickstarter** (crowdfunding). Pre-launch, campaign, pledge manager, fulfillment — details in `PLAN.md` Phase 10.
2. **Dealing math reconciliation** — recommended `L = 10, F = 10` per `math/RESULTS.md` (the original `L = 9, F = 8` is mathematically broken). Endgame is continued real-time play on the 10-card residual until either successful claims reduce it or 60s of silence terminates it.
3. ~~**Final 7-of-13 koi selection**~~ — **resolved**: Kohaku, Showa, Asagi, Ogon, Chagoi, Tancho, Kumonryu. See [koi_selection.md](koi_selection.md) for English/Japanese names, flavor blurbs, and the primary-color palette.
4. **Player count and turn structure** — turn structure **resolved: real-time call-out**. Call protocol: shout **"Koi!"** and then touch the four cards in order. Invalid-claim penalty: caller is locked out until another player claims a valid 4-card match (in mid-game this coincides with the next replenishment; in the endgame it's when another player claims one of the two final 4-card groups). Player count still TBD (suggested 2–6); see `PLAN.md` Phase 3.
5. ~~**Art pipeline**~~ — **resolved**: **AI-generated**. Keep prompt logs, confirm commercial license, follow Phase 5 + Phase 8 (copyright / Kickstarter disclosure).
6. ~~**Digital bonus**~~ — **resolved**: **Rust** compiled to **WebAssembly** (`bonus_web/`) for in-browser play; Kickstarter stretch / add-on tier.

## Pointer

See `PLAN.md` for the full 12-phase publication roadmap and `ThirteenKoi.png` for the koi reference sheet.
