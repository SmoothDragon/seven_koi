# PLAN.md — Seven Koi: roadmap to publication

A phase-by-phase plan to take Seven Koi from its current state (a concept, a koi reference sheet, and a one-line README) to a publishable card game. Each phase lists concrete deliverables. Open decisions are listed in Phase 0 and recapped at the bottom.

For the current repo state and the verbatim game spec, see [CLAUDE.md](CLAUDE.md). For the koi reference, see [ThirteenKoi.png](ThirteenKoi.png).

---

## Phase 0 — Decisions to lock first

These block later phases. Make them before sinking time into art or production.

1. ~~**Publication route**~~ — **resolved**: **Kickstarter** (crowdfunding). See Phase 10 for campaign prep, timelines, pledge manager, fulfillment.
2. **Dealing-math reconciliation — locked playable procedure** (`math/NOTES.md` §6, **`math/explore_sidon_odd_restricted/`**, **[CP24]** background in `math/NOTES.md` / `CLAUDE.md`):
   - **Fixed tableau, no mid-game stock flips.** **Expert (seven koi):** **`L₀ = 10`**. **Standard (six koi):** **`L₀ = 8`**. After each successful claim, replenish toward **`L₀`** as before. **No** “unanimous deadlock → flip one from stock” step: exhaustive strict-Sidon search on the odd-weight slices certifies **`s_max(O_7)=9`** and **`s_max(O_6)=7`** (`cargo run --release -- --prove-odd-n 7` / **`6`** in that crate), so **every** **`L₀`**-card layout from the legal deck contains a **4-card XOR match** (see `math/NOTES.md` §6 Corollary). If the table agrees no match is visible, treat it as a missed call—keep scanning. **[CP24]** ambient thresholds (**`|L| ≥ 13`** in **`GF(2)^7`**, **`|L| ≥ 10`** in full **`GF(2)^6`**) remain optional **literature context**; published play stays on the **odd-card deck** at **`L₀` only**.
   - **Expert (seven koi, `|D| = 64`).** Lay out **`L₀ = 10`** cards. After each successful claim move those four cards to the claimant's pile, then draw from the deck until the spread is **`L₀` again**, or until the deck runs out (**partial replenish** on the last cycle).
   - **Standard (six koi, `|D| = 32`).** **`L₀ = 8`**; replenish toward **eight** whenever the deck has stock. Mode B empirical sweep (**`math/layout_stall_sweep.py`**, **`math/RESULTS.md`**) still documents why smaller **`L`** stalled in simulation; formal **non-stall** at **`L₀`** now follows from **`s_max(O_6)=7`**. **`32 − L₀ = 24`** is divisible by **4**; **`|spread| < L₀`** after a claim once stock is dry matches Expert.
   - **Endgame — maximal tableau then consensus stop.** The moment the **facedown** pile **empties** mid-replenish, deal **every** remaining stub **face-up** in **one sweep** — **nothing stays hidden**, even when **`|spread| < L₀`**. Claims continue (**real-time**) until **everyone agrees** **no legal 4-card match** remains (**instant game over**; **tableau fish score nobody**).
   - **Scoring.** Each player totals **every koi (fish)** printed on cards **they claimed**; tiebreakers stay as Phase 3.
   - **Superseded:** fixed **`L = 9, F = 8`** on the 64-card deck remains invalid. **Superseded:** **baseline + escalation toward `13` / `10`** — replaced by **fixed Expert `L₀ = 10` / Standard `L₀ = 8`** with **no** mid-game escalation now that **`s_max(O_7)`** and **`s_max(O_6)`** are exhaustively certified on the odd slices.
3. ~~**Final 7-of-13 koi**~~ — **resolved** (see [koi_selection.md](koi_selection.md)): Kohaku, Showa, Asagi, Ogon, Chagoi, Tancho, Kumonryu.
4. ~~**Player count and turn structure**~~ — **resolved**:
   - Real-time call-out (everyone scans simultaneously; first to call a valid 4-card match collects it).
   - Call protocol: shout **"Koi!"** then touch the four cards in order.
   - Invalid-claim penalty: caller is locked out until the next valid 4-card match is claimed by another player (typically coincides with the next baseline refresh in mid-game; in the endgame, with the next successful claim on the residual).
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

**Literature.** Czerwinski–Pott [CP24] (*Advances in Mathematics of Communications* 18 (2024), 549–566; [DOI](https://doi.org/10.3934/amc.2023054), [arXiv:2304.07906](https://arxiv.org/abs/2304.07906)) is the authoritative source for Sidon sets in `F_2^t`, connections to `[n,k,5]` linear codes, and improved upper bounds on `s_max(F_2^t)`; full citation and proposition mapping in [math/NOTES.md](math/NOTES.md) References.
- **Card structure**: confirm the 64 cards are exactly the odd-weight binary vectors of length 7. Counts: C(7,1) + C(7,3) + C(7,5) + C(7,7) = 7 + 35 + 21 + 1 = 64. ✓ (combinatorially trivial)
- **Match definition**: a "match" is a subset of cards whose bitwise XOR is the zero vector — equivalently, every koi appears an even number of times across the chosen cards.
- **Minimum match size = 4**: every card has odd Hamming weight; sum of an odd number of odd weights is odd, so the smallest non-empty subset that can sum to even-weight (and zero in particular) has size 2 or 4. Size 2 would require two identical cards, which is impossible in this deck — so the minimum non-trivial match is 4. ✓
- **4-card guarantee — original spec is BROKEN.** The cited classical bound `max Sidon in F_2^7 ≤ 2^⌊7/2⌋ = 8` is wrong for our deck. A 9-element Sidon set exists (`S₉ = {25, 28, 35, 47, 55, 70, 73, 100, 110}` in `math/NOTES.md` Lemma D), so a 9-card layout can fail to contain a 4-card match. Random-play simulation under `L = 9` stalls mid-game ~40% of the time (`math/RESULTS.md` §2). **Deck-local corollary (`math/NOTES.md` §6):** **`s_max(O_7)=9`** is now **exhaustively certified** (`math/explore_sidon_odd_restricted`, **`--prove-odd-n 7`**), so **every `10`-card** layout from **`D`** contains a 4-match; Mode B at fixed `L = 10` never stalled in simulation. **Standard (six koi):** **`s_max(O_6)=7`** (**`--prove-odd-n 6`**), so **`L₀ = 8`** likewise forces a match. **Published dealing:** **fixed `L₀` only**, **no** mid-game escalation. **`[CP24]`** ambient caps (**`13` / `10`** in full **`GF(2)^7` / `GF(2)^6`**) remain weaker optional background than the odd-slice certificates.
- **Endgame structure**:
  - **Proven** ([math/NOTES.md](math/NOTES.md) §7.1): once matched cards leave the tableau and further draws fail, cards **R** still face-up satisfy **Σ R = 0** (even koi-parity everywhere). Figures like **`|R| = 8` vs `10`** in older notes assumed fixed dealing; **`|R|` now varies** with partial replenishments (Phase 3 endgame).
  - **Disproven** ([math/NOTES.md](math/NOTES.md) §7.2, `math/RESULTS.md` §3): the residual need **not** split into two stacked 4-card matches (~50% empirical failure). Mode A (50k trials, 51.7% unsplittable residuals) plus Mode B at fixed **`L = 10`** (20k trials, 47.4% unsplittable among tested residuals) back this up for the stabilized simulation paths.
- **Dealing archetypes** (detail in **`PLAN.md` Phase 0**). Fixed **`L = F = 10, M = 11`** was one tidy accounting path consistent with **`|D| = 64`** and no Mode B stalls. **Canonical published flow** is **fixed Expert `L₀ = 10`** and **Standard `L₀ = 8`**, **no** mid-game escalation, justified by exhaustive **`s_max(O_7)=9`** / **`s_max(O_6)=7`** on the odd slices (`math/explore_sidon_odd_restricted`). **`L = 9, F = 8`** on **`|D| = 64`** stays invalid (stall statistics in `math/RESULTS.md` §2).

**Deliverables**:

- [math/NOTES.md](math/NOTES.md) — math claims with the corrected status table (wrong classical Sidon bound; deck-local **`s_max(O_7)=9`** certified; **`[CP24]`** ambient background; Standard **`L₀ = 8`** with **`s_max(O_6)=7`**; endgame splittability ~50%). **Done.**
- [math/RESULTS.md](math/RESULTS.md) — Monte Carlo simulation report (max-Sidon empirical search; mid-game stall sweep over `L ∈ {8, 9, 10}`; cross-`n` odd-weight **`layout_stall_sweep`**; abstract reachability of unsplittable residuals). **Done.**
- [math/verify.py](math/verify.py) — Python verifier with sanity asserts and Mode A / Mode B Monte Carlo. **Done** for the **Expert 64-card** simulations; extensions still open:
  - **Formal `max Sidon` on the Expert odd slice `D`.** **Done** in-repo: exhaustive search certifies **`s_max(O_7)=9`** (`math/explore_sidon_odd_restricted`, **`--prove-odd-n 7`**). Optional: mirror certificate in `math/NOTES.md` prose or ship a short reproducibility note.
  - **Standard deck (`|D| = 32`, six odd-weight subsets after one koi omitted).** **`s_max(O_6)=7`** certified (**`--prove-odd-n 6`**); **`L₀ = 8`** is theorem-backed. Residual statistics for the 32-card slice can still be tightened for copywriting.
  - **Characterization of unsplittable residuals** (Mode A historically used residual size 8; with `L = F = 10` residuals have 10 cards). Counting and structurally describing unsplittable cases would let us tune endgame wording or decks precisely (e.g., dropping cards so maximal Sidon is smaller forces more splits).

---

## Phase 3 — Rules document

Ship one rulebook section for **Expert (7 koi, 64 cards)** and **Standard (6 koi, 32 cards)** — same flow, different `|D|`, **fixed layout `L₀ = 10`** (Expert) vs **`L₀ = 8`** (Standard); **no** mid-game stock flips on deadlock (see Phase 0 item 2 and Sidon certificates in `math/explore_sidon_odd_restricted`).

- **Player count, age, time** — suggested 2–6 players, 10+, 15–25 min (Standard runs shorter). Confirm via playtest.
- **Setup** — decide version; remove all cards that reference the **omitted koi** before shuffling (unless using a pre-sorted starter deck). See Phase 4 / Open decisions for sorting aids.
- **Turn structure** — **real-time call-out** (locked in Phase 0): all players scan the layout simultaneously; the first to call a valid 4-card match claims it. Fits the matching-game lineage (cf. *SET*).
- **Call protocol** (locked): the claiming player **shouts "Koi!" and then touches the four cards in order**. The shout is the time-stamp; the touches are the proof. Two players almost-tying is resolved by the shout, not by the touches.
- **Match claim resolution** — once "Koi!" is called, all play pauses; the caller touches four cards in order and the group verifies that each **active** koi appears 0, 2, or 4 times across them (seven in Expert, six in Standard). If valid: caller takes the four cards. If invalid: invalid-claim penalty applies.
- **Invalid-claim penalty** (locked): the caller is **locked out until the next 4-card match is claimed by someone else**. They keep all previously collected cards. In mid-game this typically ends when the next replenishment happens; in the endgame it ends when another player claims a match on the residual.
- **Scoring** — each player totals **every koi (fish)** printed on cards **they claimed**; tableau leftovers score for **nobody**.
- **Tiebreakers** — most cards collected, then **most all-koi card(s)** (Expert: 7-of-7; Standard: 6-of-6 among the active set), then highest-weight single card among active koi.
- **Endgame** — locked framing for `rules/RULES.md`:
  - **What's still true.** When the facedown pile is drained, Lemma E (**`math/NOTES.md` §7.1**) still XORs leftover face-up multisets appropriately for **`|D|=64`** and **`|D|=32`**; unsplittable residuals remain common (`math/RESULTS.md` §3), so leftover cards may conceal **hard** matches.
  - **Drain-out tableau.** Lay out **all** undealt remnant onto the tableau so the visible spread uses **every** card not already claimed (**maximum fill**, even when **`|spread| < L₀`**).
  - **Terminator.** Continue real-time 4-match claims until the **whole group unanimously agrees** there are **no** further legal matches → **game over**. Removed: timed silence splits and scavenged leftover splits (optional house rules only).
  - **Scoring.** Count **every koi (fish)** glyph on cards **each player claimed** only; tableau leavings tie at **zero** contribution.
- **Mixed-skill handicap variant** — the rulebook should suggest a "house handicap" (e.g. faster players sit on their hands for the first N seconds of each layout) for mixed-skill groups, since real-time inherently penalizes slower scanners.
- **Edge cases** — simultaneous "Koi!" shouts (rule: nearest-shouter as judged by the table; fall back to rock-paper-scissors), accidental over/under-deal, mid-touch reveal of an obviously invalid match (caller still pays the penalty).
- **Variants:**
  - **Standard:** already a first-class **32-card six-koi** deck — duplicate rules text there instead of burying under "variants only."
  - Solitaire/timed, cooperative drills, optional future "five-koi sandbox" (`|D|=16`) only after separate math review.

**Deliverable**: `rules/RULES.md` v0.1.
---

## Phase 4 — Card design (graphic design, not yet illustration)

- **Card spec** — 2.5" x 3.5" (63 x 88 mm), 3 mm bleed on every edge, 3 mm safe margin inside the trim, 300 DPI, CMYK, ICC profile per manufacturer.
- **Single-koi card layout** — large central illustration; English name top, Japanese name (kanji + romaji) bottom; koi-number badge (1–7) and corner indicator glyph.
- **Triple card layout** — three koi swimming inward in roughly a Reuleaux-triangle arrangement, each with a small badge for quick scanning.
- **Quintuple card layout** — five koi in a pentagonal/pentagram arrangement; consider a slight rotational offset so each koi remains identifiable.
- **All-seven card** — unique heptagonal/mandala arrangement.
- **Card back** — single shared design (water + seigaiha wave pattern).
- **Quick-ID system** — every card carries a row of seven small filled/unfilled circles in a corner (one per koi, filled = present). This is the visual analogue of the underlying bit vector and is the single most important playability decision: without it, scanning a dense layout for matches is brutal.
- **Deck split cue (Standard vs Expert)** — if one physical deck serves **both** 64-card Expert and **32-card** Standard games, pick a conspicuous **corner registration mark** (e.g. a screen-printed dot, foil hit, micro-icon, or color tick) keyed to "include this sheet in Standard" vs "Expert only". Document placement in `design/style_guide.md`; align with tuck-box divider / insert copy.
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
- **Digital bonus (Kickstarter)** — `bonus_web/`: Rust crate targeting `wasm32-unknown-unknown`, packaged with [wasm-pack](https://rustwasm.github.io/wasm-pack/). Delivers a static site (HTML + JS glue) for play in the browser — remote playtests, campaign demo, digital tier fulfillment. Match dealing + **consensus endgame** described in **`CLAUDE.md`**. Tabletop Simulator remains optional and is *not* planned unless you add it later.

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

- **Components** — primary SKU: **64** Expert cards + rulebook + tuckbox or 2-piece box. Variant: **single print run carrying both modes** uses the same fronts with registration marks segregating Standard (32 usable) vs Expert piles; tuck-box divider or leaflet explains removal. Separate **32-card** Standard-only SKU optional. Accessories: score pad, wooden scoring tokens, drawstring bag.
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
2. **Dealing / endgame:** Expert **`L₀ = 10`**, Standard **`L₀ = 8`**; **no** mid-game stock escalation (every **`L₀`** layout from the legal deck contains a 4-match by **`s_max(O_7)=9`** / **`s_max(O_6)=7`**, `math/explore_sidon_odd_restricted`). When the pile runs dry, flip **every** facedown remnant in **one endgame sweep** (**max tableau**). End when everyone agrees **no legal match** remains. Score **claimed fish/koi only**. Original **`L = 9, F = 8`** on **`|D| = 64`** remains invalid.
3. ~~Final 7-of-13 koi selection.~~ Resolved — see [koi_selection.md](koi_selection.md).
4. ~~Player count and turn structure.~~ Resolved: **real-time call-out**, shout **"Koi!"** then touch four cards in order, invalid claim → locked out until another player claims a valid 4-card match. Player count still TBD (Phase 3).
5. ~~Art pipeline~~ — **AI-generated**.
6. ~~Digital bonus~~ — **Rust → WebAssembly** in `bonus_web/` (Kickstarter stretch / add-on).
