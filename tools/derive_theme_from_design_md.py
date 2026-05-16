#!/usr/bin/env python3
"""
derive_theme_from_design_md.py — Fetch a brand's DESIGN.md from
voltagent/awesome-design-md and emit a WeChat-safe theme JSON candidate.

This is a developer tool, not used by the runtime. The output is a *candidate* —
always hand-review before committing. Many upstream tokens (proprietary fonts,
gradients, dark surfaces, multi-tier typography) do not survive WeChat's HTML
whitelist and must be degraded to the flat schema this skill consumes.

Usage:
    python3 tools/derive_theme_from_design_md.py <brand-slug> > themes/<brand>.json
    python3 tools/derive_theme_from_design_md.py --list  # list known brands

Requires: stdlib only. Network access to github.com.
"""

import sys
import re
import json
import argparse
import urllib.request
import urllib.error

UPSTREAM_RAW = "https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/{slug}/DESIGN.md"
UPSTREAM_HTML = "https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/{slug}"
LIST_API = "https://api.github.com/repos/VoltAgent/awesome-design-md/contents/design-md"

# WeChat-safe font fallback chains
SERIF_STACK = "Georgia, 'Songti SC', 'STSong', 'SimSun', serif"
SANS_STACK = "-apple-system, BlinkMacSystemFont, 'Helvetica Neue', 'PingFang SC', 'Microsoft YaHei', sans-serif"
MONO_STACK = "'Menlo', 'Consolas', 'Courier New', monospace"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "wechat-design-html-derive/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8")


def list_brands():
    data = json.loads(fetch(LIST_API))
    return sorted([it["name"] for it in data if it["type"] == "dir"])


def parse_yaml_subset(text):
    """Parse a tiny YAML subset: indented `key: "value"` pairs nested under
    top-level keys. Enough for DESIGN.md `colors:` / `typography:` blocks."""
    out = {}
    section = None
    indent = None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        # Top-level key (no indent)
        m = re.match(r"^([a-zA-Z][\w-]*)\s*:\s*$", raw)
        if m:
            section = m.group(1)
            out[section] = {}
            indent = None
            continue
        # Top-level scalar
        m = re.match(r'^([a-zA-Z][\w-]*)\s*:\s*"?([^"\n]+?)"?\s*$', raw)
        if m and section is None:
            out[m.group(1)] = m.group(2)
            continue
        # Indented key: value
        if section is None:
            continue
        m = re.match(r'^(\s+)([\w.-]+)\s*:\s*"?([^"\n]+?)"?\s*$', raw)
        if not m:
            # Nested deeper — skip; we only care about leaf key:value here
            continue
        cur_indent, key, val = m.group(1), m.group(2), m.group(3)
        if indent is None:
            indent = cur_indent
        if cur_indent == indent:
            out[section][key] = val
        # deeper-nested values are ignored on purpose
    return out


def pick(tokens, *names, default=None):
    """Return the first token whose name matches any of the given names."""
    for n in names:
        if n in tokens:
            return tokens[n]
    return default


def derive(slug, raw_md):
    # Extract frontmatter (between two `---` lines)
    if raw_md.startswith("---"):
        end = raw_md.find("\n---", 3)
        if end != -1:
            fm = raw_md[3:end]
        else:
            fm = raw_md
    else:
        fm = raw_md

    parsed = parse_yaml_subset(fm)
    colors = parsed.get("colors", {})
    typography = parsed.get("typography", {})
    name = parsed.get("name", slug.title())
    description_src = parsed.get("description", "")

    # Pick accent color
    accent = pick(colors, "primary", "accent", "brand", default="#333333")

    # Derive accent_* alpha variants from the accent hex
    accent_light = _alpha(accent, 0.06)
    accent_border = _alpha(accent, 0.2)
    accent_bg = _alpha(accent, 0.08)

    # Text tokens
    text_dark = pick(colors, "ink", "body-strong", "text-primary", "text", default="#141413")
    text = pick(colors, "body", "ink-secondary", "body-text", "text-secondary", default=text_dark)
    text_2 = pick(colors, "body-strong", "ink-secondary", "body", default=text)
    text_light = pick(colors, "muted", "ink-mute", "text-muted", "text-tertiary", default="#6c6a64")
    text_muted = pick(colors, "muted-soft", "ink-mute-2", "text-disabled", default=text_light)

    # Background
    bg = pick(colors, "canvas", "canvas-soft", "bg", "background", default="#faf9f5")
    if bg.startswith("#000") or bg.startswith("#111") or bg.startswith("#0"):
        # Likely a dark canvas — fall back to canvas-soft / off-white
        bg = pick(colors, "canvas-soft", "surface-soft", default="#fafafa")
    card_bg = pick(colors, "surface-soft", "surface-card", "card", "canvas-soft", default=bg)
    border = pick(colors, "hairline", "border", "divider", default="#e0e0e0")
    border_light = pick(colors, "hairline-soft", "border-light", default=border)

    # Heading font: look at display-* / heading-* / h1 fontFamily inside typography
    font_heading = SANS_STACK
    for k, v in typography.items():
        if any(k.startswith(p) for p in ("display", "heading", "h1", "title")):
            if isinstance(v, str) and "serif" in v.lower():
                font_heading = SERIF_STACK
                break
    # Body font is almost always sans in WeChat-safe scope
    font_body = SANS_STACK
    font_mono = MONO_STACK

    return {
        "id": slug,
        "name": name,
        "source": UPSTREAM_HTML.format(slug=slug),
        "description": description_src.strip() or f"{name} brand-mapped theme.",
        "preview": "",
        "style": {
            "accent": accent.lower(),
            "accent_light": accent_light,
            "accent_border": accent_border,
            "accent_bg": accent_bg,
            "text": text.lower() if text.startswith("#") else text,
            "text_2": text_2.lower() if text_2.startswith("#") else text_2,
            "text_dark": text_dark.lower() if text_dark.startswith("#") else text_dark,
            "text_light": text_light.lower() if text_light.startswith("#") else text_light,
            "text_muted": text_muted.lower() if text_muted.startswith("#") else text_muted,
            "bg": bg.lower() if bg.startswith("#") else bg,
            "card_bg": card_bg.lower() if card_bg.startswith("#") else card_bg,
            "border": border.lower() if border.startswith("#") else border,
            "border_light": border_light.lower() if border_light.startswith("#") else border_light,
            "font_heading": font_heading,
            "font_body": font_body,
            "font_mono": font_mono,
        },
    }


def _alpha(hex_color, alpha):
    """Convert #rrggbb (or shorter) to rgba(r,g,b,alpha)."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        return f"rgba(0,0,0,{alpha})"
    try:
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
    except ValueError:
        return f"rgba(0,0,0,{alpha})"
    return f"rgba({r},{g},{b},{alpha})"


def main():
    ap = argparse.ArgumentParser(description="Derive a WeChat-safe theme JSON from a voltagent DESIGN.md")
    ap.add_argument("slug", nargs="?", help="brand slug, e.g. 'stripe', 'linear.app'")
    ap.add_argument("--list", action="store_true", help="list available brands and exit")
    args = ap.parse_args()

    if args.list:
        for b in list_brands():
            print(b)
        return 0
    if not args.slug:
        ap.error("provide a brand slug, or use --list")

    try:
        raw = fetch(UPSTREAM_RAW.format(slug=args.slug))
    except urllib.error.HTTPError as e:
        print(f"error: {args.slug} not found ({e.code})", file=sys.stderr)
        return 1
    theme = derive(args.slug, raw)
    json.dump(theme, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
