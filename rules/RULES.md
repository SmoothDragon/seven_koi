# Koi — rules (v0.2)

These rules describe the **base game** (six breeds, 32 cards). An optional **Koi** expansion draft (seven species, 64 cards, different `L₀`) lives in [`expansion/seven_koi/DECK_AND_RULES.md`](../expansion/seven_koi/DECK_AND_RULES.md).

Player-facing rules. The retail box contains **one** deck of **32** cards featuring **six breeds**. Card size: 2.5" × 3.5" (63 × 88 mm), same idea as Magic-style poker cards.

**Six breeds** (order 1–6 on card badges): Kohaku, Showa, Asagi, Ogon, Chagoi, Tancho — see [koi_selection.md](../koi_selection.md) for full names and art notes.

---

## 1. What’s in the box

One deck of **32** koi cards:

- **6** single-koi cards (one featured koi each)  
- **20** triple-koi cards (every combination of three of the six)  
- **6** quintuple-koi cards (every combination of five of the six)

There is **no** “all six at once” card: the deck lists only **odd-sized** subsets (1, 3, or 5 koi per card), which is what makes the XOR match math work.

**Rulebook** (this booklet or equivalent), **tuck box** (or small two-piece box), and any campaign extras listed on your pledge (score pad, tokens, etc.) if included.

---

## 2. Goal

You are all koi collectors with an odd quirk: you only collect pairs of identical koi. Unfortunately, you are also buying from koi owners with a different odd quirk: they only sell an odd number of distinct koi at a time.

The cards represent various groups of koi available and they will be dealt into a tableau in the center accessible to all players. Groups of koi will be collected by players each turn and then the center tableau will be replenished.

The winner is the player that finished with the most koi.

Score **koi (fish)**. Each card shows some of the six breeds. When you claim a valid **match** (see below), you take those four cards. Only fish on cards **you claimed** count at the end. The tableau does **not** score.

---

## 3. Claiming koi

The quirks of the collectors and owners means that at least four cards must be claimed simultaneously in what is called a **match** (see notes at end for a precise definition).

A **match** is always **four different face-up cards** such that **every koi** appears on **0, 2, or 4** of them (never 1 or 3).

Fewer than four cards can never form a match.  
Matches of more than four cards are not allowed.

---

## 4. Playing your first game

Shuffle the **32** cards and deal **8** face up in the center (`L₀ = 8`; see section 5).

Everyone plays at once.

1. When you see a match, shout **“Koi!”** first, then **touch the four cards in order** (the shout marks who got there first if two players collide).
2. Play pauses. The group checks the four cards: every koi appears **0, 2, or 4** times across them.
   - **Valid:** that player takes all four cards, then you replenish the stock in the center to **8** cards whenever the deck still has stock.
   - **Invalid:** **invalid-claim penalty** — that player is **locked out** (cannot call “Koi!” or claim) until **another** player successfully claims **any** valid four-card match. They keep cards they already took earlier.
3. Continue until everyone agrees there are no more matches after the endgame sweep (section 6).

*(Optional later edition: worked examples with diagrams.)*

---

## 5. Table size and dealing

**Baseline face-up count `L₀`:** **`8`** for the 32-card deck.

**Setup:** shuffle all **32** cards, then deal `L₀` face up to the **tableau**; the rest are the face-down **stock**.

**After each valid claim:** remove the four scored cards to the claimant’s pile. Draw from the stock until the tableau again has `L₀` face-up cards, **or** the stock is empty (partial refill is OK).

**No mid-game stock flip on “stuck”:** With `L₀` face-up cards from this deck in play, a legal four-card match **always exists** somewhere on the tableau. There is **no** rule to add a card from stock because everyone thinks there is no match — if the table agrees there is no match, **keep looking**; someone missed one.

---

## 6. End of the deck (endgame)

When a refill would draw from an **empty** stock:

1. Flip **every** remaining face-down card onto the tableau in **one go** (bulk reveal). The tableau may be larger or smaller than `L₀`; that is fine. Nothing stays hidden in the stock.
2. Keep playing: anyone who spots a valid four-card match may still shout **“Koi!”** and claim it.
3. When **everyone agrees** there is **no** legal match left on the tableau, the game **ends**. Cards left on the tableau score for **no one**.

**Note:** the last face-up cards always satisfy a global parity condition (every koi appears evenly often across them), but they do **not** always split into two separate four-card matches. Do not assume “two clean piles left” — just keep calling real matches until none remain.

---

## 7. Scoring

Add up **every koi depiction** on cards **you claimed**:

- Single-koi card → 1  
- Triple → 3  
- Quintuple → 5  

**Tiebreakers** (if fish totals tie): (1) most cards claimed, (2) most quintuple cards claimed, (3) among single-koi cards you claimed, prefer the highest **badge number** (6 … 1) as a last resort — adjust if you adopt a different convention.

---

## 8. Table talk and edge cases (suggestions)

- **Two “Koi!” at once:** table decides who was first; if unclear, use a quick random tie-break (e.g. rock-paper-scissors).
- **Mixed skill:** optional house rule — strong players wait N seconds before each new tableau so newer players can scan.
- **Mis-deal:** fix counts before play; if a card is seen during the fix, reshuffle that portion if the group agrees.

---

## 9. Optional variants (not required for the main game)

Solitaire drills, timed rounds, or other modes are house experiments unless published separately.

---

# Math commentary

If you treat each card as the set of koi printed on it, the four sets XOR-cancel in the usual parity sense (same formal condition as in the project math notes). The published deck is the **odd-weight** vectors in **GF(2)⁶**; formal non-stall guarantees at **`L₀ = 8`** are certified in-repo (`math/explore_sidon_odd_restricted`, `--prove-odd-n 6`). The optional seven-species **Koi** expansion deck is the odd-weight slice in **GF(2)⁷** at **`L₀ = 10`** (`--prove-odd-n 7`); see `expansion/seven_koi/DECK_AND_RULES.md`.

## Document history

- **v0.1** — First consolidated rulebook draft from `PLAN.md` Phase 3 and `CLAUDE.md`. Standard / Expert naming; fixed `L₀`; no mid-game escalation; consensus endgame.
- **v0.2** — **Retail alignment:** single **32-card** deck, **six** koi; removed Expert / omitted-koi setup; scoring without an “all koi” card; `L₀ = 8` only.
