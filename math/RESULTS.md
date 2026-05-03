# math/RESULTS.md — Monte Carlo simulation results

Empirical results from `math/verify.py`. **These results invalidate the original game spec's two central mathematical claims** — see §4 for the executive summary.

For published theorems on Sidon sets in `F_2^t`, improved upper bounds, and the code-theoretic viewpoint, see Czerwinski–Pott, *Sidon sets, sum-free sets and linear codes*, *Adv. Math. Commun.* 18 (2024), 549–566 ([DOI](https://doi.org/10.3934/amc.2023054), [arXiv:2304.07906](https://arxiv.org/abs/2304.07906)); cross-references in [math/NOTES.md](math/NOTES.md) use the tag **[CP24]**.

All trials use Python's `random` with `--seed 1`. Reproduce with the commands shown.

---

## 1. Maximum Sidon set in odd-weight F_2^7

Recall: a Sidon set in our setting is a set of cards containing no 4-card match.

### 1.1 Counterexample to the cited classical bound

The original `math/NOTES.md` cited the formula `max Sidon in F_2^k = 2^⌊k/2⌋`, giving max = 8 for `k = 7`. **This is wrong** for the odd-weight subset. A direct counterexample of size 9 (found by simulation, then hand-verified):

```
{25, 28, 35, 47, 55, 70, 73, 100, 110}
= {0011001, 0011100, 0100011, 0101111, 0110111, 1000110, 1001001, 1100100, 1101110}
```

All 9 vectors have odd Hamming weight (3 or 5); all C(9,2) = 36 pairwise XORs are distinct; no 4-element subset XORs to 0. Schur triples are vacuously absent in odd-weight (`a + b` is even-weight, `c` is odd-weight). So this is a strict 9-element Sidon set in F_2^7, refuting `max ≤ 8`.

### 1.2 Empirical upper bound

Random greedy strict-Sidon construction, 50,000 trials, on the odd-weight deck (size 64):

| Final size | Frequency |
|------------|-----------|
| 8          | 1,892     |
| 9          | 48,108    |
| 10         | 0         |

For comparison, on the full F_2^7 \ {0} (size 127), 50k random greedy trials all landed at size **11** (matching the Singer / projective-plane construction expectation).

**Conclusion:** the maximum Sidon set in the 64-card odd-weight deck is **at least 9** (constructive) and **at most 9** with very high empirical confidence. Formal proof of the upper bound is still open.

---

## 2. Mode B — game-flow simulation: layout size sweep

Maintain an L-card layout, find a random 4-card match in the layout, remove it, replenish from the deck. Iterate until the deck is empty (then 8 cards remain; check whether they split into two 4-card matches) or no match exists in the current layout (mid-game stall).

20,000 trials per L:

```
python3 math/verify.py --trials 20000 --mode b --layout-size <L> --seed 1
```

| L  | Mid-game stalls | Reached residual | Splittable residual | Unsplittable residual |
|----|-----------------|------------------|---------------------|-----------------------|
| 8  | 19,298 (96.5%)  | 702              | 56.8%               | 43.2%                 |
| 9  | 8,069 (40.3%)   | 11,931           | 53.6%               | 46.4%                 |
| 10 | 0 (0%)          | 20,000           | 52.6%               | 47.4%                 |

**Two findings:**

1. **L = 9 stalls 40% of the time.** This is consistent with §1: the 4-card guarantee fails because max Sidon in our deck is 9, not 8 — so 9-card layouts can themselves be Sidon and contain no match. The original game spec is broken.
2. **L = 10 never stalls** (across 20,000 trials). This is necessary for the threshold `max Sidon < L`, i.e. `L ≥ 10`.

---

## 3. Mode A — abstract reachability of unsplittable residuals

Pick random 4-card matches from the *entire* remaining deck (not from a layout). No game-flow constraints — this measures whether the unsplittable residuals discussed in `math/NOTES.md` §7.2 can be reached under *any* valid sequence of match-removals.

50,000 trials:

```
python3 math/verify.py --trials 50000 --mode a --seed 1
```

| Outcome             | Count  | %       |
|---------------------|--------|---------|
| Reached residual    | 50,000 | 100%    |
| Splittable          | 24,150 | 48.3%   |
| Unsplittable        | 25,850 | 51.7%   |
| Distinct unsplittable residuals seen | 25,841 | — |

**Findings:**

* The 8-card residual is unsplittable roughly **half the time** under random play. This is far worse than the original spec implied.
* The unsplittable residuals are not concentrated on `S*` — almost every unsplittable residual seen was unique. There is a very large family of maximal Sidon 8-element subsets of the deck reachable as residuals.
* The Mode B (`L = 10`) splittability rate (52.6%) closely matches the Mode A rate (48.3%), suggesting the layout-based game-flow constraint does not significantly bias residuals away from the unsplittable region.

---

## 4. Executive summary — what the game spec requires changing

The original Seven Koi rules rest on two mathematical claims that are now empirically refuted:

| Claim (original spec)                                                       | Status              |
|-----------------------------------------------------------------------------|---------------------|
| "9 cards always contain a 4-card match"                                     | **False.** Counterexamples exist (§1.1). With L = 9, ~40% of random games stall mid-deck (§2). |
| "The final 8 cards always split into two 4-card matches"                    | **False ~50% of the time.** Under random play, ~48% of residuals are splittable; ~52% are not (§3). |

What *is* still true:

* `Σ D = 0` (every koi appears in exactly 32 of the 64 cards) — proven in `math/NOTES.md` §7.1, sanity-check in the simulation passes.
* The residual 8 cards always XOR to 0 (an 8-card match in the parity sense), even when they don't split into two 4-card pieces.
* `L ≥ 10` is **necessary and sufficient** to guarantee that every layout contains a 4-card match (necessary because max Sidon = 9, sufficient because L = 10 > 9).
* Minimum match size is still 4 (Lemma A in `math/NOTES.md` §2 is unaffected).

### 4.1 Implications for the design

1. **Layout size must change from 9 to 10** to keep the game from stalling. With `L = 10` and the original 64-card deck, the dealing arithmetic becomes `64 = 10 + 4M + F`. Two clean choices: `(L, F) = (10, 10)` with `M = 11`, or `(L, F) = (10, 6)` with `M = 12`. Neither matches the original "8 final cards" intuition; the endgame arithmetic needs to be re-thought.
2. **The endgame "claim one → claim both" rule cannot be the default** — it works less than half the time. Either:
   * The fallback rule from `PLAN.md` Phase 3 (60-second silence → award the residual to the player with the most recent mid-game claim) is invoked nearly every game, which is unsatisfying.
   * The endgame is restructured: e.g. when the deck is empty, *continue* normal real-time play on the residual until either it's exhausted by 4-card claims (residual reaches 0 or 4 cards) or no further claims are possible; un-claimable residual cards are split evenly or awarded to the leader. This preserves the matching-game pacing without leaning on a false splitting theorem.
3. The size-9 Sidon counterexample in §1.1 is also a *teaching example* — if any player ever sees a 9-card layout matching that pattern under L = 9, they were genuinely stuck. Showing this in playtest helps build intuition for why L must increase.

---

## 5. Reproducibility

```bash
cd math
python3 verify.py --trials 50000 --mode a   --seed 1
python3 verify.py --trials 20000 --mode b --layout-size  8 --seed 1
python3 verify.py --trials 20000 --mode b --layout-size  9 --seed 1
python3 verify.py --trials 20000 --mode b --layout-size 10 --seed 1
```

Single-trial sanity check on the size-9 counterexample:

```bash
python3 -c "
import itertools
S = [25, 28, 35, 47, 55, 70, 73, 100, 110]
sums = [a^b for a,b in itertools.combinations(S, 2)]
print('size:', len(S))
print('all odd-weight:', all(bin(v).count('1') % 2 == 1 for v in S))
print('Sidon (pairwise XORs distinct):', len(set(sums)) == len(sums))
print('any 4-card match:', any(a^b^c^d == 0 for a,b,c,d in itertools.combinations(S, 4)))
"
```
