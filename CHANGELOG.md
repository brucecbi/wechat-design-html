# Changelog

## v1.0.0 — 2026-05-16

Initial public release.

**Themes (16)**

- 15 brand-mapped themes derived from [voltagent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) (MIT): `claude`, `stripe`, `vercel`, `apple`, `linear`, `notion`, `figma`, `airbnb`, `slack`, `mintlify`, `resend`, `supabase`, `cal`, `posthog`, `framer`.
- 1 neutral baseline theme: `minimal` (no brand attribution).
- `linear` / `resend` / `framer` ship as **light interpretations** of their canonical dark surfaces — the signature accent is preserved on a light canvas. WeChat's HTML whitelist makes long-form dark reading uncomfortable on most clients, so this is a deliberate degradation.

**Runtime**

- Single-file Python 3.8+ converter, stdlib only. Markdown → `<section>...</section>` snippet ready to paste into the WeChat editor's source-code mode.
- All styles inlined (`style=""` on every tag). No `<style>` blocks, no `class`, no `id`, no external CSS, no JS.
- Themes live in `themes/*.json` and are loaded at runtime. Custom themes: drop a JSON file into `themes/` or pass an absolute path to `-t`.
- Per-theme typography: each theme specifies `font_heading` / `font_body` / `font_mono` separately, so sans-display brands (Apple, Vercel, Stripe, ...) get sans headings while serif brands (Claude) get serif.

**CLI**

- `-t / --theme <id|path>` — primary flag for picking a theme.
- `-o / --output <path>` — write HTML to a file (default stdout).
- `--list-themes` — print all available themes with preview taglines.
- `--preview-theme <id>` — render a built-in sample article for visual theme selection.
- `-s / --style <id>` — deprecated alias for `--theme`, kept for back-compat with pre-public usage; will be removed in the next major.

**Developer tooling**

- `tools/derive_theme_from_design_md.py` — fetches a brand's `DESIGN.md` from voltagent/awesome-design-md and emits a WeChat-safe theme JSON candidate. Output is meant to be hand-reviewed before commit; the runtime stays stdlib-only.
- `tests/test_inline_md.py` — 13 pytest-compatible regression tests, runnable with or without pytest installed (`python3 tests/test_inline_md.py`).

**Pre-release bugs fixed (locked by regression tests)**

Three inline-Markdown bugs were caught in pre-release development and are now covered by `tests/test_inline_md.py`:

1. **Inline code rendered as empty `<code></code>`.** The replacement string `r'...' + FONT_MONO + '...\1...'` concatenated a non-raw trailing segment, so `\1` was parsed as octal escape `\x01` — an invisible control character. Fixed by using `rf"..."` for the whole replacement.
2. **URLs containing underscores corrupted by the italic regex.** `[x](.../with_underscore)` had its `href` invaded by `<em>` tags because `_..._` matched across the link's HTML. Fixed by (a) stashing inline code into placeholders before any other inline regex runs, (b) moving link processing before italic so URLs are safely wrapped in `href=""` first, and (c) adding CommonMark word-boundary lookarounds to `__bold__` and `_italic_`.
3. **H1/H2/H3 inconsistent escape handling.** Body headings ran `_inline_md` directly (no escape of `<`); frontmatter `title` ran `_esc`. Unified to `_inline_md(_esc(title), s)`. Also removed redundant `not startswith` clauses in heading detection.

Side benefit of the placeholder approach: `` `__init__` `` and similar dunder names inside inline code now survive the bold pass intact.

**Documentation**

- Bilingual `README.md` + `README.zh.md` with install, quickstart, full theme list, custom-theme schema, comparison vs related tools, and CLI reference.
- `ATTRIBUTION.md` with per-brand source links and the verbatim upstream MIT license preserved.
- `SKILL.md` manifest for Claude Code skill registration.
- `MIT LICENSE`.

**Scope statement**

This tool deliberately does not:
- Upload drafts to the WeChat backend (compose with `md2wechat` / `wechat-publish` / baoyu `post-to-wechat`).
- Render code highlighting / math / Mermaid (use baoyu-markdown-to-html if you need them).
- Replicate brands pixel-faithfully — WeChat strips custom fonts, gradients, dark surfaces, animations. The themes capture brand *character* (accent color, body proportions, font fallback chain), not pixel-level fidelity.
