# Seven Koi — design & illustration style guide

Living document for **card faces**, **glyphs**, and **print**. Canonical koi list, Japanese names, and flavor copy: [koi_selection.md](../koi_selection.md). Roadmap cross-links: [PLAN.md](../PLAN.md) Phase 4–5.

**Art scale mock (v0):** [design/mocks/seven_koi_card_art_scale_mock.png](mocks/seven_koi_card_art_scale_mock.png) — use as a **visual pitch** for “same breed, same style, three scale tiers”; replace with final hero assets when Phase 5 runs.

---

## 1. Print specification (card)

| Item | Value |
|------|--------|
| Finished size | 2.5" × 3.5" (63 × 88 mm), poker / MTG style |
| Bleed | **3 mm** beyond trim on every edge |
| Safe margin | **3 mm** inside trim (no critical text or glyph inside this inset) |
| Resolution | **300 DPI** minimum for raster; vector preferred for glyphs and UI chrome |
| Color | **CMYK** + printer **ICC profile** (get from manufacturer before final export) |

Export: one PDF per sheet or per card per manufacturer spec; outline fonts where required.

---

## 2. The seven breeds (order is fixed)

Bit order **1 → 7** matches card encoding and **glyph row left → right**. Use these **primary hexes** for badges, glyph fills, UI — not necessarily full-body paint (fish stay naturalistic).

| # | English | Japanese (card) | Primary hex |
|---|---------|-----------------|-------------|
| 1 | Kohaku | 紅白 | `#D7263D` |
| 2 | Showa | 昭和三色 | `#1A1A1A` |
| 3 | Asagi | 浅黄 | `#2E6F95` |
| 4 | Ogon | 黄金 | `#E0B040` |
| 5 | Chagoi | 茶鯉 | `#7B4B2A` |
| 6 | Tancho | 丹頂 | `#F5F5F0` (body); crown spot `#D7263D` |
| 7 | Kumonryu | 九紋竜 | `#2B2B2B` |

**Background:** off-white parchment **or** muted pond-water blue — keep value contrast so white-bodied fish (Tancho) do not disappear.

---

## 3. Illustration style (all card types)

**Goal:** At a glance, players recognize **which breeds** are on a card; at table distance, **glyph row** still carries the load.

### 3.1 Unified “breed bible”

For **each** of the seven breeds, maintain **one approved hero** (pose, lighting, scale detail, outline weight). Every appearance of that breed on **single / triple / quint / all-seven** cards is a **scaled or cropped derivative** of the same art system — not a redraw in a different style.

- **View:** three-quarter or slightly top-down; **consistent camera height** and **light direction** across all seven masters.
- **Rendering:** clean illustrative look (cel or soft vector); **avoid** photoreal noise, heavy texture, or hyper-real scales that collapse when shrunk.
- **Outlines:** single coherent stroke weight at **master** scale; when rasterized down, prefer **slightly thicker** inner lines so small fish do not “hairline away.”
- **Eyes and mouth:** same graphic formula per breed at every scale (big read for tiny triple icons).

### 3.2 Scale tiers (relative to **safe area**)

Use **vector masters** where possible; when rasterizing, export at **2×** final print px for sharpening.

| Card type | Koi count | Approx. height of one fish *(each, if multiple)* | Notes |
|-----------|-----------|-----------------------------------------------------|--------|
| **Single** | 1 | **~78–85%** of safe-area height | Hero art; English name top, Japanese bottom, badge 1–7. |
| **Triple** | 3 | **~38–48%** each | Reuleaux-ish inward composition; **same** style as single. |
| **Quintuple** | 5 | **~22–30%** each | Pentagonal / pentagram; slight rotation offset so heads stay readable. |
| **All-seven** | 7 | **~14–20%** each | Mandala / ring; **legibility over decoration** — if a layout fails a “squint test,” simplify background. |

**Mock reference:** the Kohaku column in [seven_koi_card_art_scale_mock.png](mocks/seven_koi_card_art_scale_mock.png) shows **large / medium / small** in one style — replicate that discipline for **all seven** masters.

---

## 4. Layout zones (per card type)

### 4.1 Single-koi

- **Top:** English name (small caps or restrained serif).
- **Center:** hero koi (dominant).
- **Bottom:** Japanese (kanji + romaji line).
- **Corner:** koi index badge **1–7** + **glyph row** (section 5).

### 4.2 Triple, quintuple, all-seven

- **Center:** fish arrangement (section 3.2).
- **Per-fish micro-badge:** optional small **1–7** near each head; must not collide with art.
- **Glyph row:** always present in the **same corner** on every card front (habit muscle memory).

---

## 5. Quick-ID glyph row (mandatory)

Seven positions, **left to right = koi 1 … 7** (same as table in section 2).

- **Present on card:** filled circle using that koi’s **primary hex** (Tancho body may use off-white fill with **red stroke** on crown position only if clearer — test print).
- **Absent:** empty ring or 20–30% value disk with **1 pt** stroke so empty slots are visible on pale stock.
- **Diameter (print):** start ~**2.0–2.4 mm**; increase if playtests show misses; never shrink below **1.8 mm** without raising DPI or sheet size.
- **Contrast:** glyphs must survive **worn sleeves** and **warm indoor light**; avoid placing the row on busy scales — use a **flat matte panel** behind the row if needed.

**Standard mode (six koi):** the **omitted** species still occupies a slot in the row — use **muted** fill (e.g. 25% opacity of that hex) or a **struck-through** ring per [rules/RULES.md](../rules/RULES.md) production decision.

**Accessibility:** do not rely on **hue alone** for empty vs full — shape (ring vs disk) and value contrast must pass a quick grayscale check.

---

## 6. Standard subset aid (optional print cue)

One retail SKU is **64** cards; Standard uses **32**. Optional **manufacturing** cue so players can sort without reading every face:

- **Micro-mark** in a consistent corner (e.g. only on cards that depict the **canonical omitted** koi for retail Standard — *once that koi is chosen*), **or**
- **Tuck-box insert** diagram: “Remove all cards showing koi #N.”

Document the final decision here when locked; align with manufacturer registration specs.

---

## 7. Typography

- **Latin:** readable serif or humanist sans for names; avoid ultra-thin weights under 8 pt.
- **Japanese:** kanji + romaji; fonts must ship with **commercial license** for print (e.g. Noto Serif JP, Klee, Yuji Syuku — confirm license before embedding).
- **Minimum text size:** nothing critical below **6.5 pt** at 300 DPI on 63 × 88 mm without physical proof.

---

## 8. Card back

Single shared design for the whole product: **water surface + seigaiha** (or similar) at low contrast so **edge wear** does not reveal front patterns. No seven-koi glyph on back (optional publisher logo only).

---

## 9. AI-generated art pipeline (Phase 5 / Phase 8)

- **Locked:** AI-generated pipeline — keep **prompt logs**, **seed**, model name, and **date** per export.
- **Commercial license:** verify generator terms allow **Kickstarter + physical goods** + resale.
- **Credit line:** plan box / rulebook line (e.g. art by [tool], prompts by [designer]) per attorney advice.
- **Handoff:** deliver **layered** files (PSD / Affinity / SVG) or **high-res PNG** with transparent fish on separate layers from background for layout tweaks.

---

## 10. File naming (suggested)

```
art/koi/<breed>_master.png          # hero 1:1 per breed
art/koi/<breed>_thumb.png          # downsized common export
cards/export/<card_id>_front.pdf
design/mocks/...                   # pitches only, not for press
```

Use English **breed** slug: `kohaku`, `showa`, `asagi`, `ogon`, `chagoi`, `tancho`, `kumonryu`.

---

## 11. Revision log

| Version | Date | Notes |
|---------|------|--------|
| 0.1 | 2026-05-03 | Initial style guide: print spec, palette, illustration discipline, scale tiers, glyphs, Standard aid, typography, AI notes. |
