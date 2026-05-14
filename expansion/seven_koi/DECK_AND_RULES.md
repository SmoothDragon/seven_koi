# Koi — deck composition and rules (seven-species expansion, designer draft)

**Status:** optional expansion / possible future SKU — **not** the default boxed game. For the shipping **six-breed, 32-card** product, see [rules/RULES.md](../../rules/RULES.md).

**Tone:** publish only if you intentionally add a **seven-breed** product lane; keep base **Koi** as the primary narrative and pledge structure.

---

## 1. Deck composition (64 cards)

Cards are labeled by **odd-sized** subsets of **seven** fixed breeds. Encode breeds as bits **1 … 7** (left → right in the corner glyph row). There is **one card per nonempty odd subset**, so:

| Card type | Count | Description |
|-----------|------:|---------------|
| Singles | **7** | `C(7,1)` — one breed each |
| Triples | **35** | `C(7,3)` — every set of three breeds |
| Quintuples | **21** | `C(7,5)` — every set of five breeds |
| **All-seven** | **1** | The unique card showing **all seven** breeds at once |
| **Total** | **64** | `7 + 35 + 21 + 1` |

**Breeds (draft roster, bit order):** Kohaku, Showa, Asagi, Ogon, Chagoi, Tancho, **Kumonryu** — the first six match [koi_selection.md](../../koi_selection.md); the seventh is the expansion-only breed. Art and Japanese naming for Kumonryu should follow the same style guide discipline as the base game once this SKU is green-lit.

**No “Standard-style omit-one-species” partition:** unlike older internal prototypes that split seven breeds into parallel sub-decks, this expansion draft assumes **every card uses the full seven-breed universe** as above.

---

## 2. Matches (same XOR logic as base **Koi**)

A **match** is **four distinct face-up cards** such that **every breed appears on 0, 2, or 4** of them (equivalently, the four subset vectors XOR to **0** in **`GF(2)^7`**). Fewer than four cards never qualify; more than four is not a single claim.

**Why only odd subset sizes on cards:** each card’s incidence vector has **odd** Hamming weight, so the smallest nonempty cancellation set has size **4** (not **2**, since there are no duplicate cards).

---

## 3. Table size and dealing

**Baseline face-up count `L₀`:** **`10`** for the **64-card** deck.

**Why 10:** exhaustive search on the odd-weight seven-bit slice certifies **`s_max(O_7) = 9`** (no 10-card layout is match-free for four-card XOR). Run `cargo run --release -- --prove-odd-n 7` in [`math/explore_sidon_odd_restricted`](../../math/explore_sidon_odd_restricted/). See [math/NOTES.md](../../math/NOTES.md) for the deck-local corollary.

**Setup:** shuffle all **64** cards; deal **`L₀`** face up to the **tableau**; remaining cards are the face-down **stock**.

**After each valid claim:** remove the four scored cards; replenish from stock until the tableau again has **`L₀`** face-up cards **or** the stock is empty (partial refill allowed).

**No mid-game escalation:** with **`L₀`** face-up cards drawn only from this deck, a legal four-card match **always exists** on the tableau. If the table agrees there is none, **keep scanning** — someone missed it.

---

## 4. Claim protocol

Same as base **Koi**: real-time scanning; shout **“Koi!”** then **touch the four cards in order**; invalid-claim penalty — caller locked out until **another** player successfully claims **any** valid four-card match.

---

## 5. Endgame (stock empty)

When a refill would draw from an **empty** stock:

1. Reveal **every** remaining facedown card onto the tableau in **one sweep** (bulk reveal). The tableau may hold fewer than **`L₀`** cards; that is fine.
2. Continue claiming valid four-card matches until **everyone agrees** none remain.
3. Tableau leftovers score for **no one**.

**Parity reminder:** leftover face-up cards still satisfy global even-parity across breeds ([math/NOTES.md](../../math/NOTES.md)), but they **need not** partition into two disjoint four-card matches ([math/RESULTS.md](../../math/RESULTS.md)).

---

## 6. Scoring

Add **fish / koi** = every breed depiction printed on cards **you claimed**:

| Card type | Fish per card |
|-----------|---------------:|
| Single | 1 |
| Triple | 3 |
| Quintuple | 5 |
| **All-seven** | **7** |

Tableau cards at game end score **nothing**.

---

## 7. Tiebreakers

If two or more players tie on **total fish**:

1. **Most cards claimed** (each claimed card counts once, regardless of type).
2. **Most quintuple** (five-breed) cards claimed.
3. **Most all-seven** cards claimed (**7-of-7** tie step — rewards holding the unique richest card).
4. **Single-card badge fallback:** among single-breed cards you claimed, prefer the highest **badge number** (**7 … 1**) as a last resort (mirror base-game **6 … 1** logic).

Adjust ordering only if blind playtests show a different incentive is clearer; document changes in this file.

---

## 8. Player count and variants

Suggested table size and etiquette mirror base **Koi** ([rules/RULES.md](../../rules/RULES.md) §8–9): e.g. simultaneous “Koi!” resolution, optional handicaps for mixed skill. Any **solitaire** or **timer** modes remain house rules unless published separately.

---

## 9. Production checklist (if this becomes real)

- Confirm art pipeline for **seven** masters + glyph row ([design/glyphs/seven_crests.svg](../../design/glyphs/seven_crests.svg) reference).
- Re-run or extend **`math/explore_sidon_odd_restricted`** / sims if card faces or `L₀` change.
- Update Kickstarter copy to label the **seven-species Koi** expansion explicitly as an **expansion** or **expert SKU**, not the default box.
