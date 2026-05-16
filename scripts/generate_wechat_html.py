#!/usr/bin/env python3
"""
wechat-design-html — Markdown → 微信公众号兼容的内联样式 HTML

用法:
    python3 generate_wechat_html.py input.md [-o output.html] [-t THEME]
    python3 generate_wechat_html.py --list-themes
    python3 generate_wechat_html.py --preview-theme THEME

主题从 ../themes/*.json 加载。每个 JSON 必须包含 id / name / style 字段；style 至少包含
accent / text / text_dark / text_light / text_muted / bg / card_bg / border / border_light /
font_heading / font_body / font_mono。可选 accent_light / accent_border / accent_bg / text_2。
"""

import os
import re
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

THEMES_DIR = Path(__file__).resolve().parent.parent / "themes"


def load_themes(themes_dir: Path = THEMES_DIR):
    """Load all themes from JSON files. Returns dict keyed by theme id."""
    themes = {}
    if not themes_dir.exists():
        return themes
    for path in sorted(themes_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"warning: theme {path.name} JSON parse failed: {e}", file=sys.stderr)
            continue
        tid = data.get("id")
        style = data.get("style")
        if not tid or not isinstance(style, dict):
            print(f"warning: theme {path.name} missing id or style", file=sys.stderr)
            continue
        if tid != path.stem:
            print(f"warning: theme {path.name} id={tid!r} != filename stem", file=sys.stderr)
        themes[tid] = data
    return themes


def load_theme_from_path(path: Path):
    """Load a single theme from an explicit JSON path (for --theme ./custom.json)."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data.get("id") or not isinstance(data.get("style"), dict):
        raise ValueError(f"{path} missing id or style")
    return data


def resolve_theme(theme_arg, themes):
    """Resolve --theme argument: either a theme id or a path to a JSON file."""
    if theme_arg in themes:
        return themes[theme_arg]
    p = Path(theme_arg)
    if p.exists() and p.suffix == ".json":
        return load_theme_from_path(p)
    raise SystemExit(
        f"error: unknown theme {theme_arg!r}. Available: {', '.join(sorted(themes)) or '(none)'}"
    )


def parse_frontmatter(text):
    """Parse simple frontmatter (key: value pairs between two `---` lines)."""
    meta = {}
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            fm = text[3:end].strip()
            for line in fm.split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    meta[key.strip()] = val.strip().strip('"').strip("'")
            text = text[end+3:].strip()
    return meta, text


def md_to_html(text, s):
    """Convert Markdown body to inline-styled HTML using theme dict `s`."""
    lines = text.split('\n')
    html_parts = []
    i = 0
    in_list = False
    list_items = []
    list_ordered = False
    in_table = False
    table_rows = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            if in_list:
                html_parts.append(_render_list(list_items, list_ordered, s))
                list_items = []
                in_list = False
            if in_table:
                html_parts.append(_render_table(table_rows, s))
                table_rows = []
                in_table = False
            i += 1
            continue

        if stripped == '---':
            i += 1
            continue

        if stripped.startswith('# '):
            title = stripped[2:].strip()
            html_parts.append(
                f'<h1 style="font-family:{s["font_heading"]};font-size:26px;color:{s["text_dark"]};text-align:center;line-height:1.3;margin:0 0 10px;font-weight:700;letter-spacing:1px;">{_inline_md(_esc(title), s)}</h1>'
            )
            i += 1
            continue

        if stripped.startswith('## '):
            if in_list:
                html_parts.append(_render_list(list_items, list_ordered, s))
                list_items = []
                in_list = False
            title = stripped[3:].strip()
            html_parts.append(
                f'<h2 style="font-family:{s["font_heading"]};font-size:20px;color:{s["text_dark"]};line-height:1.4;margin:0 0 14px;font-weight:700;">{_inline_md(_esc(title), s)}</h2>'
            )
            i += 1
            continue

        if stripped.startswith('### '):
            if in_list:
                html_parts.append(_render_list(list_items, list_ordered, s))
                list_items = []
                in_list = False
            title = stripped[4:].strip()
            html_parts.append(
                f'<h3 style="font-family:{s["font_body"]};font-size:16px;color:{s["text_dark"]};line-height:1.5;margin:0 0 14px;font-weight:700;">{_inline_md(_esc(title), s)}</h3>'
            )
            i += 1
            continue

        if stripped.startswith('> '):
            if in_list:
                html_parts.append(_render_list(list_items, list_ordered, s))
                list_items = []
                in_list = False
            quote_text = stripped[2:].strip()
            text_2 = s.get('text_2', s['text'])
            accent_light = s.get('accent_light', 'rgba(0,0,0,0.04)')
            html_parts.append(
                f'<section style="border-left:3px solid {s["accent"]};padding:12px 16px;margin:0 0 16px;background-color:{accent_light};border-radius:0 6px 6px 0;">'
                f'<p style="font-family:{s["font_heading"]};font-size:15px;color:{text_2};line-height:1.8;margin:0;font-style:italic;">{_inline_md(quote_text, s)}</p>'
                f'</section>'
            )
            i += 1
            continue

        if stripped.startswith('|') and '|' in stripped[1:]:
            if in_list:
                html_parts.append(_render_list(list_items, list_ordered, s))
                list_items = []
                in_list = False
            if not stripped.startswith('|--') and not stripped.startswith('| ---'):
                cells = [c.strip() for c in stripped.split('|')[1:-1]]
                table_rows.append(cells)
            in_table = True
            i += 1
            continue
        elif in_table:
            html_parts.append(_render_table(table_rows, s))
            table_rows = []
            in_table = False

        if stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list:
                in_list = True
                list_ordered = False
            item_text = stripped[2:].strip()
            list_items.append(item_text)
            i += 1
            continue

        if re.match(r'^\d+\.\s', stripped):
            if not in_list:
                in_list = True
                list_ordered = True
            item_text = re.sub(r'^\d+\.\s+', '', stripped)
            list_items.append(item_text)
            i += 1
            continue

        if stripped == '---' or stripped == '***' or stripped == '___':
            if in_list:
                html_parts.append(_render_list(list_items, list_ordered, s))
                list_items = []
                in_list = False
            html_parts.append(
                f'<section style="width:40px;height:2px;background-color:{s["border"]};margin:24px auto;border-radius:1px;"></section>'
            )
            i += 1
            continue

        img_match = re.match(r'^!\[(.*?)\]\((.*?)\)$', stripped)
        if img_match:
            alt, src = img_match.groups()
            html_parts.append(
                f'<!-- 图片占位：请在公众号可视化模式下手动上传并替换 -->\n'
                f'<p style="text-align:center;margin:16px 0;">'
                f'<img src="{src}" alt="{alt}" style="max-width:100%;border-radius:8px;display:block;margin:0 auto;box-shadow:0 4px 6px rgba(0,0,0,0.15);">'
                f'</p>'
            )
            i += 1
            continue

        if in_list:
            html_parts.append(_render_list(list_items, list_ordered, s))
            list_items = []
            in_list = False
        html_parts.append(
            f'<p style="font-size:15px;color:{s["text"]};line-height:1.8;margin:0 0 12px;">{_inline_md(stripped, s)}</p>'
        )
        i += 1

    if in_list:
        html_parts.append(_render_list(list_items, list_ordered, s))
    if in_table:
        html_parts.append(_render_table(table_rows, s))

    return '\n'.join(html_parts)


def _render_list(items, ordered, s):
    tag = 'ol' if ordered else 'ul'
    style = f'style="padding-left:20px;margin:0 0 16px;list-style-type:{"decimal" if ordered else "disc"};"'
    li_html = ''
    for item in items:
        li_html += f'<li style="font-size:15px;color:{s["text"]};line-height:1.8;margin:0 0 6px;">{_inline_md(item, s)}</li>'
    return f'<{tag} {style}>{li_html}</{tag}>'


def _render_table(rows, s):
    if not rows:
        return ''
    headers = rows[0]
    data_rows = rows[1:]
    th_html = ''.join(
        f'<th style="background-color:{s["border_light"]};font-weight:600;text-align:left;padding:10px 12px;border-bottom:2px solid {s["border"]};font-size:14px;color:{s["text_dark"]};">{_inline_md(h, s)}</th>'
        for h in headers
    )
    tr_html = ''
    for row in data_rows:
        td_html = ''.join(
            f'<td style="padding:10px 12px;border-bottom:1px solid {s["border_light"]};font-size:14px;color:{s["text"]};line-height:1.6;">{_inline_md(c, s)}</td>'
            for c in row
        )
        tr_html += f'<tr>{td_html}</tr>'
    return (
        f'<section style="overflow-x:auto;margin:0 0 16px;">'
        f'<table style="width:100%;border-collapse:collapse;font-size:14px;">'
        f'<thead><tr>{th_html}</tr></thead>'
        f'<tbody>{tr_html}</tbody>'
        f'</table></section>'
    )


def _inline_md(text, s):
    """Inline markdown: code → link → bold → italic, with placeholder protection for code.

    Order rationale (see CHANGELOG):
    - Inline code stashed first so its content (which may contain `__`, `*`, `[`) is
      protected from later bold/italic/link regex passes.
    - Links before italic so URLs with underscores aren't corrupted by `_..._`.
    - Underscore forms (__bold__, _italic_) use CommonMark word-boundary lookaround.
    """
    accent = s['accent']
    code_style = (
        f'background-color:rgba(0,0,0,0.05);padding:2px 5px;border-radius:3px;'
        f'font-family:{s["font_mono"]};font-size:13px;color:#C7254E;'
    )

    code_stash = []
    def _stash(m):
        code_stash.append(m.group(1))
        return f'\x00CODE{len(code_stash) - 1}\x00'
    text = re.sub(r'`([^`]+)`', _stash, text)

    text = re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        rf'<a href="\2" style="color:{accent};text-decoration:none;border-bottom:1px solid {accent};">\1</a>',
        text,
    )
    text = re.sub(r'\*\*(.+?)\*\*', rf'<strong style="color:{accent};font-weight:700;">\1</strong>', text)
    text = re.sub(r'(?<!\w)__(.+?)__(?!\w)', rf'<strong style="color:{accent};font-weight:700;">\1</strong>', text)
    text = re.sub(r'(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'(?<!\w)_([^_\n]+?)_(?!\w)', r'<em>\1</em>', text)

    def _restore(m):
        content = code_stash[int(m.group(1))]
        return f'<code style="{code_style}">{content}</code>'
    text = re.sub(r'\x00CODE(\d+)\x00', _restore, text)
    return text


def generate_article_html(markdown_text, theme, meta=None):
    """Build the final <section>...</section> snippet from theme dict + parsed meta."""
    if isinstance(theme, str):
        themes = load_themes()
        theme = resolve_theme(theme, themes)
    s = theme["style"]
    if meta is None:
        meta = {}

    title = meta.get('title', '')
    author = meta.get('author', '')
    date = meta.get('date', datetime.now().strftime('%Y年%m月'))
    series = meta.get('series', '')

    body_html = md_to_html(markdown_text, s)

    header_html = ''
    if title or series or author:
        header_html += f'<section style="width:60px;height:3px;background-color:{s["accent"]};margin:0 auto 24px;border-radius:2px;"></section>\n'
        if series:
            header_html += f'<p style="text-align:center;font-size:12px;color:{s["accent"]};letter-spacing:3px;margin:0 0 8px;font-weight:600;">{series}</p>\n'
        if title:
            header_html += f'<h1 style="font-family:{s["font_heading"]};font-size:26px;color:{s["text_dark"]};text-align:center;line-height:1.3;margin:0 0 10px;font-weight:700;letter-spacing:1px;">{_esc(title)}</h1>\n'
        if author or date:
            header_html += f'<p style="text-align:center;font-size:13px;color:{s["text_light"]};margin:0 0 28px;">{_esc(author)}{" · " if author and date else ""}{_esc(date)}</p>\n'

    footer_html = ''
    disclaimer = meta.get('disclaimer', '')
    if disclaimer:
        footer_html += f'\n<section style="width:80px;height:1px;background-color:{s["border"]};margin:0 auto 20px;"></section>\n'
        footer_html += f'<p style="font-size:12px;color:{s["text_muted"]};line-height:1.7;text-align:center;margin:0 0 8px;">{_esc(disclaimer)}</p>\n'

    container = (
        f'<section style="max-width:100%;box-sizing:border-box;background-color:{s["bg"]};padding:30px 20px 40px;margin:0 auto;'
        f'font-family:{s["font_body"]};color:{s["text"]};line-height:1.8;letter-spacing:0.5px;font-size:15px;">\n'
        f'{header_html}'
        f'{body_html}'
        f'{footer_html}'
        f'</section>'
    )
    return container


def _esc(text):
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def cmd_list_themes(themes):
    if not themes:
        print(f"(no themes found in {THEMES_DIR})", file=sys.stderr)
        return 1
    rows = []
    for tid in sorted(themes):
        t = themes[tid]
        preview = t.get('preview') or t.get('description', '')
        rows.append((tid, t.get('name', tid), preview))
    width = max(len(r[0]) for r in rows)
    name_w = max(len(r[1]) for r in rows)
    for tid, name, preview in rows:
        print(f"  {tid:<{width}}  {name:<{name_w}}  {preview}")
    print(f"\n  (Total: {len(rows)} themes from {THEMES_DIR})", file=sys.stderr)
    return 0


def _preview_markdown():
    """Sample markdown used by --preview-theme."""
    return (
        "---\n"
        "title: 主题预览 · {theme}\n"
        "author: wechat-design-html\n"
        "series: 主题样张\n"
        "disclaimer: 本页用于检视主题色板、字体、版式。\n"
        "---\n\n"
        "## 二级标题：节奏与色彩\n\n"
        "这是一段普通正文，目的是检视字体、行高、字间距、段距是否舒适。**加粗** 与 *斜体* 各自需要清楚区分。"
        "中文与英文 mixed 段落也应当看着不别扭。可以含一个 [外链](https://example.com/path/with_underscore_segments) 看看 URL 渲染是否完整。\n\n"
        "### 三级标题：列表与代码\n\n"
        "- 无序列表第一项：示意 `inline_code` 在正文中的样子\n"
        "- 第二项：与前后段落的视觉关系\n"
        "- 第三项 `__init__`、`text_dark` 这种含下划线的标识符也应保持原样\n\n"
        "1. 有序列表第一项\n"
        "2. 第二项\n\n"
        "> 引用块：用衬线字体与左侧色边强调，常用于摘录或题词。\n\n"
        "| 列1 | 列2 | 列3 |\n"
        "|-----|-----|-----|\n"
        "| 数据 A | **加粗** | `code` |\n"
        "| 数据 B | *斜体*  | [link](https://x.com) |\n\n"
        "---\n\n"
        "尾部加一段日常段落，看页脚和分割线效果。"
    )


def cmd_preview_theme(theme_id, themes):
    if theme_id not in themes:
        # Allow path-based preview
        try:
            theme = load_theme_from_path(Path(theme_id))
        except Exception as e:
            print(f"error: cannot preview {theme_id!r}: {e}", file=sys.stderr)
            return 1
    else:
        theme = themes[theme_id]
    text = _preview_markdown().replace("{theme}", theme.get("name", theme_id))
    meta, body = parse_frontmatter(text)
    print(generate_article_html(body, theme, meta))
    return 0


def main():
    parser = argparse.ArgumentParser(
        description='Markdown → 微信公众号兼容的内联样式 HTML（基于品牌设计系统的主题）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('input', nargs='?', help='Markdown 文件路径（与 --list-themes / --preview-theme 互斥）')
    parser.add_argument('-o', '--output', help='输出 HTML 路径（默认 stdout）')
    parser.add_argument('-t', '--theme', default='claude', help='主题 id 或自定义 theme JSON 路径（默认 claude）')
    parser.add_argument('-s', '--style', help='[deprecated] --theme 的旧别名；下个 major 版本删除')
    parser.add_argument('--list-themes', action='store_true', help='列出所有可用主题并退出')
    parser.add_argument('--preview-theme', metavar='THEME', help='渲染指定主题的样张 HTML 到 stdout')
    args = parser.parse_args()

    themes = load_themes()

    if args.list_themes:
        sys.exit(cmd_list_themes(themes))

    if args.preview_theme:
        sys.exit(cmd_preview_theme(args.preview_theme, themes))

    if not args.input:
        parser.error('需要 input 参数，或使用 --list-themes / --preview-theme')

    theme_arg = args.style or args.theme
    if args.style and args.theme != 'claude':
        print(f"warning: --style 已 deprecated；以 --theme={args.theme!r} 为准", file=sys.stderr)
        theme_arg = args.theme
    elif args.style:
        print(f"warning: --style {args.style!r} 已 deprecated，请改用 --theme", file=sys.stderr)
    theme = resolve_theme(theme_arg, themes)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"错误: 文件不存在: {input_path}", file=sys.stderr)
        sys.exit(1)

    text = input_path.read_text(encoding='utf-8')
    meta, markdown_body = parse_frontmatter(text)

    html = generate_article_html(markdown_body, theme, meta)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(html, encoding='utf-8')
        print(f"已生成: {output_path}")
        print(f"  主题: {theme.get('name', theme['id'])}  ({theme['id']})")
        print(f"  标题: {meta.get('title', input_path.stem)}")
        print("\n粘贴步骤：")
        print("  1. 公众号后台 → 新建图文")
        print("  2. 编辑器「<>」进入源代码模式")
        print("  3. 全选粘贴 HTML")
        print("  4. 再点「<>」退回可视化模式预览")
        print("  5. 图片在可视化模式下手动上传替换")
    else:
        print(html)


if __name__ == '__main__':
    main()
