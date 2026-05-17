# Economist-inspired editorial style

> **Disclaimer.** This `DESIGN.md` is an original interpretation of the
> editorial design language commonly associated with **The Economist**
> magazine. It is **not** affiliated with, endorsed by, derived from,
> or based on any official Economist publication, asset, codebase, or
> internal style guide. All token names, hex values, type-scale ratios,
> and component descriptions are referential and built on widely
> recognized public visual traits.
>
> *"The Economist"* is a trademark of The Economist Newspaper Limited.
> Use of the name here is descriptive (to identify the visual style being
> referenced), not commercial or associative.
>
> ---
>
> This file is included in
> [wechat-design-html](https://github.com/brucecbi/wechat-design-html)
> as the source-of-truth design system for the `economist` theme. The
> WeChat-renderable subset of these tokens lives in
> [`themes/economist.json`](../themes/economist.json) — that's the file
> the runtime actually consumes. Many things described below
> (multi-tier type scale, charts, shadow levels, responsive breakpoints,
> dashboard patterns) do not survive WeChat's HTML whitelist and are
> dropped in the JSON.

---

# Economist Inspired Design System

A DESIGN.md-style document modeled after the editorial and interface language associated with The Economist: high-contrast print heritage, disciplined information hierarchy, restrained typography, signature red accents, and dense but calm analytical layouts.

This document is designed for AI agents generating landing pages, dashboards, reports, article pages, briefings, and magazine-like longform experiences that should feel intelligent, credible, and editorial rather than startup-marketing glossy.

---

## 1. Visual Theme & Atmosphere

### Core Mood
- Serious, intelligent, internationally minded
- Editorial rather than promotional
- Dense with information, but never chaotic
- Premium print heritage translated into digital clarity
- Quietly authoritative, not flashy

### Design Philosophy
- Use **restraint as a design feature**
- Prefer **hierarchy, rhythm, and proportion** over decorative effects
- Let **typography and spacing** do most of the work
- Accent color should feel **institutional and iconic**, not playful
- Layouts should support **analysis, comparison, reading, and scanning**

### Experience Keywords
- Editorial
- Analytical
- Credible
- Disciplined
- Red-accented
- Structured
- Print-informed
- International affairs / business intelligence

### Surface Character
- Mostly bright backgrounds with strong contrast
- Occasional black or charcoal bands for emphasis
- Minimal gradients; flat color preferred
- Borders and rules used deliberately to separate sections like print columns

---

## 2. Color Palette & Roles

### Primary Palette
| Token | Hex | Usage |
|------|-----|------|
| Economist Red | `#E3120B` | Brand accent, primary CTA, data highlight, active states |
| Ink Black | `#111111` | Headlines, core text, high-contrast UI elements |
| Editorial Charcoal | `#2A2A2A` | Secondary headings, nav text, dividers on light surfaces |
| Paper White | `#FFFFFF` | Main page background |
| Newsprint | `#F7F5F2` | Soft section background, cards, pull quotes |
| Rule Gray | `#D9D4CD` | Borders, table rules, separators |
| Caption Gray | `#6B6B6B` | Metadata, captions, supporting labels |
| Data Gray | `#B9B4AD` | Neutral chart lines, disabled states |

### Supporting Palette
| Token | Hex | Usage |
|------|-----|------|
| Deep Burgundy | `#8A1C1C` | Dark editorial emphasis, hover darkening for red |
| Slate Blue | `#48627A` | Secondary chart series, cool analytical contrast |
| Forest Graph | `#2F6B55` | Positive trend lines, restrained success state |
| Amber Briefing | `#C98A2E` | Caution markers, data callouts |
| Crisis Plum | `#6E445B` | Alternate data accent for geopolitics/markets |

### Color Usage Rules
- Red is **rare and meaningful**. Do not flood the page with red.
- Prefer black text on white or warm off-white backgrounds.
- Use gray rules and column structure to create editorial discipline.
- Charts should use muted analytical colors, not SaaS neon palettes.
- Avoid candy colors, saturated gradients, and glassmorphism.

---

## 3. Typography Rules

### Typography Strategy
The Economist feel comes from the tension between **formal serif editorial typography** and **high-discipline sans-serif utility text**.

### Font Stack
#### Headlines / Editorial Display
```css
font-family: "Georgia", "Iowan Old Style", "Times New Roman", serif;
```
Use a refined serif for article titles, feature headings, quote pullouts, and magazine-like hero sections.

#### UI Sans / Data / Navigation
```css
font-family: Inter, "Helvetica Neue", Arial, sans-serif;
```
Use a neutral sans for nav, metadata, buttons, tables, labels, and charts.

#### Monospace (rare)
```css
font-family: "SF Mono", "IBM Plex Mono", Consolas, monospace;
```
Use only for market numbers, code-like references, or compact data modules.

### Type Scale
| Role | Size | Weight | Line Height | Notes |
|------|------|--------|-------------|------|
| Hero Feature Title | 52-64px | 700 | 1.02-1.08 | Large serif, tight leading |
| Section Lead Title | 34-42px | 700 | 1.1 | Serif preferred |
| Article Headline | 28-36px | 700 | 1.12 | Sharp, compressed feel |
| Deck / Standfirst | 20-24px | 400-500 | 1.4 | Calm explanatory text |
| Section Label | 11-13px | 700 | 1.2 | Sans, uppercase, letter-spaced |
| Body Large | 19-21px | 400 | 1.65 | Longform reading |
| Body Standard | 16-18px | 400 | 1.65 | Default article/body copy |
| UI Label | 13-14px | 500-600 | 1.4 | Controls, tabs, metadata |
| Caption / Meta | 12-13px | 400-500 | 1.35 | Date, source, byline, chart notes |
| Data Number XL | 36-48px | 700 | 1.0 | KPI/stat callouts |

### Typography Behavior
- Headlines should feel **edited**, not oversized startup hero copy.
- Keep body text highly readable with generous line height.
- Uppercase labels should be compact and restrained.
- Use serif selectively for editorial authority; not every heading needs serif.
- Avoid rounded, friendly, bubbly fonts.

---

## 4. Component Stylings

### Buttons
#### Primary Button
- Background: `#E3120B`
- Text: white
- Radius: `0px` to `4px` max
- Padding: `10px 16px`
- Font: sans, `13-14px`, `600`
- Hover: darken to `#C10F09`
- Feel: sharp, news-desk efficient

#### Secondary Button
- Background: transparent or `#F7F5F2`
- Border: `1px solid #111111` or `#D9D4CD`
- Text: `#111111`
- Hover: subtle fill to `#F1EEEA`

### Cards
- Border radius: `0-6px`
- Border: `1px solid #D9D4CD`
- Background: white or `#F7F5F2`
- Shadow: almost none; rely on border and spacing
- Typical use: article teasers, data callouts, briefing tiles

### Navigation
- Minimal, orderly, publication-like
- Horizontal nav with strong alignment and clear spacing
- Active state marked by red underline, red text, or black-to-red transition
- Sticky header acceptable if visually quiet

### Tabs / Section Switchers
- Use editorial rule lines rather than pill tabs
- Active tab can use:
  - red top/bottom rule
  - bold black text
  - small red marker block

### Inputs / Search
- High clarity, low decoration
- White background, black text
- `1px` gray or black border
- Focus state: black or red outline, no glowing shadows
- Placeholder text should remain readable, not too faint

### Tables
- Extremely important to this style
- Use fine horizontal rules
- Strong header row contrast
- Right-align numeric columns
- No excessive striping; use spacing and rules instead

### Quotes / Pull Quotes
- Serif text
- Large but controlled
- Left red rule or subtle top/bottom rules
- Surround with generous whitespace

### Charts / Data Modules
- White or off-white background
- Fine gridlines in neutral gray
- One red series max unless highlighting comparison
- Clear labels directly on chart when possible
- Source note and date footnote always visible

---

## 5. Layout Principles

### Grid System
- Use a disciplined **editorial grid**
- Recommended desktop grid: `12 columns`
- Article pages may use:
  - 2-column asymmetric layouts
  - main text column + side note rail
  - modular stacked sections separated by horizontal rules

### Width Guidance
- Main content width: `720-840px` for reading-heavy pages
- Feature pages may extend to `1200-1280px`
- Side rails should be narrow and information-dense

### Spacing Scale
| Token | Value |
|------|------|
| xs | 4px |
| sm | 8px |
| md | 12px |
| lg | 16px |
| xl | 24px |
| 2xl | 32px |
| 3xl | 48px |
| 4xl | 64px |
| 5xl | 96px |

### Spatial Behavior
- Use whitespace to separate ideas, not to create emptiness for its own sake
- Sections often separated by rules instead of giant empty gaps
- Dense pages are acceptable if hierarchy is excellent
- Align baselines and card edges carefully; precision matters

### Editorial Patterns
- Section kicker above headline
- Byline + date + reading time row
- Standfirst under headline
- Inline charts and sidebars inside longform
- Briefing lists with short summaries and metadata
- Numbered insights / key takeaways panels

---

## 6. Depth & Elevation

### Elevation Philosophy
Economist-like design is mostly **flat, print-derived, and structural**.
Depth comes from **layering, section contrast, borders, and typographic scale**, not from soft floating cards.

### Shadow System
| Level | Shadow | Usage |
|------|--------|------|
| Level 0 | none | Most surfaces |
| Level 1 | `0 1px 2px rgba(17,17,17,0.04)` | Rare hover cards |
| Level 2 | `0 4px 16px rgba(17,17,17,0.06)` | Modals only |

### Borders & Rules
- Preferred separator: `1px solid #D9D4CD`
- Heavy rule for major breaks: `2px solid #111111`
- Accent rule: `2px solid #E3120B`

---

## 7. Do's and Don'ts

### Do
- Use red with intention and discipline
- Build layouts that feel edited and structured
- Prioritize reading rhythm and factual clarity
- Mix serif editorial headings with sans utility text
- Use rules, metadata, and modular sections like a premium publication
- Make data visualizations clear, sober, and source-aware

### Don't
- Do not use playful startup gradients
- Do not round everything into soft consumer UI blobs
- Do not use oversized CTA-first hero sections that feel like SaaS landing pages
- Do not over-animate charts, cards, or headlines
- Do not rely on shadows for hierarchy
- Do not use more than one loud accent color system
- Do not make article pages feel sparse, airy, or lifestyle-blog-like

---

## 8. Responsive Behavior

### Breakpoints
| Size | Range | Behavior |
|------|------|----------|
| Mobile | `< 640px` | Collapse to single-column, preserve hierarchy |
| Tablet | `640px - 1023px` | Reduce rails, stack modules, simplify nav |
| Desktop | `1024px - 1439px` | Full editorial grid |
| Wide | `1440px+` | Add side rails and expanded data modules |

### Mobile Rules
- Preserve section labels, byline, and standfirst
- Headlines can remain serif but reduce sharply in size
- Tables should become scroll containers or card summaries
- Charts must prioritize legibility over density
- Tap targets: minimum `44px`
- Sticky bottom subscription/action bars allowed only if visually restrained

### Responsive Priorities
1. Headline hierarchy
2. Body readability
3. Data clarity
4. Section navigation
5. Secondary modules / related content

---

## 9. Agent Prompt Guide

### Quick Design Summary
Create interfaces that feel like a premium international affairs and business publication: disciplined white backgrounds, black editorial typography, restrained serif headlines, crisp sans-serif metadata, signature Economist red accents, fine gray rules, analytical tables, and modular report-style layouts.

### Use This Style For
- Magazine-style article pages
- Daily briefings and weekly reports
- Market, policy, and strategy dashboards
- Longform explainers
- Research landing pages
- Election / macro / industry analysis pages

### Avoid This Style For
- Youthful social apps
- Playful consumer brands
- High-gloss 3D marketing pages
- Neon cyberpunk dashboards
- Soft rounded wellness / lifestyle products

### Ready-to-Use Prompt
```txt
Design this page in an Economist-inspired editorial style: use a white or warm off-white canvas, black and charcoal typography, restrained serif headlines, sans-serif metadata and controls, fine rule-based separation, disciplined spacing, dense but readable information layout, and sparing use of signature red for highlights, active states, and key data emphasis. The result should feel analytical, credible, premium, and publication-led rather than like a SaaS landing page.
```

### Optional Variants
#### Variant A — Print-Forward
- More serif
- Stronger rules and section dividers
- Tighter article column
- Fewer card metaphors

#### Variant B — Digital Briefing
- More sans-serif UI
- Modular summary cards
- Slightly more whitespace
- Cleaner chart containers and dashboard blocks

#### Variant C — Policy / Intelligence Dashboard
- Strong tables and data modules
- Red used only for critical emphasis
- Dark header band acceptable
- More compact navigation and filters

---

## 10. Implementation Hints for AI Agents

### HTML/CSS Direction
- Prefer CSS variables for all palette tokens
- Use a serif class for editorial headlines and pull quotes
- Default everything else to sans-serif
- Keep border radius low across the system
- Use top and bottom rules to organize sections
- Use content max-widths appropriate for reading

### Suggested CSS Variables
```css
:root {
  --economist-red: #E3120B;
  --economist-red-dark: #C10F09;
  --ink-black: #111111;
  --editorial-charcoal: #2A2A2A;
  --paper-white: #FFFFFF;
  --newsprint: #F7F5F2;
  --rule-gray: #D9D4CD;
  --caption-gray: #6B6B6B;
  --data-gray: #B9B4AD;
  --slate-blue: #48627A;
  --forest-graph: #2F6B55;
  --amber-briefing: #C98A2E;
}
```

### Starter Component Heuristics
- Headline blocks: serif, bold, narrow max-width
- Metadata rows: sans, compact, gray, uppercase labels optional
- Buttons: mostly rectangular, compact, red only when important
- Cards: thin rules, almost no shadows
- Data modules: title + number + small chart + source note

---

## 11. Canonical Page Pattern

### Homepage / Briefing Frontpage
1. Thin utility bar
2. Publication masthead / brand strip
3. Lead feature with serif headline
4. Secondary story grid
5. Markets / briefing / data strip
6. Topic sections separated by rules
7. Opinion / analysis rail
8. Footer with compact navigation

### Article Page
1. Section label
2. Large serif headline
3. Standfirst
4. Byline / date / share row
5. Hero image or chart (optional)
6. Main reading column
7. Inline data callouts / side notes
8. Related reading
9. Source / footer notes

---

## 12. One-Sentence Essence

If in doubt, make it feel like **a world-class weekly briefing magazine translated into modern web UI: authoritative, economical, red-accented, typographically disciplined, and built for intelligent reading.**
