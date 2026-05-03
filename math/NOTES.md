# math/NOTES.md — Seven Koi: math claims, status, and proofs

This note tracks the central mathematical claims behind Seven Koi, what is proven, what was disproven by simulation, and what remains open. **Two of the original spec's claims have been falsified by the Monte Carlo in `math/RESULTS.md`** — the headline change is summarized in §0 and propagated through the rest of this document.

A previous version of this note attempted to prove the original spec by citing a closed-form bound on Sidon sets in `F_2^k` (`max ≤ 2^⌊k/2⌋`). That bound is incorrect at `k = 7` for our setting (and arguably for the full vector space too — see `math/RESULTS.md` §1.2). The proof is rebuilt below from first principles.

Conventions: `+` denotes XOR (addition in F_2). `wt(v)` is the Hamming weight of `v`. The 7 koi are indexed 0..6 and a card is the bit vector `v ∈ F_2^7` whose i-th bit is 1 iff koi i appears on the card.

---

## 0. Headline status

| Claim                                                                                         | Status                                       |
|-----------------------------------------------------------------------------------------------|----------------------------------------------|
| Deck is the 64 odd-weight vectors of F_2^7.                                                   | **Trivially true** (§1).                     |
| Minimum match size = 4.                                                                       | **Proven** (§2 Lemma A).                     |
| Match-finding reduces to a 4-cycle / Sidon condition.                                         | **Proven** (§3–§4 Lemmas B, C).              |
| Maximum Sidon set in our deck has size **9** (not 8 as previously claimed).                   | **Proven lower bound** (§5 Lemma D), **upper bound 9 with very high empirical confidence** (§5 Remark; `math/RESULTS.md` §1.2). |
| Any 9-card layout contains a 4-card match.                                                    | **FALSE** (§6 Theorem). Counterexample exhibited. |
| Any **10**-card layout contains a 4-card match.                                               | **Conditionally true** assuming max Sidon = 9 (§6 Corollary). |
| Σ R = 0 for the 8-card residual after the deck empties.                                       | **Proven** (§7.1 Lemma E).                   |
| The 8-card residual always splits into two 4-card matches.                                    | **FALSE.** Splittable only ~52% of the time under random play (`math/RESULTS.md` §3). |

The headline consequence is that the original game's `L = 9` layout size and "claim one → claim both" endgame rule are both unsupported. See `math/RESULTS.md` §4 for the design implications and the proposed revisions tracked in `PLAN.md` Phase 0.

---

## 1. Setup

The deck is the set `D ⊂ F_2^7` of all 64 odd-weight 7-bit vectors:

| weight | count    | game role         |
|--------|----------|-------------------|
| 1      | C(7,1)=7  | single-koi cards |
| 3      | C(7,3)=35 | triple-koi cards |
| 5      | C(7,5)=21 | quintuple cards  |
| 7      | C(7,7)=1  | all-seven card   |

Total: 7 + 35 + 21 + 1 = 64. ✓

A **match** is a non-empty subset `M ⊆ D` with `Σ M = 0` — equivalently, every koi appears an even number of times across the cards in `M`.

---

## 2. Lemma A — every match has even size

**Claim.** If `M ⊆ D` is non-empty and `Σ M = 0`, then `|M|` is even.

**Proof.** For any `v ∈ D`, `wt(v)` is odd, so the parity bit `wt(v) mod 2` equals 1. Summing over `M` in F_2:

```
0 = wt(Σ M) ≡ Σ wt(v) ≡ |M| (mod 2)
```

so `|M|` is even. ∎

Combined with the fact that the deck has no duplicate cards (so no 2-element match exists), the smallest possible match has size 4.

---

## 3. Lemma B — Sidon reduction

**Definition.** A set `S ⊆ F_2^k` is a **strict Sidon set** if it satisfies:

* (a) `0 ∉ S`,
* (b) elements of `S` are distinct,
* (c) **no Schur triple**: for all distinct `a, b, c ∈ S`, `a + b ≠ c`,
* (d) **no 4-cycle**: for all distinct `a, b, c, d ∈ S`, `a + b ≠ c + d`.

**Claim.** A set `S ⊆ F_2^k` contains no non-empty subset of size ≤ 4 summing to 0 iff `S` is a strict Sidon set.

**Proof.** Each forbidden zero-sum corresponds directly to a violated condition:

* size 1: `v = 0` ⟺ violates (a),
* size 2: `v + w = 0` with `v ≠ w` impossible in F_2; equality `v = w` violates (b),
* size 3: `a + b + c = 0` ⟺ `a + b = c`, violating (c),
* size 4: `a + b + c + d = 0` ⟺ `a + b = c + d`. If `{a,b}` and `{c,d}` overlap in one element, the equation forces a duplicate (violates (b)); if disjoint, it violates (d).

Conversely each violation gives a zero-sum of the corresponding size. ∎

---

## 4. Lemma C — for our deck, Sidon = "no 4-cycle"

**Claim.** Every subset `S ⊆ D` automatically satisfies (a), (b), (c). So `S` is strict-Sidon iff it contains no 4-cycle iff it contains no 4-card match.

**Proof.**

* (a) `0 ∉ D` because `wt(0) = 0` is even.
* (b) The deck `D` consists of distinct vectors by construction.
* (c) For distinct `a, b, c ∈ D`, the sum `a + b + c` has parity `1 + 1 + 1 = 1 (mod 2)`, so `wt(a + b + c)` is odd, hence nonzero. So `a + b ≠ c`.

Therefore in our setting "Sidon" reduces to condition (d) alone. ∎

---

## 5. Lemma D — a 9-element Sidon set in `D`

**Claim.** The set

```
S₉ = {25, 28, 35, 47, 55, 70, 73, 100, 110}
   = {0011001, 0011100, 0100011, 0101111, 0110111, 1000110, 1001001, 1100100, 1101110}
```

is a strict Sidon set in `D` of size 9.

**Proof.** All 9 vectors have odd Hamming weight (three of weight 5, six of weight 3) so `S₉ ⊂ D`. Conditions (a), (b), (c) of Lemma B hold by Lemma C. For (d) we need all `C(9, 2) = 36` pairwise XORs distinct. Direct computation (`math/verify.py` includes this as a sanity print) gives 36 distinct values in the 64-element even-weight subspace of F_2^7. ∎

This refutes the original `math/NOTES.md` claim that the maximal Sidon set had size 8 (`S* = {e_1, ..., e_7, 𝟙}`). `S*` is still *a* maximal-by-extension Sidon set, but it is not the unique-up-to-symmetry maximum — `S₉` is strictly larger.

**Remark (empirical upper bound).** Random greedy strict-Sidon construction never exceeds size 9 across 50,000 trials (`math/RESULTS.md` §1.2). Together with the size-9 lower bound, this is very strong evidence that `max{|S| : S ⊆ D Sidon} = 9`. A formal proof of the upper bound is still open — a brute-force exhaustive DFS times out under naive pruning; a proper proof likely requires the affine geometry of F_2^7 or a direct Hamming-code argument. For the design purposes below we treat `max Sidon = 9` as established at the empirical level.

---

## 6. Theorem — the (corrected) match guarantee

**Theorem.** A 9-card layout *can* fail to contain a 4-card match. Specifically, the set `S₉` from Lemma D is itself a 9-card layout with no 4-card sub-match.

**Proof.** By Lemma D, `S₉` is a strict Sidon set, equivalently (by Lemma C) it contains no 4-card match. ∎

**Corollary (conditional on max Sidon = 9).** Every 10-card subset of `D` contains a 4-card match.

**Proof.** Any 10-card subset `L ⊆ D` has |L| = 10 > 9 = max Sidon, so `L` is not Sidon, so by Lemma C `L` contains a 4-card match. ∎

This corollary is the strongest match-guarantee statement the math currently supports. It motivates the recommendation in `PLAN.md` to change the layout size from `L = 9` to `L = 10`.

---

## 7. Endgame analysis

### 7.1 Lemma E — the residual 8 cards always XOR to 0

**Claim.** Suppose play proceeds from the full deck `D` (|D| = 64) by repeatedly removing 4-card matches. Whenever the deck is exhausted with 8 cards remaining on the table — call this set `R ⊆ D` — `Σ R = 0`.

**Proof.** Two ingredients.

(i) **`Σ D = 0`.** Each koi `i ∈ {0,...,6}` appears in exactly half of the 64 cards: in `C(6, 0) + C(6, 2) + C(6, 4) + C(6, 6) = 1 + 15 + 15 + 1 = 32` cards (the count of even-sized subsets of the other 6 koi makes an odd-sized set containing `i`). 32 is even, so the i-th coordinate of `Σ D` is 0 in F_2 for every `i`, giving `Σ D = 0`.

(ii) **XOR is conserved.** Each removed match `M_i` has `Σ M_i = 0`, so `Σ (D \ ⋃ M_i) = Σ D + Σ ⋃ M_i = 0 + 0 = 0` (in F_2 addition equals subtraction).

So `Σ R = 0`. ∎

In game terms: the residual 8 cards always have every koi appearing an even number of times — they always form a single 8-card match in the parity sense.

### 7.2 The splittability claim is empirically false ~50% of the time

The residual 8-card subset `R` with `Σ R = 0` is *intended* to split into two 4-card matches, but this does not follow from `Σ R = 0` alone.

**Witness 1 (still valid).** `S* = {e_0, e_1, ..., e_6, 𝟙}` (where `e_i = 1 << i` and `𝟙 = 127`). `Σ S* = (e_0 + ... + e_6) + 𝟙 = 𝟙 + 𝟙 = 0` ✓. Every 4-subset of `S*` is either four `e_i`'s (XOR weight 4, nonzero) or `𝟙` plus three `e_i`'s (XOR weight 4, nonzero). So `S*` is an 8-card match with no 4-card sub-match.

**Witness 2 (Mode A simulation).** 50,000 random-play trials produced **25,850 distinct unsplittable 8-card residuals** (~51.7%) — a vast family, not just the `S*` orbit. See `math/RESULTS.md` §3.

### 7.3 Empirical reachability under game flow

Under Mode B simulation with `L = 10` (the only L-value that avoids mid-game stalls), 47.4% of residuals are unsplittable across 20,000 trials (`math/RESULTS.md` §2). This rate is essentially the same as the abstract Mode A rate (51.7%), so the layout-based game-flow constraint does not significantly bias residuals away from the unsplittable region.

The original endgame rule "claim one 4-card match → claim both" is therefore unworkable as stated: it would silently fail in roughly half of all games. `PLAN.md` Phase 3 has been updated with a revised endgame structure that does not depend on the splittability claim.

### 7.4 Verification status (computational)

`math/verify.py` implements three checks. Status:

1. **Sanity asserts** for `Σ D = 0` and the `S*` properties — pass on every run.
2. **Mode A** (random match removal from the whole remaining deck): done at 50k trials, see `math/RESULTS.md` §3.
3. **Mode B** (L-card layout with replenishment): swept over `L ∈ {8, 9, 10}` at 20k trials each, see `math/RESULTS.md` §2.

The two open computational items not yet implemented:

* **Formal proof of `max Sidon ≤ 9` in `D`.** Exhaustive DFS times out under naive pruning. Promising approaches: (a) symmetry breaking under `S_7` orbits of weight-3/weight-5 vectors; (b) SAT or ILP; (c) connection to caps in projective geometry over F_2.
* **Characterization of unsplittable residuals.** All 25k+ unsplittable residuals seen are 8-element strict-Sidon sets. Determining the structure (and count) of these maximal-by-XOR-zero Sidon octets would let us tune the endgame rule precisely (e.g., constructing the deck or the replenishment so that unsplittable residuals are unreachable).

---

## 8. Implications for game design

* The 4-card guarantee fails at `L = 9` (Theorem in §6). The minimum layout size that *does* guarantee a 4-card match is `L = 10` (corollary in §6, conditional on the empirical `max Sidon = 9`). `PLAN.md` Phase 0 / Phase 2 must change accordingly.
* The XOR-to-zero invariant for the 8-card residual (§7.1) is unconditional and gives the endgame whatever structural cleanliness it has. But the residual fails to split into two 4-card pieces about half the time, so any rule that *requires* such a split must be replaced.
* Two currently-on-the-table fixes for the endgame:
  1. Restructure the endgame as continued real-time play on the residual (claim 4-card matches as long as any exist; un-claimable cards either go to the leader or are split). Preserves the matching-game pacing and doesn't lean on a false theorem.
  2. Keep the `PLAN.md` Phase 3 fallback rule (60-second silence → award residual to the player with the most recent mid-game claim) and accept that ~50% of games end via the fallback. This is design-feasible but feels unsatisfying.
* The fact that the deck has so many maximal Sidon-sized residuals suggests the math is essentially "noisy" near 8 cards. If the game is to have a clean endgame *theorem*, the deck size or composition probably needs to change (e.g., dropping a small number of cards to make the max Sidon drop to 7, which would force every 8-card residual to split).
