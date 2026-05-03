# PLAN.md — Seven Koi: roadmap to publication

A phase-by-phase plan to take Seven Koi from its current state (a concept, a koi reference sheet, and a one-line README) to a publishable card game. Each phase lists concrete deliverables. Open decisions are listed in Phase 0 and recapped at the bottom.

For the current repo state and the verbatim game spec, see [CLAUDE.md](CLAUDE.md). For the koi reference, see [ThirteenKoi.png](ThirteenKoi.png).

---

## Phase 0 — Decisions to lock first

These block later phases. Make them before sinking time into art or production.

1. **Publication route** — print-on-demand, crowdfunding, pitch-to-publisher, or personal/hobby.
2. **Dealing-math reconciliation** — see Phase 2; the stated "9 out / 8 left" arithmetic does not close over a 64-card deck. Pick: initial layout of 8, initial layout of 12, or "stop replenishing once the deck is empty" with the residual handled explicitly.
3. ~~**Final 7-of-13 koi**~~ — **resolved** (see [koi_selection.md](koi_selection.md)): Kohaku, Showa, Asagi, Ogon, Chagoi, Tancho, Kumonryu.
4. ~~**Player count and turn structure**~~ — **resolved**:
   - Real-time call-out (everyone scans simultaneously; first to call a valid 4-card match collects it).
   - Call protocol: shout **"Koi!"** then touch the four cards in order.
   - Invalid-claim penalty: caller is locked out until the next valid 4-card match is claimed by another player (in mid-game this coincides with the next replenishment; in the endgame it's the moment another player claims one of the two 4-card groups).
   - Player count still TBD (see Phase 3).
5. **Art pipeline** — commissioned illustrator, DIY, or AI-generated.
6. **Digital prototype** — Tabletop Simulator mod, web prototype, or none.

---

## Phase 1 — Koi selection (7 of 13)

**Criteria** (in priority order):

1. Visually distinct dominant color/pattern at thumbnail size (the triple and quintuple cards will use small renderings).
2. Distinct silhouette / pattern density (so the corner glyph isn't the only differentiator).
3. Cultural recognizability — pick canonical varieties when possible.
4. Avoid near-duplicates (Asagi vs Shusui, Sanke vs Showa, Utsuri vs Utsurimono vs Bekko).

**Recommended 7** (max contrast, no near-duplicates, full hue spread):

| # | English   | Japanese (kanji / romaji) | Dominant look                          | Suggested primary hex |
|---|-----------|---------------------------|----------------------------------------|----------------------|
| 1 | Kohaku    | 紅白 / Kōhaku             | Red markings on white                  | `#D7263D`            |
| 2 | Showa     | 昭和三色 / Shōwa Sanshoku | Black-dominant tricolor (black/red/white) | `#1A1A1A`         |
| 3 | Asagi     | 浅黄 / Asagi              | Blue scaled net pattern                | `#2E6F95`            |
| 4 | Ogon      | 黄金 / Ōgon               | Solid metallic gold                    | `#E0B040`            |
| 5 | Chagoi    | 茶鯉 / Chagoi             | Solid brown                            | `#7B4B2A`            |
| 6 | Tancho    | 丹頂 / Tanchō             | White body, single red dot on head     | `#F5F5F0`            |
| 7 | Kumonryu  | 九紋竜 / Kumonryū         | Black-and-white sumi pattern           | `#2B2B2B`            |

**Dropped, with reason**: Shusui (too close to Asagi), Sanke (too close to Showa), Utsurimono / Utsuri / Bekko / Hariwake (cluster in black/yellow/white space; keeping all four hurts thumbnail readability).

**Deliverable**: [koi_selection.md](koi_selection.md) with the seven chosen koi, English + Japanese (kanji + romaji) names, a 1–2 sentence flavor blurb each, and the primary color hex above for use in card design. **Done.**

---

## Phase 2 — Mathematical verification (do before art)

Lock the math before committing to art, because if a claim is wrong the rules change.

- **Card structure**: confirm the 64 cards are exactly the odd-weight binary vectors of length 7. Counts: C(7,1) + C(7,3) + C(7,5) + C(7,7) = 7 + 35 + 21 + 1 = 64. ✓ (combinatorially trivial)
- **Match definition**: a "match" is a subset of cards whose bitwise XOR is the zero vector — equivalently, every koi appears an even number of times across the chosen cards.
- **Minimum match size = 4**: every card has odd Hamming weight; sum of an odd number of odd weights is odd, so the smallest non-empty subset that can sum to even-weight (and zero in particular) has size 2 or 4. Size 2 would require two identical cards, which is impossible in this deck — so the minimum non-trivial match is 4. ✓
- **4-card guarantee in any 9-card layout**: proven self-contained in [math/NOTES.md](math/NOTES.md), adapting the argument from <https://chatgpt.com/share/69f67dcc-d818-832f-80a4-bb5e0c37e963> ("Subset sum to zero"). Sketch:
  1. Reduce "no ≤4 zero-sum subset" to "Sidon set" (no duplicates, no Schur triples, no 4-cycles).
  2. For our deck, the Schur-triple condition is automatic (sum of three odd-weight vectors is odd, hence nonzero), so Sidon collapses to "no 4-cycle" = "no 4-card match".
  3. Cite the classical bound `max Sidon set in F_2^7 ≤ 2^⌊7/2⌋ = 8`.
  4. The natural set `{e_1, ..., e_7, 𝟙}` achieves 8 and is maximal (every extra weight-3 vector closes a triangle with three `e_i`'s; every extra weight-5 vector closes a 4-cycle with `𝟙` and the two `e_i`'s in its complement).
- **Endgame structure**:
  - **Proven** ([math/NOTES.md](math/NOTES.md) §7.1): the residual 8 cards always XOR to 0, i.e. form a single 8-card match. Follows from `Σ D = 0` (each koi appears in exactly 32 cards) and the conservation of XOR under match removal.
  - **Open**: whether the residual always further splits into *two* 4-card matches. This is **false** in general — `S* = {e_1, ..., e_7, 𝟙}` is an 8-card match with no 4-card sub-match (`math/NOTES.md` §7.2). The remaining question is whether `S*` (or any other unsplittable residual) is *reachable* under valid mid-game play (`math/NOTES.md` §7.3). Phase 2 brute-force will settle this; if no unsplittable residual is reachable, the rule "claim one 4-card group → claim both" promotes to a theorem; otherwise the fallback rule in Phase 3 is necessary.
- **Dealing arithmetic**. With initial layout L and final layout F, total cards passing through play satisfy `64 = L + 4M + F` where M is the number of mid-game matches. The user's stated `L = 9, F = 8` gives M = 11.75 (no integer solution). Resolutions:
  - **L = 8, F = 8** → M = 12. Cleanest; loses one card from initial spread.
  - **L = 12, F = 8** → M = 11. More cards visible from start (easier first match).
  - **L = 9, F = 8, deck empties mid-game** → after the deck runs out, claimed matches simply shrink the layout from 9 → 5 → ... etc. This is rule-elegant but the endgame is no longer guaranteed to be exactly 8 cards.
  - Pick one and update the rules document accordingly.

**Deliverables**:

- [math/NOTES.md](math/NOTES.md) — self-contained writeup of the 4-card-guarantee proof, the XOR-invariant endgame proof, and the `S*` counterexample. **Done.**
- `math/verify.py` — small Python script using `itertools` and bitmask XOR for three independent computational checks (see `math/NOTES.md` §7.4):
  - (a) **Sidon enumeration.** Confirm no Sidon set in odd-weight F_2^7 reaches size 9 (backstop for the cited classical bound).
  - (b) **Static splittability.** Enumerate all 8-element subsets `R ⊆ D` with `Σ R = 0`; report how many fail to split into two 4-card matches and characterize them (we expect at least the `S*` orbit under permutations of the 7 koi).
  - (c) **Endgame reachability.** Simulate game play under the chosen dealing convention with adversarial match selection; check whether any unsplittable residual is reachable. If no, promote the splittability claim to a theorem and remove the Phase 3 fallback rule. If yes, keep the fallback rule and document the reachable bad residuals.
  - Update `math/NOTES.md` §7.4 with the verification results, and add the chosen dealing convention to §1.

---

## Phase 3 — Rules document

- **Player count, age, time** — suggested 2–6 players, 10+, 15–25 min. Confirm via playtest.
- **Setup** — shuffle, deal initial layout (number set in Phase 2).
- **Turn structure** — **real-time call-out** (locked in Phase 0): all players scan the layout simultaneously; the first to call a valid 4-card match claims it. Fits the matching-game lineage (cf. *SET*).
- **Call protocol** (locked): the claiming player **shouts "Koi!" and then touches the four cards in order**. The shout is the time-stamp; the touches are the proof. Two players almost-tying is resolved by the shout, not by the touches.
- **Match claim resolution** — once "Koi!" is called, all play pauses; the caller touches four cards in order and the group verifies that each of the seven koi appears 0, 2, or 4 times across them. If valid: caller takes the four cards. If invalid: invalid-claim penalty applies.
- **Invalid-claim penalty** (locked): the caller is **locked out until the next 4-card match is claimed by someone else**. They keep all previously collected cards. In typical mid-game play, a successful match is followed by a 4-card replenishment, so the lockout ends as the new layout appears. In the endgame (deck empty, 8 cards on the table), the lockout still ends the moment another player claims one of the two 4-card groups — the locked-out player can then race for the remaining group. This is a soft penalty (no card loss) but a real tempo cost in a real-time game.
- **Scoring** — collected cards go face-up in front of the claimer; final score = total koi pips across collected cards.
- **Tiebreakers** — most cards collected, then most all-seven cards, then highest-weight single card.
- **Endgame** (locked):
  - When the deck is exhausted, exactly 8 cards remain on the table. By [math/NOTES.md](math/NOTES.md) §7.1 these always XOR to 0, i.e. form a single 8-card match.
  - **Claim one → claim both.** When any player calls "Koi!" on a 4-card match in the residual, they immediately claim **all 8** residual cards (the 4 they called plus the remaining 4, which are guaranteed to also XOR to 0 in the typical case). Game ends.
  - **Fallback for an unsplittable residual.** It is mathematically possible that the residual contains *no* 4-card sub-match (the witness is `S* = {e_1, ..., e_7, 𝟙}` from `math/NOTES.md` §7.2; whether this can actually occur during play is an open question scheduled for brute-force resolution in Phase 2). If, after a generous timer (e.g. 60 seconds with no successful claim), no player has called a 4-card match in the residual, the entire 8-card residual is awarded to **the player who claimed the most recent mid-game match**. Game ends.
  - This fallback is unattractive enough (it costs every other player the whole endgame) that players are incentivized to scan harder before the timer expires, while still guaranteeing the game terminates.
- **Mixed-skill handicap variant** — the rulebook should suggest a "house handicap" (e.g. faster players sit on their hands for the first N seconds of each layout) for mixed-skill groups, since real-time inherently penalizes slower scanners.
- **Edge cases** — simultaneous "Koi!" shouts (rule: nearest-shouter as judged by the table; fall back to rock-paper-scissors), accidental over/under-deal, mid-touch reveal of an obviously invalid match (caller still pays the penalty).
- **Variants**:
  - Solitaire/timed: how fast can you clear the deck?
  - Cooperative: find all matches in N seconds.
  - Teaching variant: play with only 5 koi (32 cards = odd-weight vectors of length 5; same math structure, smaller deck).

**Deliverable**: `rules/RULES.md` v0.1.

---

## Phase 4 — Card design (graphic design, not yet illustration)

- **Card spec** — 2.5" x 3.5" (63 x 88 mm), 3 mm bleed on every edge, 3 mm safe margin inside the trim, 300 DPI, CMYK, ICC profile per manufacturer.
- **Single-koi card layout** — large central illustration; English name top, Japanese name (kanji + romaji) bottom; koi-number badge (1–7) and corner indicator glyph.
- **Triple card layout** — three koi swimming inward in roughly a Reuleaux-triangle arrangement, each with a small badge for quick scanning.
- **Quintuple card layout** — five koi in a pentagonal/pentagram arrangement; consider a slight rotational offset so each koi remains identifiable.
- **All-seven card** — unique heptagonal/mandala arrangement.
- **Card back** — single shared design (water + seigaiha wave pattern).
- **Quick-ID system** — every card carries a row of seven small filled/unfilled circles in a corner (one per koi, filled = present). This is the visual analogue of the underlying bit vector and is the single most important playability decision: without it, scanning a 9-card layout for matches is brutal. The corner code is what lets players actually compute the XOR by eye.
- **Color palette** — derive accent colors from the seven primary hexes in Phase 1; pick a neutral background (off-white parchment or muted pond-water blue).
- **Typography** — pair a Latin serif/display font with a Japanese font supporting kanji (e.g. Noto Serif JP, Klee, or Yuji Syuku); confirm commercial-use license.

**Deliverable**: `design/templates/` with one InDesign / Affinity Publisher / SVG template per card type plus `design/style_guide.md` (palette, typography, glyph spec, bleed/safe diagrams).

---

## Phase 5 — Art production

- **Pipeline decision** — commissioned illustrator (best for IP-clean, highest cost), DIY (cheapest, slowest, requires skill), or AI-generated (fastest, lowest cost, IP/copyright caveats; see Phase 8).
- **Per-koi assets needed**:
  - Hero illustration: top-down view, consistent lighting and scale, transparent background, ~1500 x 3000 px.
  - Thumbnail version: same fish, simplified for triple/quintuple cards (~600 x 1200 px).
  - Corner glyph: tiny silhouette or filled circle in the koi's primary color.
- **Shared assets** — card-back pattern, box art, rulebook header art, optional score-pad art.
- **Consistency checklist** — every koi rendered at the same scale, same camera angle, same water-surface lighting, same stroke style.

**Deliverable**: `art/koi/{kohaku,showa,asagi,ogon,chagoi,tancho,kumonryu}.{png,svg}` (hero + thumbnail), `art/back.png`, `art/box/`, `art/glyphs/`.

---

## Phase 6 — Prototyping

- **v0 paper prototype** — print all 64 cards on cardstock at home, hand-cut, sleeve in penny sleeves with MTG cards as backers. Fastest playtest loop; usable within a day of finishing Phase 4 layouts.
- **v1 print-on-demand proof** — order one deck from [The Game Crafter](https://www.thegamecrafter.com/) or [MakePlayingCards](https://www.makeplayingcards.com/) (~$15–30 per deck). Tests tactile feel, color reproduction, and finish.
- **(Optional) Digital prototype** — a [Tabletop Simulator](https://www.tabletopsimulator.com/) workshop mod, or a small web app with a draggable 9-card spread and an "is this a match?" checker. Useful both for remote playtesting and as a marketing demo.

---

## Phase 7 — Playtesting

- **Internal playtests** (5–10 sessions) — designer plus friends, iterate freely.
- **Blind playtests** (≥5 sessions) — hand a stranger only the rulebook and the deck; observe without coaching. This is where the rulebook gets fixed.
- **Metrics to track**:
  - Time to first match (proxy for accessibility).
  - % of invalid claims (proxy for rule clarity / glyph readability).
  - Player confusion points (where do they re-read the rules?).
  - Endgame satisfaction (does the 8-card split feel earned or arbitrary?).
- **Iterate** rules + corner-glyph design. The quick-ID system almost always needs tuning after first playtest.

**Deliverable**: `playtest/log.md` with one entry per session: date, players, demographics, issues observed, fixes tried.

---

## Phase 8 — Branding, naming, legal

- **Name clearance**:
  - [USPTO TESS](https://tmsearch.uspto.gov/) trademark search for "Seven Koi" in International Class 28 (games and playthings).
  - Domain check (`sevenkoi.com`, `sevenkoi.game`, `playsevenkoi.com`).
  - [BoardGameGeek](https://boardgamegeek.com/) search for collisions.
- **Logo / wordmark / box title treatment** — derived from the visual identity in Phase 4.
- **Copyright notice** — "© [Year] [Designer Name]" on cards (small, on the back or rulebook), full notice in the rulebook.
- **AI-art caveat** — if any art is AI-generated, keep prompt logs and confirm the generator's commercial-use license. The US Copyright Office currently does not register purely AI-generated images, which limits protection of derivative merch and may be a problem for a publisher pitch.
- **Credits** — designer, illustrator(s), font licenses, playtester thanks.
- **Optional**: ISBN / barcode (UPC for retail; many POD services provide one).

---

## Phase 9 — Production

- **Manufacturer comparison** (rough, per-deck cost at the listed run sizes):

| Manufacturer                                                   | MOQ      | ~Cost / deck | Notes                              |
|----------------------------------------------------------------|----------|--------------|------------------------------------|
| [The Game Crafter](https://www.thegamecrafter.com/)            | 1        | $15–25       | Easiest US POD                     |
| [MakePlayingCards](https://www.makeplayingcards.com/)          | 1        | $10–20       | International, good color          |
| [DriveThruCards](https://www.drivethrucards.com/)              | 1        | $10–20       | POD, retail channel                |
| [Whatz Games](https://www.whatzgames.com/)                     | ~500     | $4–8         | Bulk, China-based                  |
| [Panda Game Manufacturing](https://www.pandagm.com/)           | ~1500    | $3–6         | High-end, used by major publishers |
| [LongPack Games](https://www.longpackgames.com/)               | ~500     | $4–7         | Bulk, China-based                  |
| [Ninja Print](https://ninoprint.de/en/)                        | ~250     | $5–9         | Bulk, EU-based                     |

- **Components** — 64 cards + rulebook + tuckbox or 2-piece box. Optional: score pad, wooden scoring tokens, drawstring bag.
- **Pre-press checklist** — bleed, safe zone, color profile (CMYK with manufacturer's ICC), file naming convention, single combined proof PDF, font outlining.
- **Always order one physical proof** before any bulk run — colors and finishes shift between screen and print.

---

## Phase 10 — Funding & business model (only if commercial)

- **Self-fund POD** — lowest risk, lowest reach. Order on demand or in small batches.
- **Crowdfunding** ([Kickstarter](https://www.kickstarter.com/), [Backerkit](https://www.backerkit.com/), [Gamefound](https://gamefound.com/)) — needs:
  - Pre-launch landing page + email list (3–6 months of build).
  - Prototype playthrough video (90 seconds is the gold standard).
  - BGG listing.
  - Reviewer outreach (3–6 months lead time).
  - Pledge manager + fulfillment partner (e.g. Quartermaster Logistics, ShipQuest, Spiral Galaxy in EU).
- **Pitch to publisher** — produce a 1-page sell sheet (overview + hook + math + photo of prototype) and a 2-minute rules video. Target small-card-game publishers like [Button Shy](https://buttonshygames.com/), [Allplay](https://www.allplay.com/), [Pandasaurus](https://pandasaurusgames.com/), [Floodgate](https://floodgategames.com/), [AEG](https://www.alderac.com/).
- **Pricing** — small-deck retail typically $15–25. To reach retail, MSRP must support roughly a 4–5x markup over manufacturing cost (manufacturer → distributor → retailer → customer).
- **Realistic Kickstarter sizing for a small-deck game**:
  - Average pledge typically $20–35 (single tier with a stretch-goal upgrade), versus $80–100 for mid-weight board games with miniatures.
  - A single small-deck campaign that funds is usually in the $5K–$50K range; breakout small-deck campaigns occasionally reach $100K+.
  - Set the funding goal deliberately low (covers manufacturing + fulfillment for the minimum viable run) so the campaign can earn the green checkmark and the "Project We Love" boost early.

### Comparable campaigns (benchmarks to study)

A short reference list of campaigns to study for pacing, video, reward tiers, and stretch goals. Add to this as new comparables surface.

| Campaign | Designer / Publisher | Format | Goal → Pledged | Backers | Avg pledge | Notes |
|----------|----------------------|--------|----------------|---------|------------|-------|
| [Pantheum: Demigods of Olympia](https://www.kickstarter.com/projects/pantheum/pantheum-demigods-of-olympia) | Trevor Kerth | Engine builder + area control, 1–4 players | $10K → $288,619 (≈29x) | 3,374 | ~$85 | Sep–Oct 2024, 30-day campaign, "Project We Love" badge. Different weight class than Seven Koi but a strong example of a low-goal-high-overfund strategy and a polished campaign video. |

---

## Phase 11 — Marketing

- **Hook line** — try variants like: "A 64-card matching game built on the Hamming code: find the 4 koi that cancel out."
- **Reviewer / preview copies** — [BoardGameGeek](https://boardgamegeek.com/), [Shut Up & Sit Down](https://www.shutupandsitdown.com/), [Watch It Played](https://www.watchitplayed.com/) (for the how-to-play video), [No Pun Included](https://nopunincluded.com/), math-game YouTubers (Numberphile-adjacent, Matt Parker / Stand-up Maths).
- **Social** — short clips of a 9-card layout with a slow reveal of the matching 4. The visual symmetry of the koi makes this naturally good content.
- **Conventions** (only relevant at scale) — PAX Unplugged, Gen Con, Essen Spiel, UK Games Expo.

---

## Phase 12 — Distribution & fulfillment (only at scale)

- **Direct-to-consumer** via Shopify or BackerKit Shop (highest margin, all customer support is yours).
- **Distributor** ([Alliance Game Distributors](https://www.alliance-games.com/), [GTS](https://gtsdistribution.com/), [Asmodee](https://corporate.asmodee.com/)) — gets you into FLGSs but takes a big cut.
- **Fulfillment partner** for crowdfunding waves (Quartermaster Logistics in US, Spiral Galaxy in EU, Aetherworks in AU).
- **Tax / VAT** — register where required (especially EU IOSS for orders < €150).
- **Inventory + reorder policy** — track sell-through, set reorder thresholds before stockout.

---

## Open decisions (recap)

1. Publication route (print-on-demand / Kickstarter / publisher / personal).
2. Reconcile dealing math (initial layout 8 or 12, or "stop replenishing once deck empty").
3. ~~Final 7-of-13 koi selection.~~ Resolved — see [koi_selection.md](koi_selection.md).
4. ~~Player count and turn structure.~~ Resolved: **real-time call-out**, shout **"Koi!"** then touch four cards in order, invalid claim → locked out until another player claims a valid 4-card match. Player count still TBD (Phase 3).
5. Art pipeline (commissioned / DIY / AI-generated).
6. Whether to build a digital prototype (Tabletop Simulator / web / none).
