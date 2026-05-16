"""Regression tests for three inline-Markdown bugs caught during pre-release dev.

Run from the repo root:

    python3 -m pytest tests/
    # or, if pytest isn't installed:
    python3 tests/test_inline_md.py

Tests cover:
  1. Inline code substitution must not produce \x01 control chars (raw-string bug).
  2. URLs containing underscores must not be corrupted by the italic underscore regex.
  3. Inline code containing __dunder__ must be preserved verbatim (placeholder protection).
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from generate_wechat_html import (  # noqa: E402
    _inline_md,
    generate_article_html,
    load_themes,
    parse_frontmatter,
)

THEMES = load_themes()
CLAUDE = THEMES["claude"]["style"]


# --- Bug 1: inline-code substitution producing \x01 ---------------------------

def test_inline_code_does_not_emit_control_char():
    """The original v1.0 bug: replacement string `r'...' + FONT + '\1...'` had
    the trailing segment as non-raw, so `\1` was parsed as octal escape \x01."""
    out = _inline_md("variable `accent_light` here", CLAUDE)
    assert "\x01" not in out
    assert ">accent_light<" in out


def test_inline_code_preserves_content():
    out = _inline_md("Run `python3 script.py --flag value`", CLAUDE)
    assert ">python3 script.py --flag value<" in out


# --- Bug 2: URL with underscores corrupted by italic regex --------------------

def test_url_with_underscore_intact():
    md = "[Anthropic](https://docs.anthropic.com/path/with_underscore_segments)"
    out = _inline_md(md, CLAUDE)
    assert 'href="https://docs.anthropic.com/path/with_underscore_segments"' in out
    # The italic <em> tag must not have invaded the href value
    assert "<em>" not in out.split('href="')[1].split('"')[0]


def test_multiple_urls_with_underscores():
    md = "See [A](https://a.com/foo_bar) and [B](https://b.com/x_y_z) for details."
    out = _inline_md(md, CLAUDE)
    assert 'href="https://a.com/foo_bar"' in out
    assert 'href="https://b.com/x_y_z"' in out


def test_italic_underscore_still_works_in_prose():
    """Word-boundary lookaround must not break legit `_italic_` usage."""
    out = _inline_md("This is _emphasized_ text.", CLAUDE)
    assert "<em>emphasized</em>" in out


# --- Bug 3: inline code with __dunder__ corrupted by bold regex ---------------

def test_inline_code_with_dunder_preserved():
    """`__init__` inside backticks must survive the bold __..__ regex."""
    out = _inline_md("Python's `__init__` method", CLAUDE)
    assert ">__init__<" in out
    assert "<strong" not in out


def test_inline_code_with_bold_markers_preserved():
    out = _inline_md("Markdown: `**not bold here**`", CLAUDE)
    assert ">**not bold here**<" in out


def test_inline_code_with_link_syntax_preserved():
    out = _inline_md("Markdown: `[label](url)`", CLAUDE)
    assert ">[label](url)<" in out
    assert "<a href" not in out


# --- WeChat whitelist compliance (defensive) ----------------------------------

def test_output_has_no_class_attributes():
    md = "# Title\n\nA paragraph with `code` and *italic* and **bold** and [link](https://x.com)."
    out = _inline_md(md, CLAUDE)
    assert " class=" not in out


def test_full_article_has_no_forbidden_constructs():
    """Article-level: no <style>, <script>, class=, id=, or null/control chars."""
    md = (
        "---\ntitle: Test\n---\n\n"
        "# Heading\n\nBody with `code`, **bold**, *italic*, [link](https://example.com/a_b).\n\n"
        "> Quote with `__init__`.\n\n"
        "| Col1 | Col2 |\n|------|------|\n| `inline_code` | **bold** |\n"
    )
    meta, body = parse_frontmatter(md)
    html = generate_article_html(body, THEMES["claude"], meta)
    for forbidden in ("<style", "<script", " class=", " id=", "\x00", "\x01"):
        assert forbidden not in html, f"unexpected {forbidden!r} in output"


# --- Theme loading ------------------------------------------------------------

def test_all_themes_have_required_tokens():
    required = {
        "accent", "text", "text_dark", "text_light", "text_muted",
        "bg", "card_bg", "border", "border_light",
        "font_heading", "font_body", "font_mono",
    }
    for tid, theme in THEMES.items():
        missing = required - theme["style"].keys()
        assert not missing, f"theme {tid!r} missing tokens: {missing}"


def test_theme_ids_match_filenames():
    themes_dir = ROOT / "themes"
    for path in themes_dir.glob("*.json"):
        theme = THEMES.get(path.stem)
        assert theme is not None, f"theme {path.stem!r} failed to load"
        assert theme["id"] == path.stem


def test_theme_count():
    """Sanity: shipping with the documented 15 brand themes + minimal."""
    assert len(THEMES) >= 16, f"expected at least 16 themes, got {len(THEMES)}"


if __name__ == "__main__":
    # Allow `python3 tests/test_inline_md.py` without pytest installed
    import inspect
    failures = 0
    tests = [
        (name, fn) for name, fn in globals().items()
        if name.startswith("test_") and callable(fn)
    ]
    for name, fn in tests:
        try:
            fn()
            print(f"  ✓ {name}")
        except AssertionError as e:
            print(f"  ✗ {name}: {e}")
            failures += 1
        except Exception as e:
            print(f"  ✗ {name}: {type(e).__name__}: {e}")
            failures += 1
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    sys.exit(1 if failures else 0)
