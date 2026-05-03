# math/NOTES.md — Seven Koi: math claims, status, and proofs

This note tracks the central mathematical claims behind Seven Koi, what is proven, what was disproven by simulation, and what remains open. **Two of the original spec's claims have been falsified by the Monte Carlo in `math/RESULTS.md`** — the headline change is summarized in §0 and propagated through the rest of this document.

A previous version of this note attempted to prove the original spec by citing a closed-form bound on Sidon sets in `F_2^k` (`max ≤ 2^⌊k/2⌋`). That bound is incorrect at `k = 7` for our setting (and arguably for the full vector space too — see `math/RESULTS.md` §1.2). The proof is rebuilt below from first principles.

**References — literature.** For sharp discussion of Sidon sets in `F_2^t`, sum-free Sidon sets, their connection to binary linear codes of minimum distance ≥ 5, improved upper bounds on `s_max(F_2^t)`, and maximal Sidon sets in small dimensions, see Czerwinski–Pott [CP24]. Tabulated certified maxima **`s_max(GF(2)^6) = 9`**, **`s_max(GF(2)^7) = 12`** (sequence values **`a(6)`**, **`a(7)`**) appear as [OEISA394031]; the OEIS entry cites [CP24] **Proposition 2.7** and **Table 2** (`s_max`), also **Proposition 2.8** for **`n = 7`**. Full bibliographic data is in References at the end of this file.

Conventions: `+` denotes XOR (addition in F_2). `wt(v)` is the Hamming weight of `v`. The 7 koi are indexed 0..6 and a card is the bit vector `v ∈ F_2^7` whose i-th bit is 1 iff koi i appears on the card.

---

## 0. Headline status

| Claim                                                                                         | Status                                       |
|-----------------------------------------------------------------------------------------------|----------------------------------------------|
| Deck is the 64 odd-weight vectors of F_2^7.                                                   | **Trivially true** (§1).                     |
| Minimum match size = 4.                                                                       | **Proven** (§2 Lemma A).                     |
| Match-finding reduces to a 4-cycle / Sidon condition.                                         | **Proven** (§3–§4 Lemmas B, C).              |
| **`s_max(GF(2)^6) = 9`**, **`s_max(GF(2)^7) = 12`** (largest Sidon subset of the full additive group **`GF(2)^n`**).              | **Certified** [OEISA394031]; values recorded in [CP24] (**Proposition 2.7** / **Table 2**, and **Proposition 2.8** for **`n = 7`**). |
| Any **10** distinct vectors in **`GF(2)^6`** contain four summing to **0**.                     | **Proven** via **`|L| > a(6)`** (§6 Corollary, ambient **`GF(2)^6`**). |
| Any **13** distinct vectors in **`GF(2)^7`** contain four summing to **0**.                     | **Proven** via **`|L| > a(7)`** (§6 Corollary, ambient **`GF(2)^7`**). |
| Maximal Sidon cardinality **inside** the odd deck **`D`** (same as **`s_max(O_7)`** on nonzero odd-weight masks). | Lemma D constructs **`|S|=9`**. **`s_max(D) ≤ s_max(GF(2)^7)=12`** is trivial containment. Exhaustive search (**`math/explore_sidon_odd_restricted`**, **`--prove-odd-n 7`**) certifies **`s_max(D)=s_max(O_7)=9`**. |
| Any **10** distinct cards drawn only from **`D`** contain a **4‑card match**.                     | **Proven** (**§6 Corollary**) from **`s_max(D)=9`**. Sharper than ambient **`GF(2)^7`**, where **10‑tuples can still be Sidon** (`a(7)=12`, so **`|L|=10`** is below the **`13`** threshold). |
| Any **8** distinct cards drawn only from the **Standard** six-koi deck (**`|D| = 32`**, odd-weight nonzero vectors in **`F_2^6`** for the six active species) contain a **4‑card match**. | **Proven** from **`s_max(O_6)=7`** (**`math/explore_sidon_odd_restricted`**, **`--prove-odd-n 6`**). **`L₀ = 8`** Standard. |
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

**Remark (ambient vs odd slice).** Czerwinski–Pott [CP24], recorded as **[OEISA394031]**, certify **`s_max(GF(2)^6) = a(6) = 9`** and **`s_max(GF(2)^7) = a(7) = 12`**. Combined with §6 Corollary **(ambient)** this gives **`|L| ≥ 10`** in **`GF(2)^6`** and **`|L| ≥ 13`** in **`GF(2)^7`** for **four distinct XOR-zero summands** among **arbitrary** vectors in the full space. Inside the **odd** deck **`D ⊂ GF(2)^7`**, Lemma D gives **`s_max(D) ≥ 9`**; exhaustive search in **`math/explore_sidon_odd_restricted`** (**`--prove-odd-n 7`**) certifies **`s_max(D) = s_max(O_7) = 9`**, so **`|L| = 10`** on **`D`** always forces a **4-card match** (§6 Corollary, unconditional). The six-koi Standard slice satisfies **`s_max(O_6)=7`** (**`--prove-odd-n 6`**), so **`|L| = 8`** there always forces a match.

---

## 6. Theorem — the (corrected) match guarantee

**Theorem.** A 9-card layout *can* fail to contain a 4-card match. Specifically, the set `S₉` from Lemma D is itself a 9-card layout with no 4-card sub-match.

**Proof.** By Lemma D, `S₉` is a strict Sidon set, equivalently (by Lemma C) it contains no 4-card match. ∎

**Corollary (ambient groups — OEIS [A394031](https://oeis.org/A394031) / [CP24]).** Let **`a(n)`** denote the maximum size of a Sidon subset of **`GF(2)^n`**, sequence **[A394031](https://oeis.org/A394031)**. **[OEISA394031]** states the operative characterization inside **`GF(2)^n`**: a finite set **`S`** is Sidon iff there are **no** four distinct elements whose XOR totals the identity **0**. Hence any **`L ⊆ GF(2)^n`** with **`|L| > a(n)`** cannot be Sidon, so **`L`** harbors four distinct XOR‑zero summands (equivalently a Seven Koi **4**‑card match whenever those vectors are legal cards). **[CP24]** certify **`a(6)=9`**, **`a(7)=12`**, yielding **`|L| ≥ 10`** in **`GF(2)^6`** and **`|L| ≥ 13`** in **`GF(2)^7`**.

**Corollary (restricted deck `D`).** If **`s_max(D)=9`**, every **10**‑card **`L ⊆ D`** contains a **4**‑card match.

**Proof.** Suppose toward a contradiction that **`L`** admits **no** four distinct XOR-zero cards. Lemma C ⇒ **`L`** is Sidon-as-a-subset-of-**`D`**. But **`s_max(D)=9`** forbids **`|L| = 10`**. Hence **`L`** **does** admit such a cancelling quadruple — a legal **4**‑card match for Seven Koi. ∎

Published dealing (**`PLAN.md`**, **`CLAUDE.md`**) uses **fixed** **`L₀ = 10`** (Expert, seven koi) and **`L₀ = 8`** (Standard, six koi) with **no** mid-game stock escalation: **`s_max(O_7)=9`** and **`s_max(O_6)=7`** on the odd slices are **exhaustively certified** in **`math/explore_sidon_odd_restricted`**, so every **`L₀`**-card layout from the legal deck contains a **4-card match**. **[CP24]** / ambient thresholds **`|L| ≥ 13`** (**`GF(2)^7`**) and **`|L| ≥ 10`** (**`GF(2)^6`**) remain **literature context** for arbitrary vectors in the full space. Mode B simulation (**`math/layout_stall_sweep.py`**, **`math/RESULTS.md`**) still documents mid-game stalls at smaller **`L`** (e.g. **`L = 7`** on six koi).

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

Open items:

* **`s_max(D) ≤ 9`** is **settled computationally** in-repo (**`math/explore_sidon_odd_restricted`**, **`--prove-odd-n 7`**). A short human proof or independent verification run remains optional polish.
* **Characterization of unsplittable residuals.** All 25k+ unsplittable residuals seen are 8-element strict-Sidon sets. Determining the structure (and count) of these maximal-by-XOR-zero Sidon octets would let us tune the endgame rule precisely (e.g., constructing the deck or the replenishment so that unsplittable residuals are unreachable).

---

## 8. Implications for game design

* **Layout cardinality.** Lemma D / Theorem **`S₉`** persists: nine face‑up cards from **`D`** can deadlock. Exhaustive **`s_max(O_7)=9`** / **`s_max(O_6)=7`** (**`math/explore_sidon_odd_restricted`**) makes **`L₀ = 10`** (Expert) and **`L₀ = 8`** (Standard) **sufficient** for a **visible 4-match** whenever the tableau is exactly **`L₀`** cards from the legal deck — **`PLAN.md`** / **`CLAUDE.md`** now ship **fixed `L₀`** with **no** mid-game escalation. **[OEISA394031]** (per **[CP24]** Table 2) still records ambient **`s_max(GF(2)^6)=9`**, **`s_max(GF(2)^7)=12`** for **arbitrary** nonzero vectors (**§6** Ambient Corollary).
* **Residual XOR** (**§7.1**) is unconditional whenever the tableau drains properly, yet ~half of exhausted layouts still dodge tidy **two‑claim** endings (**§7.2–7.3**). Rules insisting on stacking two auto‑matches stay invalid.
* Two archived endgame salvage ideas (**now largely superseded** by unanimous consensus stop in **`PLAN.md`** Phase 0): (1) keep hunting matches until brute exhaustion rather than insisting on phantom double claims; (2) optional timed silence adjudication if a group rejects consensus flow.
* The fact that the deck has so many maximal Sidon-sized residuals suggests the math is essentially "noisy" near 8 cards. If the game is to have a clean endgame *theorem*, the deck size or composition probably needs to change (e.g., dropping a small number of cards to make the max Sidon drop to 7, which would force every 8-card residual to split).

---

## References

[OEISA394031] OEIS sequence [A394031](https://oeis.org/A394031): *Maximum size of a subset of **`GF(2)^n`** being a Sidon set* (`a(6)=9`, `a(7)=12` in **[CP24]** notation). Maintainer entry by Aleksei Udovenko; cites **[CP24]** Props. 2.7–2.8 / Table 2.

[CP24] Ingo Czerwinski and Alexander Pott, *Sidon sets, sum-free sets and linear codes*, **Advances in Mathematics of Communications** 18 (2024), no. 2, 549–566. DOI: [10.3934/amc.2023054](https://doi.org/10.3934/amc.2023054). Preprint: [arXiv:2304.07906](https://arxiv.org/abs/2304.07906).

Contains, among other results: the trivial upper bound on `s_max(F_2^t)` (their Proposition 2.1); improved bounds via non-existence of certain `[n, n−t, 5]` codes (Theorems 5.2–5.3); classification of maximal Sidon sets through dimension 6 (Proposition 2.7) and computer-assisted size data in dimensions 7–8 (Proposition 2.8); and the equivalence between sum-free Sidon subsets of `F_2^t \ {0}` and associated linear codes with minimum distance ≥ 5 (Proposition 4.1, Theorem 4.2). Our “no 4-card match among distinct cards” condition matches Sidon disjoint-pair collisions in characteristic 2; the odd-parity affine deck suppresses Schur triples relative to unrestricted `F_2^t` — see §§3–5 above.

TODO: Verify or create a new OEIS entry based on odd Sidon sets. What we have so far:
1 1
2 2
3 3
4 4
5 6
6 7
7 9
