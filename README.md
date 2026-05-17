# wechat-design-html

> Markdown → WeChat Official Account inline-style HTML, with 17 design themes — 15 brand-mapped from [voltagent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md), 1 editorial-style original (`economist`), 1 neutral baseline (`minimal`). Single-file Python, zero dependencies.

[简体中文](README.zh.md) · MIT License

---

## What this is

A Claude Code skill that converts a Markdown file into a `<section>...</section>` HTML snippet you can paste straight into the WeChat Official Account editor's "source code mode" (`<>`). Every style is inlined — no `<style>` tag, no `class`, no `id`, no external CSS — so it survives WeChat's HTML whitelist intact.

15 of the 17 themes are mapped from the brand DESIGN.md files in voltagent/awesome-design-md (MIT). Each takes the brand's signature accent + a sensible neutral palette, degraded into the subset WeChat will actually render. The `economist` theme is an original DESIGN.md interpretation included in this repo, and `minimal` is a neutral baseline.

## What this is **not**

- Not a draft uploader. Output is HTML you paste yourself. For upload, compose with [md2wechat](https://github.com/JimLiu/md2wechat-toolkit) or a sibling Claude Code skill like `wechat-publish`.
- Not high-fidelity brand replication. WeChat strips gradients, custom fonts (Geist/Copernicus/Sohne never load), dark surfaces, and animations. You get **approximately the brand's character**, not a pixel-faithful reproduction. The vibe is in the accent color, the body proportions, and the font fallback chain.
- Not a code-highlighter / math-renderer / mermaid pipeline. If you need any of those, use [JimLiu/baoyu-skills `baoyu-markdown-to-html`](https://github.com/JimLiu/baoyu-skills) — it's the right tool.

## Install

```bash
git clone https://github.com/brucecbi/wechat-design-html.git
ln -s "$PWD/wechat-design-html" ~/.claude/skills/wechat-design-html
```

That's it. Python 3.8+ stdlib only.

## Quickstart

```bash
# List the 17 themes
python3 ~/.claude/skills/wechat-design-html/scripts/generate_wechat_html.py --list-themes

# Convert article.md using the Stripe theme
python3 ~/.claude/skills/wechat-design-html/scripts/generate_wechat_html.py article.md -t stripe -o article.html

# Render a one-page theme preview (great for picking)
python3 ~/.claude/skills/wechat-design-html/scripts/generate_wechat_html.py --preview-theme posthog > preview.html
```

Then in the WeChat backend:

1. New article → editor toolbar `<>` (source code mode)
2. Paste the HTML
3. Click `<>` again to exit source mode and preview
4. Images: the script inserts placeholders. Replace them by uploading via the visual editor.

## Themes (17)

Each theme is derived from a brand's DESIGN.md, conservatively mapped to WeChat-safe inline tokens.

| ID | Accent | Vibe |
|---|---|---|
| `claude` | `#cc785c` terracotta | Cream + terracotta · serif headlines |
| `economist` | `#e3120b` red | **Newsprint cream + signature red · authoritative editorial** |
| `stripe` | `#533afd` indigo | Indigo + navy ink · cool white canvas |
| `vercel` | `#000000` pure black | Black on white · disciplined minimalism |
| `apple` | `#0066cc` system blue | Apple blue · museum-precision |
| `linear` | `#5e6ad2` lavender violet | Technical software-craft (light variant) |
| `notion` | `#5645d4` purple | Knowledge-base editorial |
| `figma` | `#f24e1e` red | Editorial confidence |
| `airbnb` | `#ff385c` Rausch coral | Warm consumer hospitality |
| `slack` | `#4a154b` aubergine | Enterprise messaging |
| `mintlify` | `#00d4a4` mint green | Documentation-first clarity |
| `resend` | `#ff801f` accent-orange | Monochrome developer minimal (light variant) |
| `supabase` | `#3ecf8e` emerald | Open-source clean |
| `cal` | `#111111` near-black | Booking-grade minimalism |
| `posthog` | `#f7a501` yellow-orange | Playful engineering on cream canvas |
| `framer` | `#0099ff` blue | Poster-tight precision (light variant) |
| `minimal` | `#333333` neutral | No-brand baseline · pure B&W |

Brands shipped with **light interpretations** (Linear, Resend, Framer) because their canonical surface is dark; reading long-form on a black WeChat article is unkind to most readers. The signature accent is preserved.

The `economist` theme is the one theme not derived from voltagent/awesome-design-md — its source DESIGN.md is an original interpretation included in this repo at [`docs/economist-design.md`](docs/economist-design.md). See [ATTRIBUTION.md](ATTRIBUTION.md) for the trademark / no-affiliation note.

## Frontmatter

```markdown
---
title: 文章标题
author: Author Name
date: 2026 年 5 月
series: Series tag · 副标题
disclaimer: Footer disclaimer
---

正文从这里开始...
```

All fields optional.

## Custom themes

Drop a JSON file matching the schema into `themes/` (or pass an absolute path to `-t`):

```bash
python3 .../generate_wechat_html.py article.md -t ./my-theme.json -o out.html
```

Required schema:

```json
{
  "id": "my-theme",
  "name": "My Theme",
  "source": "(optional URL or attribution string)",
  "description": "(optional one-line description)",
  "preview": "(optional tagline shown in --list-themes)",
  "style": {
    "accent": "#xxxxxx",
    "text": "#xxxxxx",
    "text_dark": "#xxxxxx",
    "text_light": "#xxxxxx",
    "text_muted": "#xxxxxx",
    "bg": "#xxxxxx",
    "card_bg": "#xxxxxx",
    "border": "#xxxxxx",
    "border_light": "#xxxxxx",
    "font_heading": "...",
    "font_body": "...",
    "font_mono": "..."
  }
}
```

Optional: `text_2`, `accent_light`, `accent_border`, `accent_bg` (sensible defaults derived if omitted).

To pull a new brand from voltagent/awesome-design-md as a starting point:

```bash
python3 tools/derive_theme_from_design_md.py airbnb > themes/airbnb.json
# Then hand-review color picks, set `preview` tagline, shorten `description`.
```

## Where this sits vs other tools

| Need | Best tool |
|---|---|
| Brand-themed WeChat article, zero deps | **this skill** |
| Code highlighting + math + mermaid + PlantUML | [JimLiu/baoyu-skills `baoyu-markdown-to-html`](https://github.com/JimLiu/baoyu-skills) (TypeScript, requires bun) |
| Draft upload to WeChat backend | [JimLiu/baoyu-skills `baoyu-post-to-wechat`](https://github.com/JimLiu/baoyu-skills) or `wechat-publish` |
| Cover image / infographic / AI-trace removal | [md2wechat](https://github.com/JimLiu/md2wechat-toolkit) |
| Browser-based GUI editing | [doocs/md](https://github.com/doocs/md) |

If you need the full feature set, baoyu-skills is the more mature choice and you should probably use it. This skill exists for the specific case where you want brand-themed inline-style HTML with no Node/bun toolchain and the option to read every line of the converter in five minutes.

## CLI reference

```
generate_wechat_html.py [INPUT.md] [options]

  -t, --theme <id|path>      Theme id or path to custom theme JSON (default: claude)
  -o, --output <path>        Write HTML to file (default: stdout)
      --list-themes          List all themes and exit
      --preview-theme <id>   Render a built-in sample article with the theme
  -s, --style <id>           [deprecated] Alias for --theme; will be removed in v3
```

## Testing

```bash
python3 tests/test_inline_md.py     # no pytest required
# or
python3 -m pytest tests/
```

## Attribution

15 of the brand themes are derived from [voltagent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) (MIT). The `economist` theme is an original DESIGN.md interpretation included in this repo at [`docs/economist-design.md`](docs/economist-design.md). See [ATTRIBUTION.md](ATTRIBUTION.md) for per-brand source links and the Economist-trademark / no-affiliation note. Brand names and visual identities are property of their respective owners; this project uses publicly-documented color tokens as a *reference* and does not claim affiliation.

## License

MIT — see [LICENSE](LICENSE).
