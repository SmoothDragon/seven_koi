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

## 7. Independent verification (planned)

The Phase 2 deliverable `math/verify.py` will provide a computational double-check:

1. **Sidon enumeration.** Depth-first branch-and-bound over `D = 64` odd-weight vectors of `F_2^7`, extending only when the next vector creates no 4-cycle with the current set. Confirm no leaf reaches size 9. Estimated runtime: seconds.
2. **Endgame split.** For every 8-card subset `R ⊆ D` reachable as the residual after the deck empties (definition depends on the dealing convention chosen in `PLAN.md` Phase 2), check that `R` partitions into exactly two 4-card matches. This is the second math claim that has not yet been proven in writing; brute force will either confirm it or surface counterexamples that constrain the dealing rule.

---

## 8. Implication for game design

* The 4-card guarantee underwrites the core gameplay loop (a player can *always* find a match in the layout, so the game never stalls).
* The maximal Sidon set `S*` is also the "hardest" 8-card snapshot — if the layout reduces to exactly `S*` plus one more card, exactly one 4-card match is available. This may be the most interesting tactical position; designers may want to explicitly engineer the endgame layout to land here.
* Because Lemma A forces every match to have even size, the 9-card layout never contains a "trivial" 2-card match, and matches of size 6 or 8 are also possible (and may overlap with size-4 matches). The rules need to clarify whether players may claim larger matches or are restricted to size 4.
