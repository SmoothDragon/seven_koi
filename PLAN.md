# PLAN.md — Seven Koi: roadmap to publication

A phase-by-phase plan to take Seven Koi from its current state (a concept, a koi reference sheet, and a one-line README) to a publishable card game. Each phase lists concrete deliverables. Open decisions are listed in Phase 0 and recapped at the bottom.

For the current repo state and the verbatim game spec, see [CLAUDE.md](CLAUDE.md). For the koi reference, see [ThirteenKoi.png](ThirteenKoi.png).

---

## Phase 0 — Decisions to lock first

These block later phases. Make them before sinking time into art or production.

1. **Publication route** — print-on-demand, crowdfunding, pitch-to-publisher, or personal/hobby.
2. **Dealing-math reconciliation** — see Phase 2; the stated "9 out / 8 left" arithmetic does not close over a 64-card deck. Pick: initial layout of 8, initial layout of 12, or "stop replenishing once the deck is empty" with the residual handled explicitly.
3. **Final 7-of-13 koi** — recommendation in Phase 1.
4. **Player count and turn structure** — real-time call-out vs turn-based scan.
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

**Deliverable**: `koi_selection.md` with the seven chosen koi, English + Japanese (kanji + romaji) names, a 1–2 sentence flavor blurb each, and the primary color hex above for use in card design.

---

## Phase 2 — Mathematical verification (do before art)

Lock the math before committing to art, because if a claim is wrong the rules change.

- **Card structure**: confirm the 64 cards are exactly the odd-weight binary vectors of length 7. Counts: C(7,1) + C(7,3) + C(7,5) + C(7,7) = 7 + 35 + 21 + 1 = 64. ✓ (combinatorially trivial)
- **Match definition**: a "match" is a subset of cards whose bitwise XOR is the zero vector — equivalently, every koi appears an even number of times across the chosen cards.
- **Minimum match size = 4**: every card has odd Hamming weight; sum of an odd number of odd weights is odd, so the smallest non-empty subset that can sum to even-weight (and zero in particular) has size 2 or 4. Size 2 would require two identical cards, which is impossible in this deck — so the minimum non-trivial match is 4. ✓
- **4-card guarantee in any 9-card layout**: established per the proof at <https://chatgpt.com/share/69f67dcc-d818-832f-80a4-bb5e0c37e963> ("Subset sum to zero"). Equivalent statement: the maximum Sidon set among the 64 odd-weight vectors of F_2^7 has size ≤ 8. The natural 8-element Sidon set `{e_1, ..., e_7, 1111111}` is maximal — every additional odd-weight vector closes a 4-cycle:
  - any weight-3 vector `e_i + e_j + e_k` closes with `{e_i, e_j, e_k}`;
  - any weight-5 vector `v` closes with `{1111111, e_i, e_j}` where `e_i, e_j` are the two unit vectors absent from `v`.
- **Endgame split**: verify that the final 8 cards always partition into two 4-card matches (and characterize what happens if a player misidentifies the split).
- **Dealing arithmetic**. With initial layout L and final layout F, total cards passing through play satisfy `64 = L + 4M + F` where M is the number of mid-game matches. The user's stated `L = 9, F = 8` gives M = 11.75 (no integer solution). Resolutions:
  - **L = 8, F = 8** → M = 12. Cleanest; loses one card from initial spread.
  - **L = 12, F = 8** → M = 11. More cards visible from start (easier first match).
  - **L = 9, F = 8, deck empties mid-game** → after the deck runs out, claimed matches simply shrink the layout from 9 → 5 → ... etc. This is rule-elegant but the endgame is no longer guaranteed to be exactly 8 cards.
  - Pick one and update the rules document accordingly.

**Deliverable**: `math/verify.py` (a small Python script using `itertools` and bitmask XOR for two independent checks: (a) enumerate Sidon sets among odd-weight F_2^7 vectors via branch-and-bound and confirm none reach size 9, which is equivalent to the 4-card guarantee; (b) verify the endgame-split claim on every reachable 8-card residual) plus `math/NOTES.md` with the writeup of the cited proof in our own words, the chosen dealing convention, and the verification results.

---

## Phase 3 — Rules document

- **Player count, age, time** — suggested 2–6 players, 10+, 15–25 min. Confirm via playtest.
- **Setup** — shuffle, deal initial layout (number set in Phase 2).
- **Turn structure** — real-time call-out (everyone scans simultaneously; first to call a valid match collects it) vs turn-based (each player scans on their turn). Real-time fits the matching genre (cf. SET) but penalizes slower players; turn-based is friendlier for kids/casual.
- **Match claim resolution** — call out + point to 4 cards; group verifies XOR-to-zero by checking each koi appears 0, 2, or 4 times.
- **Scoring** — collected cards go face-up in front of the claimer; final score = total koi pips across collected cards.
- **Tiebreakers** — most cards collected, then most all-seven cards, then highest-weight single card.
- **Endgame split** — define what happens if a player calls only one of the two final 4-card groups (do they get only the called group, or both?). The verbatim spec says "gets both," so document that.
- **Edge cases** — simultaneous claims, invalid claim penalty (lose a card? skip a turn?), accidental over/under-deal.
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
3. Final 7-of-13 koi selection (recommendation in Phase 1).
4. Player count and turn structure (real-time call-out vs turn-based).
5. Art pipeline (commissioned / DIY / AI-generated).
6. Whether to build a digital prototype (Tabletop Simulator / web / none).
