# Seven Koi — rules (v0.1)

Player-facing rules. The retail box contains **one** full card set (**Expert**, 64 cards, seven koi). **Standard** is the same physical cards, but you **use only half of them** (32 cards): set aside every card that depicts a chosen **omitted** koi, then play only with the remainder. Same flow for both modes unless noted. Card size: 2.5" × 3.5" (63 × 88 mm), same idea as Magic-style poker cards.

**Seven koi** (order 1–7 on card badges): Kohaku, Showa, Asagi, Ogon, Chagoi, Tancho, Kumonryu — see [koi_selection.md](../koi_selection.md) for full names and art notes.

---

## 1. What’s in the box

One deck of **64** koi cards containing:

- **7** single-koi cards (one featured koi each)  
- **35** triple-koi cards (every combination of three koi)  
- **21** quintuple-koi cards (every combination of five koi)  
- **1** all-seven card (all koi on one card)

**Rulebook** (this booklet or equivalent), **tuck box** (or small two-piece box), and any campaign extras listed on your pledge (score pad, tokens, etc.) if included.

*Standard mode does not add a second deck:* before Standard play, remove and set aside **all** cards that show the **omitted** koi (32 cards stay in play). The box or insert may show which koi to omit for the “house” Standard setup; otherwise the group agrees on one species before the first shuffle.

---

## 2. Goal

You are all koi collectors with an odd quirk: You only collect pairs of identical koi. Unfortunatley, you are also buying from koi owners with a different odd quirk: They only sell an odd number of distinct koi at a time.

The cards represent various groups of koi available and they will be dealt into a tableau in the center accessible to all players. Groups of koi will be collected by players each turn and then the center tableaux will be replenished.

The winner is the player that finished with the most koi.

Score **koi (fish)**. Each card shows some of the active koi. When you claim a valid **match** (see below), you take those four cards. Only fish on cards **you claimed** count at the end. The tableau does **not** score.

---

## 3. Claiming koi

The quirks of the collectors and owners means that at least four cards must be claimed simultaneously in what is called a **match** (See notes at end for detailed explanation).

A **match** is always **four different face-up cards** such that **every active koi** appears on **0, 2, or 4** of them (never 1 or 3). 

Fewer than four cards can never form a match.
Matches of more than four cards are not allowed.

---

## 4. Playing your first game

Set the 32 expert cards aside (TODO: make an easy way to do this).
Shuffle and deal 8 of the 32 remaining standard cards in the center of all the players.

Everyone plays at once.

1. When you see a match, shout **“Koi!”** first, then **touch the four cards in order** (the shout marks who got there first if two players collide).
2. Play pauses. The group checks the four cards: every active koi appears **0, 2, or 4** times across them.
   - **Valid:** that player takes all four cards, then you replenish the stock in the center to 8 cards.
   - **Invalid:** **invalid-claim penalty** — that player is **locked out** (cannot call “Koi!” or claim) until **another** player successfully claims **any** valid four-card match. They keep cards they already took earlier.
3. Continue until the deck is exhausted.
4. When the final eight cards are in the stock, it is guaranteed (for the standard deck) to have two matches. Whomever claims on match claims both.

TODO: Show a graphic with 8 enumerated cards on the table and then say which subset forms a match. Perhaps 2 or 3 examples. The first should be easiest with three single cards that match a triple and other random cards. Choose cards so there is also a different more difficult match to find. The final example should have only cards with 3 and 5 koi on them to show a more difficult case and then explain the matches below. Again all the examples should contain at least two matches.

---

## 5. Table size and dealing

**Baseline face-up count `L₀`** (restore toward this after each successful claim):

- **Standard:** `L₀ = 8`
- **Expert:** `L₀ = 10`

**Setup:** **Expert** — shuffle all **64** cards, then deal `L₀` face up to the **tableau**; the rest are the face-down **stock**. **Standard** — after setting aside the 32 cards that depict the omitted koi, shuffle the **32** remaining cards, then deal `L₀` and form the stock from those only.

**After each valid claim:** remove the four scored cards to the claimant’s pile. Draw from the stock until the tableau again has `L₀` face-up cards, **or** the stock is empty (partial refill is OK).

**No mid-game stock flip on “stuck”:** With `L₀` face-up cards from the **legal** pile in play (64-card Expert or 32-card Standard), a legal four-card match **always exists** somewhere on the tableau. There is **no** rule to add a card from stock because everyone thinks there is no match — if the table agrees there is no match, **keep looking**; someone missed one.

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
- All-seven (Expert) → **7**  

**Tiebreakers** (if fish totals tie): (1) most cards claimed, (2) most “all-koi” cards (all-seven vs all-six), (3) highest-weight single card among the active species (quint beats triple beats single).

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
If you treat each card as the set of koi printed on it, the four sets XOR-cancel in the usual parity sense (same formal condition as in the project math notes).

TODO: Add comment about Sidon sets.
TODO: Add comment about odd Sidon sets.
TODO: Possibly include a LEAN proof that odd Sidon set bounds are correct.
TODO: Math explanation of why the standard game always ends with 8 cards than can be split into two matches.

## Document history

- **v0.1** — First consolidated rulebook draft from [PLAN.md](../PLAN.md) Phase 3 and [CLAUDE.md](../CLAUDE.md). Standard / Expert naming; fixed `L₀`; no mid-game escalation; consensus endgame.
