# koi_selection.md — the seven koi of Seven Koi

This file freezes the Phase 1 decision from [PLAN.md](PLAN.md): which seven koi varieties (out of the thirteen on [ThirteenKoi.png](ThirteenKoi.png)) appear in the deck. Selection criteria, in priority order: visual distinctness at thumbnail size, distinct silhouette/pattern density, cultural recognizability, and avoidance of near-duplicates.

The seven dropped varieties (Shusui, Sanke, Utsurimono, Hariwake, Bekko, Utsuri, plus one of the rotation candidates noted in §2) are listed at the bottom along with the reason each was cut.

---

## 1. The seven

Cards are numbered 1–7 in this order (the koi's bit position in the F_2^7 encoding from `math/NOTES.md`).

### 1. Kohaku — 紅白 (Kōhaku)

**Primary hex**: `#D7263D` (vermilion red on white)

The classic. A pure white body marked with bold patches of red. Kohaku is the oldest of the Gosanke ("big three") koi and the bloodline against which every other variety is judged — when in doubt, the saying goes, "begin and end with Kohaku".

### 2. Showa — 昭和三色 (Shōwa Sanshoku)

**Primary hex**: `#1A1A1A` (lacquer black, with red and white)

Named for the Shōwa era. A black-dominated tricolor with deep red and crisp white markings wrapping the body — the koi equivalent of a sumi-ink painting that has been splashed with vermilion. Reads jet-black at thumbnail size, which is what we want for contrast against Kohaku and Tancho.

### 3. Asagi — 浅黄 (Asagi)

**Primary hex**: `#2E6F95` (indigo-blue, scaled)

The oldest documented koi variety. A blue-grey net of scales runs the length of the back, with red blooming along the cheeks and belly. Named after the indigo-pale colour `asagi-iro`. Brings the only blue note in the deck.

### 4. Ogon — 黄金 (Ōgon)

**Primary hex**: `#E0B040` (metallic gold)

A single solid colour — burnished metallic gold from nose to tail — and nothing else. The simplicity is the point: at thumbnail size, an Ogon is a smooth gold ingot among patterned neighbours.

### 5. Chagoi — 茶鯉 (Chagoi)

**Primary hex**: `#7B4B2A` (tea brown)

The friendliest koi in any pond — chagoi are the first to learn to take food from a hand. A uniform tea-brown body, occasionally with a faint reticulated scale outline. Reads as a warm earth-tone counterweight to the cooler Asagi and the metallic Ogon.

### 6. Tancho — 丹頂 (Tanchō)

**Primary hex**: `#F5F5F0` (paper white, with `#D7263D` crown)

Pure white body, single red disc on the head — the Japanese flag rendered in fish form. Named for the red-crowned crane (`tanchō-zuru`). The most visually striking of the seven and the one casual players will recognise instantly.

### 7. Kumonryu — 九紋竜 (Kumonryū)

**Primary hex**: `#2B2B2B` (sumi black on white)

"Nine-marked dragon" — a scaleless (doitsu) koi whose flowing black-and-white pattern is said to shift with the seasons and water temperature, like ink dragging across rice paper. Where Showa is structured tricolor, Kumonryu is loose calligraphy: the contrast in pattern *style* (not just colour) is what earns it the seventh slot over the other black-and-white candidates.

---

## 2. Why these seven and not the others

| Dropped       | Reason for cut                                                                                       |
|---------------|------------------------------------------------------------------------------------------------------|
| Shusui        | Doitsu (scaleless) version of Asagi — same blue tonality and same red accents. Too close to Asagi.  |
| Sanke         | White-red-black tricolor; visually overlaps with Showa once shrunk to thumbnail.                    |
| Utsurimono    | Black with red/white/yellow markings — overlaps with Showa and the Utsuri family.                   |
| Utsuri        | Black with yellow markings — overlaps with Kumonryu (black-on-white) and the Utsurimono family.     |
| Bekko         | White body with black spots — overlaps with Kumonryu, with less visual character.                   |
| Hariwake      | Metallic white with orange/yellow patterning — overlaps with Ogon (metallic) and is less iconic.    |

Net result: the seven kept span seven distinct hue/pattern niches (red-on-white, black-tricolor, blue-scaled, solid-gold, solid-brown, white-with-red-spot, sumi-black-on-white) with no two confusable at thumbnail size on a triple or quintuple card.

---

## 3. Palette summary (for `design/style_guide.md`)

| #  | Koi      | Japanese      | Primary hex |
|----|----------|---------------|-------------|
| 1  | Kohaku   | 紅白          | `#D7263D`   |
| 2  | Showa    | 昭和三色      | `#1A1A1A`   |
| 3  | Asagi    | 浅黄          | `#2E6F95`   |
| 4  | Ogon     | 黄金          | `#E0B040`   |
| 5  | Chagoi   | 茶鯉          | `#7B4B2A`   |
| 6  | Tancho   | 丹頂          | `#F5F5F0`   |
| 7  | Kumonryu | 九紋竜        | `#2B2B2B`   |

The seven primary colours are deliberately spread around the wheel: warm red, neutral black, cool blue, warm yellow, warm brown, neutral white, neutral dark grey. Tancho and Kumonryu are the two close-to-neutral picks; Tancho is differentiated by the red `#D7263D` crown spot it shares with Kohaku.

---

## 4. Open follow-ups

- The corner-glyph design in `PLAN.md` Phase 4 should use these exact hexes for the seven small filled circles, in the order above.
- For the all-seven card, the seven hexes give a natural rainbow-ordering palette (red → black → blue → gold → brown → white → grey is fine; reorder by hue if a clockwise gradient looks cleaner).
- Japanese text: confirm with a native speaker that `紅白 / 昭和三色 / 浅黄 / 黄金 / 茶鯉 / 丹頂 / 九紋竜` are the canonical kanji forms for card use (sometimes `黄金` is written as `黄金鯉`, etc.).
- **Beginner (six-koi) mode:** rules and `CLAUDE.md` describe a parallel **32-card** deck consisting of odd-weight subsets of **six** koi—the seventh species is omitted on **every** card. **Which of the seven to exclude for production beginner decks is not decided.** Pedagogy likely favours omitting whichever variety is busiest visually for new players (possibly Kumonryu or Showa — revisit after glyph-row playtests).
