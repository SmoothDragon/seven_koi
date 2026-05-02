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
- `math/NOTES.md` — self-contained proof of the 4-card guarantee.
- `koi_selection.md` — the seven chosen koi (Phase 1 deliverable, **done**).

No source code yet (`math/verify.py` is the next planned artifact); no art beyond the reference sheet; no rules document yet.

## Game spec (verbatim from designer)

- **Total cards**: 64, sized as Magic: The Gathering cards (2.5" x 3.5" / 63 x 88 mm).
- **7 single-koi cards**: each of the 7 chosen koi featured prominently on one card with English name, Japanese name, and a large picture.
- **35 triple-koi cards** = C(7, 3): every 3-koi combination, with the three koi swimming toward each other in roughly the shape of a Reuleaux triangle.
- **21 quintuple-koi cards** = C(7, 5): every 5-koi combination, arranged in some interesting five-fold pattern.
- **1 all-seven card**: all 7 koi together.
- **Card count check**: 7 + 35 + 21 + 1 = 64. ✓

## Rules (verbatim from designer)

1. Shuffle the deck.
2. Lay out 9 cards.
3. By a Sidon-set property, there is guaranteed to be a set of 4 cards such that every koi is represented an even number of times. This is the match players are looking for.
4. Because every card has an odd number of koi on it (1, 3, 5, or 7), any subset of cards covering each koi an even number of times must contain an even number of cards; the smallest such match is 4 cards.
5. When a match is claimed, deal 4 more cards and repeat.
6. Eventually 8 cards remain; due to the math, these split exactly into two groups of 4. Whichever player identifies one group of 4 collects both groups.
7. **Score** = total number of koi (across all collected cards) for each player.

## Math claims

The full self-contained proof of the 4-card guarantee is in [math/NOTES.md](math/NOTES.md), which adapts the argument from the designer's reference at <https://chatgpt.com/share/69f67dcc-d818-832f-80a4-bb5e0c37e963> ("Subset sum to zero"). Independent computational verification (`math/verify.py`) is still pending — see `PLAN.md` Phase 2.

- The 64 cards are exactly the odd-weight vectors in F_2^7. ✓ (combinatorially obvious)
- A "match" = subset whose XOR is the zero vector.
- **Minimum match size = 4.** Every card has odd Hamming weight, so any non-empty subset that XORs to 0 must have even size. Size 2 would require two identical cards (impossible in this deck), so the smallest non-trivial match has 4 cards. ✓ (proof in `math/NOTES.md` §2)
- **Every 9-card subset of the 64 contains a 4-card match.** Equivalent to: the maximum Sidon set among the 64 odd-weight vectors of F_2^7 has size ≤ 8. The natural set {e_1, ..., e_7, 𝟙} achieves size 8 and is maximal (every additional odd-weight vector closes a 4-cycle). Proof in `math/NOTES.md` §3–6, modulo the cited classical bound `max Sidon in F_2^7 = 2^⌊7/2⌋ = 8`.
- **Endgame split**: the final 8 cards always split exactly into two 4-card matches. *Not yet proven*; brute-force verification scheduled in Phase 2 (depends on which dealing convention is chosen).

## Open decisions (must be resolved before later phases)

1. **Publication route** — print-on-demand, Kickstarter, pitch-to-publisher, or personal/hobby?
2. **Dealing math reconciliation** — initial layout 9 + endgame 8 doesn't close: 64 = 9 + 4M + 8 gives M = 11.75. Likely fixes: deal 8 initially (clean), deal 12 initially (clean), or stop replenishing once the deck empties (residual handled explicitly).
3. ~~**Final 7-of-13 koi selection**~~ — **resolved**: Kohaku, Showa, Asagi, Ogon, Chagoi, Tancho, Kumonryu. See [koi_selection.md](koi_selection.md) for English/Japanese names, flavor blurbs, and the primary-color palette.
4. **Player count and turn structure** — real-time call-out vs turn-based scan; suggested 2–6 players.
5. **Art pipeline** — commissioned illustrator, DIY, or AI-generated (with copyright implications).
6. **Digital prototype** — whether to build a Tabletop Simulator mod or web prototype for remote playtesting.

## Pointer

See `PLAN.md` for the full 12-phase publication roadmap and `ThirteenKoi.png` for the koi reference sheet.
