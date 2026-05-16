# wechat-design-html

> Markdown → 微信公众号兼容的内联样式 HTML，附 15 个从 [voltagent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) 衍生的品牌主题。纯单文件 Python，零依赖。

[English](README.md) · MIT License

---

## 这是什么

一个 Claude Code skill：把 Markdown 文件转成 `<section>...</section>` HTML 片段，可以直接粘贴到公众号编辑器的「源代码模式」(`<>`)。所有样式都用 inline `style=""` 写在标签上 —— 没有 `<style>` 标签、没有 `class`、没有 `id`、没有外部 CSS，完整通过公众号 HTML 白名单。

16 个主题是从 voltagent/awesome-design-md（MIT）里的品牌 DESIGN.md 派生而来。每个主题保留品牌的标志强调色 + 合理的中性配色，并降级到公众号实际能渲染的子集。

## 这**不是**什么

- 不做草稿上传。输出是 HTML，自己粘贴。要上传请配合 [md2wechat](https://github.com/JimLiu/md2wechat-toolkit) 或同类 skill（如 `wechat-publish`）使用。
- 不是高保真品牌复刻。公众号会剥掉渐变、自定义字体（Geist/Copernicus/Sohne 都加载不了）、深色 surface 和动画。**你拿到的是品牌"近似的气质"**，不是像素级还原。气质体现在强调色、正文行距与字体 fallback 链上。
- 不做代码高亮 / 数学公式 / Mermaid。需要这些请用 [JimLiu/baoyu-skills 的 `baoyu-markdown-to-html`](https://github.com/JimLiu/baoyu-skills) —— 它是正确工具。

## 安装

```bash
git clone https://github.com/brucecbi/wechat-design-html.git
ln -s "$PWD/wechat-design-html" ~/.claude/skills/wechat-design-html
```

完事。Python 3.8+ 标准库即可。

## 快速上手

```bash
# 列出 16 个主题
python3 ~/.claude/skills/wechat-design-html/scripts/generate_wechat_html.py --list-themes

# 用 Stripe 主题转换文章
python3 ~/.claude/skills/wechat-design-html/scripts/generate_wechat_html.py article.md -t stripe -o article.html

# 渲染单页主题样张（用于挑主题）
python3 ~/.claude/skills/wechat-design-html/scripts/generate_wechat_html.py --preview-theme posthog > preview.html
```

公众号后台操作：

1. 新建图文 → 编辑器工具栏 `<>` 进入源代码模式
2. 粘贴 HTML
3. 再点 `<>` 退回可视化模式预览
4. 图片：脚本会插入占位符。在可视化模式下手动上传后替换占位。

## 16 个主题

每个主题从某品牌的 DESIGN.md 派生，保守地映射到公众号安全的 inline tokens。

| ID | 强调色 | 气质 |
|---|---|---|
| `claude` | `#cc785c` 赤陶 | 米色 + 赤陶 · 衬线标题 |
| `stripe` | `#533afd` 靛紫 | 靛紫 + 深海军蓝 · 冷白底 |
| `vercel` | `#000000` 纯黑 | 黑白克制 |
| `apple` | `#0066cc` 系统蓝 | 苹果蓝 · 美术馆精度 |
| `linear` | `#5e6ad2` 薰衣紫 | 技术派工艺感（亮色变体） |
| `notion` | `#5645d4` 紫 | 知识库编辑感 |
| `figma` | `#f24e1e` 红 | 编辑式自信 |
| `airbnb` | `#ff385c` Rausch 珊瑚 | 温暖消费品 |
| `slack` | `#4a154b` 茄紫 | 企业级沉稳 |
| `mintlify` | `#00d4a4` 薄荷绿 | 文档优先 · 清晰 |
| `resend` | `#ff801f` 强调橙 | 极简开发者（亮色变体） |
| `supabase` | `#3ecf8e` 翡翠绿 | 开源洁净 |
| `cal` | `#111111` 近黑 | 预约级极简 |
| `posthog` | `#f7a501` 黄橙 | **米色底 · 顽皮工程感** |
| `framer` | `#0099ff` 蓝 | 海报级紧致（亮色变体） |
| `minimal` | `#333333` 中性 | 无品牌基线 · 纯黑白 |

Linear / Resend / Framer 三个品牌的官网主色是深色，但长文在深色公众号阅读对眼睛不友好，因此本仓库提供**亮色诠释**，保留品牌的标志强调色。

## Frontmatter

```markdown
---
title: 文章标题
author: 作者名
date: 2026 年 5 月
series: 系列标签 · 副标题
disclaimer: 文末免责声明
---

正文从这里开始...
```

全部字段可选。

## 自定义主题

把符合 schema 的 JSON 文件放到 `themes/` 目录，或者用绝对路径传给 `-t`：

```bash
python3 .../generate_wechat_html.py article.md -t ./my-theme.json -o out.html
```

必需字段：

```json
{
  "id": "my-theme",
  "name": "My Theme",
  "source": "（可选：URL 或归属信息）",
  "description": "（可选：一行描述）",
  "preview": "（可选：--list-themes 显示的简介）",
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

可选字段：`text_2` / `accent_light` / `accent_border` / `accent_bg`（不传则按合理默认推导）。

从 voltagent/awesome-design-md 拉一个新品牌作为起点：

```bash
python3 tools/derive_theme_from_design_md.py airbnb > themes/airbnb.json
# 然后人工 review 配色、设置 preview 标语、压缩 description
```

## 工具选型对照

| 需求 | 推荐 |
|---|---|
| 品牌主题化的公众号文章，零依赖 | **本 skill** |
| 代码高亮 / 数学 / Mermaid / PlantUML | [JimLiu/baoyu-skills 的 `baoyu-markdown-to-html`](https://github.com/JimLiu/baoyu-skills)（TS，依赖 bun） |
| 草稿上传到公众号后台 | [JimLiu/baoyu-skills 的 `baoyu-post-to-wechat`](https://github.com/JimLiu/baoyu-skills) 或 `wechat-publish` |
| 封面 / 信息图 / 去除 AI 痕迹 | [md2wechat](https://github.com/JimLiu/md2wechat-toolkit) |
| 浏览器 GUI 编辑器 | [doocs/md](https://github.com/doocs/md) |

如果你想要功能全的全家桶，baoyu-skills 更成熟，推荐用它。本 skill 服务的是更窄的场景：**想要品牌质感的内联样式 HTML，且不想引入 Node/bun，且希望整个转换逻辑五分钟之内能审计完一遍**。

## CLI 参数

```
generate_wechat_html.py [INPUT.md] [options]

  -t, --theme <id|path>      主题 id 或自定义主题 JSON 路径（默认 claude）
  -o, --output <path>        输出 HTML 路径（默认 stdout）
      --list-themes          列出全部主题后退出
      --preview-theme <id>   渲染内置样张文章
  -s, --style <id>           [deprecated] --theme 的旧别名；v3 删除
```

## 测试

```bash
python3 tests/test_inline_md.py     # 不需要装 pytest
# 或
python3 -m pytest tests/
```

## 致谢

15 个品牌主题派生自 [voltagent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)（MIT）。详见 [ATTRIBUTION.md](ATTRIBUTION.md) 的逐品牌来源链接。品牌名与视觉系统归属各自所有者；本项目把公开记载的色彩 token 作为**参考**使用，不主张任何关联或背书。

## License

MIT — 见 [LICENSE](LICENSE)。
