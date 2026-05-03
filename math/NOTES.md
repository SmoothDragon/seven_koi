# math/NOTES.md — Seven Koi: proof of the 4-card guarantee

This note proves the central mathematical claim that makes Seven Koi work: any layout of 9 cards from the 64-card deck contains a 4-card *match*. It is a writeup of the argument summarized at <https://chatgpt.com/share/69f67dcc-d818-832f-80a4-bb5e0c37e963> ("Subset sum to zero"), specialized to our deck and made self-contained.

Conventions: `+` denotes XOR (addition in F_2). `wt(v)` is the Hamming weight of `v`. The 7 koi are indexed 1..7 and a card is the bit vector `v ∈ F_2^7` whose i-th bit is 1 iff koi i appears on the card.

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

A **match** is a non-empty subset `M ⊆ D` with `Σ_{v∈M} v = 0` — equivalently, every koi appears an even number of times across the cards in `M`.

---

## 2. Lemma A — every match has even size

**Claim.** If `M ⊆ D` is non-empty and `Σ_{v∈M} v = 0`, then `|M|` is even.

**Proof.** For any `v ∈ D`, `wt(v)` is odd, so the parity bit `wt(v) mod 2` equals 1. Summing over `M` in F_2:

```
0 = wt(Σ v) ≡ Σ wt(v) ≡ |M| (mod 2)
```

so `|M|` is even. ∎

Combined with the fact that the deck has no duplicate cards (so no 2-element match exists), the smallest possible match has size 4.

---

## 3. Lemma B — Sidon reduction

**Definition.** A set `S ⊆ F_2^k` is a **Sidon set** if it satisfies:

* (a) `0 ∉ S`,
* (b) elements of `S` are distinct,
* (c) **no Schur triple**: for all distinct `a, b, c ∈ S`, `a + b ≠ c`,
* (d) **no 4-cycle**: for all distinct `a, b, c, d ∈ S`, `a + b ≠ c + d`.

**Claim.** A set `S ⊆ F_2^k` contains no non-empty subset of size ≤ 4 summing to 0 iff `S` is a Sidon set.

**Proof.** Each forbidden zero-sum corresponds directly to a violated condition:

* size 1: `v = 0` ⟺ violates (a),
* size 2: `v + w = 0` with `v ≠ w` impossible in F_2; equality `v = w` violates (b),
* size 3: `a + b + c = 0` ⟺ `a + b = c`, violating (c),
* size 4: `a + b + c + d = 0` ⟺ `a + b = c + d`. If `{a,b}` and `{c,d}` overlap in one element, the equation forces a duplicate (violates (b)); if disjoint, it violates (d).

Conversely each violation gives a zero-sum of the corresponding size. ∎

In F_2 this *is* the right notion of Sidon set: a 4-cycle `a+b = c+d` with disjoint pairs is exactly a 4-element zero sum.

---

## 4. Lemma C — for our deck, Sidon = "no 4-cycle"

**Claim.** Every subset `S ⊆ D` automatically satisfies (a), (b), (c). So `S` is Sidon iff `S` contains no 4-cycle iff `S` contains no 4-card match.

**Proof.**

* (a) `0 ∉ D` because `wt(0) = 0` is even.
* (b) The deck `D` consists of distinct vectors by construction.
* (c) For distinct `a, b, c ∈ D`, the sum `a + b + c` has parity `1 + 1 + 1 = 1 (mod 2)`, so `wt(a + b + c)` is odd, hence nonzero. So `a + b ≠ c`.

Therefore in our setting "Sidon" reduces to condition (d) alone. ∎

---

## 5. Lemma D — a maximal Sidon set of size 8

Let `e_i ∈ F_2^7` denote the i-th standard basis vector (the single-koi card for koi i), and let `𝟙 = 1111111 ∈ F_2^7` denote the all-ones (all-seven) card.

**Claim.** The set

```
S* = {e_1, e_2, e_3, e_4, e_5, e_6, e_7, 𝟙}
```

is a Sidon set in `D` of size 8, and *no* odd-weight vector outside `S*` can be added without creating a 4-cycle (so `S*` is maximal under extension).

**Proof.** First, `S* ⊂ D` (each element has weight 1 or 7, both odd) and `|S*| = 8`. To see `S*` is Sidon, use Lemma C: we just need to check no 4-cycle. The pairwise sums are:

* `e_i + e_j` for `1 ≤ i < j ≤ 7`: these are exactly the 21 weight-2 vectors of F_2^7 — all distinct.
* `𝟙 + e_i` for `i = 1, ..., 7`: these are the 7 weight-6 vectors of F_2^7 — all distinct from each other and from the weight-2 vectors above.

So the C(8, 2) = 28 pairwise sums are all distinct, meaning no `a + b = c + d` with `{a,b} ≠ {c,d}`. So `S*` is a Sidon set.

For maximality, take any `v ∈ D \ S*`. Then `wt(v) ∈ {3, 5}` (the weight-1 and weight-7 vectors are already in `S*`).

* If `wt(v) = 3`, write `v = e_i + e_j + e_k`. Then `{v, e_i, e_j, e_k} ⊆ S* ∪ {v}` is a 4-card match: `v + e_i + e_j + e_k = 0`.
* If `wt(v) = 5`, then `𝟙 + v` has weight 2, so `𝟙 + v = e_i + e_j` for some pair `i, j`. Rearranging: `v + 𝟙 + e_i + e_j = 0`. So `{v, 𝟙, e_i, e_j} ⊆ S* ∪ {v}` is a 4-card match.

In either case `S* ∪ {v}` is no longer Sidon. ∎

This shows the lower bound `max{|S| : S ⊆ D Sidon} ≥ 8` is achieved, and hints — by exhausting the natural extension candidates — that the maximum is exactly 8.

---

## 6. Theorem — the 4-card guarantee

**Theorem.** Any 9-card subset `L ⊆ D` contains a 4-card match.

**Proof.** By Lemma C, it suffices to show that `L` is *not* a Sidon set, i.e., some 4 cards in `L` form a 4-cycle.

By the classical bound on Sidon sets in `F_2^k` (see ChatGPT writeup linked above and the references therein), the maximum size of a Sidon set in `F_2^7` is `2^⌊7/2⌋ = 8`. Lemma D exhibits a witness achieving 8, confirming the bound is tight at our specific dimension.

Since `|L| = 9 > 8`, `L` cannot be Sidon, so it contains a 4-cycle, which by Lemma C is a 4-card match. ∎

**Remark on the upper bound.** The classical bound `max Sidon ≤ 2^⌊k/2⌋` is non-trivial and not implied by the elementary counting bound `C(|S|, 2) ≤ 2^k - 1` (which only gives `|S| ≤ 16` for `k = 7`). It holds at `k = 7`; it is *not* a universal identity for every small `k` (for example, `F_2^3` admits a Sidon set of size 3 = `{e_1, e_2, e_3}`, exceeding `2^⌊3/2⌋ = 2`). For our application we only need the case `k = 7`, which the cited reference establishes and which `math/verify.py` will confirm computationally.

---

## 7. The endgame: what is and isn't proven

### 7.1 Lemma E — the residual 8 cards always XOR to 0

**Claim.** Suppose play proceeds from the full deck `D` (|D| = 64) by repeatedly removing 4-card matches (each match is some `M_i ⊆ D` with `Σ M_i = 0` and `|M_i| = 4`). When the deck is exhausted, exactly 8 cards remain on the table (assuming a dealing convention where this is the case — see `PLAN.md` Phase 2). Call this set `R ⊆ D`. Then `Σ R = 0`.

**Proof.** Two ingredients.

(i) `Σ D = 0`. Each koi `i ∈ {1,...,7}` appears in exactly half of the 64 cards: it appears in `C(6, 0) + C(6, 2) + C(6, 4) + C(6, 6) = 1 + 15 + 15 + 1 = 32` cards (the count of even-sized subsets of the other 6 koi added to the singleton `{i}` makes an odd-sized set containing `i`). 32 is even, so the i-th coordinate of `Σ D` is 0 in F_2. This holds for every `i`, so `Σ D = 0`.

(ii) Each removed match `M_i` has `Σ M_i = 0`, so `Σ (D \ ⋃ M_i) = Σ D + Σ ⋃ M_i = 0 + 0 = 0` (in F_2, addition and subtraction coincide).

So `Σ R = 0`. ∎

In game terms: the residual 8 cards always have every koi appearing an even number of times — they are themselves a single 8-card match. The endgame rule "claim one 4-card group → claim both" is grounded in the *intent* that this 8-card match further splits into two 4-card pieces. §7.2 shows the splitting is *not* automatic from `Σ R = 0` alone.

### 7.2 The splittability claim is *not* a theorem of `Σ R = 0` alone

**Claim (negative).** There exists an 8-element subset `R ⊆ D` with `Σ R = 0` and *no* 4-card sub-match.

**Witness.** The maximal Sidon set from Lemma D, `S* = {e_1, ..., e_7, 𝟙}`.

* `Σ S* = (e_1 + ... + e_7) + 𝟙 = 𝟙 + 𝟙 = 0`. ✓
* Every 4-subset of `S*` is one of:
  - 4 distinct `e_i` vectors → XOR has weight 4, nonzero;
  - `𝟙` plus 3 distinct `e_i` vectors → XOR has weight 7 − 3 = 4, nonzero.
* So `S*` is an 8-card match with no 4-card sub-match. ∎

### 7.3 The remaining open question

The negative claim in §7.2 *only* says `S*` exists abstractly as an 8-element subset of `D`. It does **not** say `S*` is reachable as a residual `R` of an actual game. Reachability requires:

> The 56 cards `D \ S*` can be partitioned into 14 four-card matches `M_1, ..., M_14`, where the i-th match was claimable from the 9-card layout present at step i (so each `M_i` is a 4-element zero-sum subset of the live layout, and the sequence respects the dealing rule).

This is a strictly stronger condition than abstract partitionability of `D \ S*`. Settling reachability either way is the second computational task in §7.4. If no unsplittable residual is reachable, the rule "claim one 4-card group → claim both" is sound. Otherwise the rules need the fallback in `PLAN.md` Phase 3.

### 7.4 Independent verification (planned)

The Phase 2 deliverable `math/verify.py` provides three computational checks:

1. **Sidon enumeration.** Depth-first branch-and-bound over the 64 odd-weight vectors of `F_2^7`, extending only when the next vector creates no 4-cycle with the current set. Confirm no leaf reaches size 9. (Backstop for §6.) Estimated runtime: seconds.
2. **Static splittability.** Enumerate all 8-element subsets `R ⊆ D` with `Σ R = 0` and check how many fail to partition into two 4-card matches. We expect at least the `S*` orbit (under the symmetric group `S_7` permuting the 7 koi indices). Quantifying this set bounds the worst case.
3. **Endgame reachability.** Simulate game play under the chosen dealing convention with adversarial match selection: at each step, given the current layout and deck, branch over all valid 4-card matches in the layout. Check whether any leaf produces a residual `R` that fails check 2. If yes, the fallback rule below is *necessary*; if no (no unsplittable residual is reachable), the rule "claim one → claim both" is sound and we can promote it to a theorem. Tractability depends on the dealing convention; for `L = 8`, the search tree may be large but is bounded by `64! / (4!)^16 ≈ ...`-style figures, with heavy pruning available via symmetry and dominated-state detection.

---

## 8. Implications for game design

* The 4-card guarantee (§6) underwrites the core gameplay loop: a player can always find a match in any 9-card layout, so the game never stalls mid-deck.
* The XOR-to-zero invariant (§7.1) is unconditional and gives the endgame its structural cleanliness: the residual is always an 8-card match. The further claim that it splits into two 4-card matches is not yet proven — see §7.3.
* **Fallback rule for the rules document**: if the residual contains no 4-card match (i.e. it is `S*` or a similar maximal-Sidon residual), no player can call "Koi!" on the residual. The rules must specify what happens in this case. The current Phase 3 decision: the player who claimed the last *mid-game* match is awarded the entire residual as a single 8-card match. This makes the last mid-game claim slightly more valuable in expectation, which is acceptable design and avoids a stalled endgame.
* The maximal Sidon set `S*` is also the "hardest" 8-card snapshot tactically — if any 8-card layout reduces to exactly `S*`, no 4-card match exists. This is the same configuration that powers both the upper bound in §6 and the counterexample in §7.2.
* Because Lemma A forces every match to have even size, the 9-card layout never contains a "trivial" 2-card match, and matches of size 6 or 8 are also possible. The current rules restrict claims to size 4 only; this should be re-examined in playtest.
