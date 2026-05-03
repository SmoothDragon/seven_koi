# PLAN.md — Seven Koi: roadmap to publication

A phase-by-phase plan to take Seven Koi from its current state (a concept, a koi reference sheet, and a one-line README) to a publishable card game. Each phase lists concrete deliverables. Open decisions are listed in Phase 0 and recapped at the bottom.

For the current repo state and the verbatim game spec, see [CLAUDE.md](CLAUDE.md). For the koi reference, see [ThirteenKoi.png](ThirteenKoi.png).

---

## Phase 0 — Decisions to lock first

These block later phases. Make them before sinking time into art or production.

1. ~~**Publication route**~~ — **resolved**: **Kickstarter** (crowdfunding). See Phase 10 for campaign prep, timelines, pledge manager, fulfillment.
2. **Dealing-math reconciliation** — `math/RESULTS.md` forces `L ≥ 10` (smaller layouts stall). Recommended: `L = 10, F = 10` (clean math, no mid-game stalls, endgame is continued real-time play on the 10-card residual). Original `L = 9, F = 8` is mathematically broken and removed from consideration.
3. ~~**Final 7-of-13 koi**~~ — **resolved** (see [koi_selection.md](koi_selection.md)): Kohaku, Showa, Asagi, Ogon, Chagoi, Tancho, Kumonryu.
4. ~~**Player count and turn structure**~~ — **resolved**:
   - Real-time call-out (everyone scans simultaneously; first to call a valid 4-card match collects it).
   - Call protocol: shout **"Koi!"** then touch the four cards in order.
   - Invalid-claim penalty: caller is locked out until the next valid 4-card match is claimed by another player (in mid-game this coincides with the next replenishment; in the endgame it's the moment another player claims one of the two 4-card groups).
   - Player count still TBD (see Phase 3).
5. ~~**Art pipeline**~~ — **resolved**: **AI-generated** (with licensing, copyright, and credit obligations). See Phase 5 and Phase 8.
6. ~~**Digital bonus**~~ — **resolved**: In-browser game implemented in **Rust**, compiled to **WebAssembly** (`bonus_web/`), shipped as a Kickstarter stretch goal / add-on. Uses `wasm-bindgen` + `wasm-pack`; UI can be plain HTML/JS or layered with a framework later.

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
- **4-card guarantee — original spec is BROKEN.** The cited classical bound `max Sidon in F_2^7 ≤ 2^⌊7/2⌋ = 8` is wrong for our deck. A 9-element Sidon set exists (`S₉ = {25, 28, 35, 47, 55, 70, 73, 100, 110}` in `math/NOTES.md` Lemma D), so a 9-card layout can fail to contain a 4-card match. Random-play simulation under `L = 9` stalls mid-game ~40% of the time (`math/RESULTS.md` §2). The minimum layout size that guarantees a 4-card match is **`L = 10`** (corollary, conditional on the empirical `max Sidon = 9`), at which random-play simulation stalls 0% of the time across 20,000 trials.
- **Endgame structure**:
  - **Proven** ([math/NOTES.md](math/NOTES.md) §7.1): the residual 8 cards always XOR to 0 (a single 8-card match in the parity sense).
  - **Disproven** ([math/NOTES.md](math/NOTES.md) §7.2, `math/RESULTS.md` §3): the further claim that the residual splits into two 4-card matches is **false ~50% of the time** under random play. Both Mode A (50k trials, 51.7% unsplittable) and Mode B with `L = 10` (20k trials, 47.4% unsplittable) confirm this. The "claim one → claim both" endgame rule cannot be the default and the fallback would fire in nearly half of all games.
- **Dealing arithmetic** (rewritten in light of `math/RESULTS.md`). With initial layout `L` and final layout `F`, total cards passing through play satisfy `64 = L + 4M + F`. The math results force `L ≥ 10` (smaller and the layout can stall). Clean choices:
  - **`L = 10, F = 10`** → `M = 11`. No mid-game stalls. Endgame begins with 10 cards on the table, which is more than the original "8 cards" intuition. Players continue real-time match-claiming on the 10-card residual until either it can't be reduced further or it reaches 0 / 2 cards. Simple and consistent with mid-game.
  - **`L = 10, F = 6`** → `M = 12`. Final residual has 6 cards. The 6-card residual still XORs to some fixed value (Σ D minus 12 zero-sums = 0), so it's an even-weight sum, but not necessarily 0 — depends on which cards were claimed mid-game. Less elegant.
  - The original `L = 9, F = 8` is **off the table**: math/RESULTS.md §2 shows it stalls 40% of the time.

**Deliverables**:

- [math/NOTES.md](math/NOTES.md) — math claims with the corrected status table (the cited classical Sidon bound was wrong; max Sidon = 9; the 4-card guarantee requires `L ≥ 10`; endgame splittability is empirically ~50%). **Done.**
- [math/RESULTS.md](math/RESULTS.md) — Monte Carlo simulation report (max-Sidon empirical search; mid-game stall sweep over `L ∈ {8, 9, 10}`; abstract reachability of unsplittable residuals). **Done.**
- [math/verify.py](math/verify.py) — Python verifier with sanity asserts and Mode A / Mode B Monte Carlo. **Done** for the simulations; remaining work:
  - **Formal proof that `max Sidon ≤ 9` in `D`.** Empirical evidence (50k random greedy trials, all max ≤ 9) is very strong but not a proof. Promising approaches: (a) symmetry breaking under `S_7` orbits of weight-3/weight-5 vectors; (b) SAT/ILP encoding; (c) connection to caps in projective geometry over F_2.
  - **Characterization of unsplittable 8-card residuals.** All 25k+ unsplittable residuals seen in Mode A are 8-element strict-Sidon sets. Counting and structurally describing them would let us tune the endgame rule precisely (e.g., dropping a small number of cards from the deck so that `max Sidon ≤ 7`, which would force every 8-card residual to split).

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
- **Endgame** — needs redesign in light of `math/RESULTS.md`:
  - **What's still true.** When the deck is exhausted, the residual cards always XOR to 0 (Lemma E, `math/NOTES.md` §7.1). With the recommended `L = 10, F = 10` dealing, the residual has 10 cards (not 8 as in the original spec).
  - **What's no longer assumed.** The "claim one 4-card group → claim both" rule was based on the residual splitting into two 4-card matches, which fails ~50% of the time empirically. That rule is dropped.
  - **Proposed new endgame rule (continued real-time play).** When the deck empties, real-time play simply continues on the residual: any player who calls a valid 4-card match claims those 4 cards. Repeat until either (a) the residual is reduced to 0, 2, or 6 cards by successful claims, or (b) no player can find a 4-card match (60-second silence). Any cards left at the end are split evenly (with leftover cards going to the player with the most cards collected so far, then by tiebreaker rules).
  - **Why this works.** It preserves the matching-game pacing through the endgame, avoids leaning on a false splitting theorem, and has a deterministic terminator (the silence timer). In the lucky case where the residual happens to split into two 4-card matches, this rule plays out exactly like the original "claim one → claim both" intent (the second claim is racing against an empty layout). In the unlucky ~50% case, the players just take what they can claim.
  - **Status:** locked as a working draft; revisit after the first round of playtesting.
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

- **Pipeline decision** — **locked: AI-generated.** Keep complete prompt logs + version metadata; ensure the tool’s **commercial-use license** allows Kickstarter physical goods; plan box/credit line for “art by [tool] + prompts by [you]” unless your attorney advises otherwise (see Phase 8).
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
- **Digital bonus (Kickstarter)** — `bonus_web/`: Rust crate targeting `wasm32-unknown-unknown`, packaged with [wasm-pack](https://rustwasm.github.io/wasm-pack/). Delivers a static site (HTML + JS glue) for play in the browser — remote playtests, campaign demo, digital tier fulfillment. Match `L=10` dealing and rules in `CLAUDE.md`. Tabletop Simulator remains optional and is *not* planned unless you add it later.

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
  - **Digital bonus tier** — deliver the in-browser build from `bonus_web/` (Rust → WASM). Host the static `www/` + `pkg/` bundle on your campaign page, Itch.io, or a simple CDN; fulfillment is usually a BackerKit digital-asset download or emailed link (no freight).
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

1. ~~Publication route~~ — Kickstarter (crowdfunding).
2. Reconcile dealing math: recommended `L = 10, F = 10` per `math/RESULTS.md` (the original `L = 9, F = 8` is mathematically broken — see `math/NOTES.md` §6 and `math/RESULTS.md` §4). Endgame rule rewritten as continued real-time play on the residual.
3. ~~Final 7-of-13 koi selection.~~ Resolved — see [koi_selection.md](koi_selection.md).
4. ~~Player count and turn structure.~~ Resolved: **real-time call-out**, shout **"Koi!"** then touch four cards in order, invalid claim → locked out until another player claims a valid 4-card match. Player count still TBD (Phase 3).
5. ~~Art pipeline~~ — **AI-generated**.
6. ~~Digital bonus~~ — **Rust → WebAssembly** in `bonus_web/` (Kickstarter stretch / add-on).
