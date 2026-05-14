# koi_selection.md — retail roster for **Koi** (six breeds)

This file freezes the **retail** roster from [PLAN.md](PLAN.md): which six breeds (out of the thirteen on [ThirteenKoi.png](ThirteenKoi.png)) appear on the **32-card** deck for the game **Koi**. Selection criteria, in priority order: visual distinctness at thumbnail size, distinct silhouette/pattern density, cultural recognizability, and avoidance of near-duplicates.

**Kumonryu** is **not** on retail **Koi** cards; it is reserved as the seventh breed for the optional **Koi** expansion (seven species) ([`expansion/seven_koi/README.md`](expansion/seven_koi/README.md)). Repository math tools still exercise the seven-bit odd slice for that expansion geometry — see [CLAUDE.md](CLAUDE.md).

---

## 0. Seventh breed (expansion only)

**Kumonryu (九紋竜)** — held back from the base **six** so thumbnails stay maximally distinct at card scale; reinstated only if the seven-species **Koi** expansion SKU ships. See [`expansion/seven_koi/README.md`](expansion/seven_koi/README.md) and [`expansion/seven_koi/DECK_AND_RULES.md`](expansion/seven_koi/DECK_AND_RULES.md).

---

## 1. The six

Cards are numbered **1–6** in this order (the koi’s bit position in the **GF(2)⁶** encoding used in `math/NOTES.md` for the published odd-weight deck).

### 1. Kohaku — 紅白 (Kōhaku)

**Primary hex**: `#D7263D` (vermilion red on white)

The classic. A pure white body marked with bold patches of red. Kohaku is the oldest of the Gosanke (“big three”) koi and the bloodline against which every other variety is judged — when in doubt, the saying goes, “begin and end with Kohaku”.

### 2. Karasu — 烏鯉 (Karasu)

**Primary hex**: `#0D0D0D` (near-black body; uniform black read at card scale)

**All-black koi** (“crow carp”): a single uninterrupted sumi field from nose to tail — no hi, no second color blocks. At thumbnail size it is deliberately **flat black**; optional art direction is a whisper of **scale rows** or a **soft dorsal highlight** so the fish does not read as a silhouette hole. **Not** a tricolor Gosanke layout (that role is intentionally dropped from retail in favor of this cleaner black anchor).

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

Pure white body, single red disc on the head — the Japanese flag rendered in fish form. Named for the red-crowned crane (`tanchō-zuru`). The most visually striking of the six and the one casual players will recognise instantly.

---

## 2. Why these six and not the others

The thirteen-way shortlist and cut reasons for **Shusui, Sanke, Utsurimono, Hariwake, Bekko, Utsuri** are unchanged from the earlier seven-species write-up (see git history or [ThirteenKoi.png](ThirteenKoi.png) for the full grid).

**Kumonryu (九紋竜)** — see **section 0** for expansion placement. Retail uses **uniform Karasu** as the black anchor; **Kumonryu** stays expansion-only so players are not asked to separate two **sumi-forward** pattern languages under real-time pressure. Asagi, Ogon, Chagoi, and Tancho each own a distinct hue or motif beside Kohaku and Karasu.

---

## 3. Palette summary (for `design/style_guide.md`)

| #  | Koi    | Japanese   | Primary hex |
|----|--------|------------|-------------|
| 1  | Kohaku | 紅白       | `#D7263D`   |
| 2  | Karasu | 烏鯉       | `#0D0D0D`   |
| 3  | Asagi  | 浅黄       | `#2E6F95`   |
| 4  | Ogon   | 黄金       | `#E0B040`   |
| 5  | Chagoi | 茶鯉       | `#7B4B2A`   |
| 6  | Tancho | 丹頂       | `#F5F5F0`   |

The six primary colours stay spread around the wheel: warm red, neutral black, cool blue, warm yellow, warm brown, neutral white with a red crown accent.

---

## 4. Open follow-ups

- The corner **glyph row** in `PLAN.md` Phase 4 uses these hexes inside each breed’s **micro-crest** (horizontal segment), left → right in the order above — see `design/style_guide.md` §5 and `design/glyphs/six_crests.svg`.
- Japanese text: confirm with a native speaker that `紅白 / 烏鯉 / 浅黄 / 黄金 / 茶鯉 / 丹頂` are the canonical kanji forms for card use (sometimes `黄金` is written as `黄金鯉`, etc.).
