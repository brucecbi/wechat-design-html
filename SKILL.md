---
name: wechat-design-html
description: >
  将 Markdown 文章转换为微信公众号兼容的内联样式 HTML 片段，附 16 个主题
  （15 个从 voltagent/awesome-design-md 派生的品牌主题 + 1 个中性 minimal）。
  输出 <section> 包裹的 HTML，可直接粘贴到公众号「源代码模式」。纯 Python
  stdlib、零依赖、单文件可审计。不做草稿上传（请与 md2wechat / wechat-publish
  组合使用）。
  触发词：公众号排版、微信推文、markdown转公众号、公众号html、
  微信文章排版、公众号文章生成、brand-themed wechat、wechat article html。
trigger_examples:
  - 把这个 Markdown 转成公众号文章
  - 用 Stripe 风格生成微信公众号 HTML
  - 这篇文章做成 PostHog 米色底排版
  - /wechat-design-html article.md -t notion -o wechat.html
  - 用 Claude 主题排版这篇推文
version: 1.0.0
metadata:
  homepage: https://github.com/brucecbi/wechat-design-html
  source: voltagent/awesome-design-md (MIT)
---

# WeChat Design HTML

Markdown → 微信公众号内联样式 HTML，16 个主题可选。

## 核心特性

- **纯内联样式**：所有 CSS 写在 `style=""` 中，完全符合公众号白名单
- **零外部依赖**：无 JS、无 `<style>` 标签、无外部字体 CDN
- **Frontmatter 支持**：自动提取标题、作者、日期、系列、免责声明
- **16 个主题**：从 voltagent/awesome-design-md 派生的 15 个品牌主题 + 1 个中性 minimal
- **图片占位提示**：自动标记需要在公众号可视化模式手动上传的图片位置
- **零依赖**：Python 3.8+ 标准库即可运行

## 使用方式

### 列出全部主题

```bash
python3 "$SKILL_DIR/scripts/generate_wechat_html.py" --list-themes
```

### 转换文章

```bash
python3 "$SKILL_DIR/scripts/generate_wechat_html.py" article.md -t claude -o article.html
```

### 预览某主题样张

```bash
python3 "$SKILL_DIR/scripts/generate_wechat_html.py" --preview-theme posthog > preview.html
```

### 自然语言触发示例

```
帮我把这篇文章做成公众号排版，用 Stripe 主题。 （附 Markdown 文件）
```

### 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `input` | 是* | Markdown 文件路径（与 `--list-themes`/`--preview-theme` 互斥） |
| `-o` / `--output` | 否 | 输出 HTML 路径，默认 stdout |
| `-t` / `--theme` | 否 | 主题 id 或自定义主题 JSON 路径（默认 `claude`） |
| `-s` / `--style` | 否 | `--theme` 的 deprecated 别名，v3 删除 |
| `--list-themes` | 否 | 列出所有主题并退出 |
| `--preview-theme <id>` | 否 | 渲染主题样张到 stdout |

## 主题（16 个）

| ID | 强调色 | 气质 |
|---|---|---|
| `claude` | `#cc785c` 赤陶 | 米色 + 赤陶 · 衬线标题 |
| `stripe` | `#533afd` 靛紫 | 靛紫 + 深海军蓝 · 冷白底 |
| `vercel` | `#000000` 黑 | 黑白克制 |
| `apple` | `#0066cc` 系统蓝 | 美术馆精度 |
| `linear` | `#5e6ad2` 薰衣紫 | 技术派工艺感（亮色变体） |
| `notion` | `#5645d4` 紫 | 知识库编辑感 |
| `figma` | `#f24e1e` 红 | 编辑式自信 |
| `airbnb` | `#ff385c` 珊瑚 | 温暖消费品 |
| `slack` | `#4a154b` 茄紫 | 企业级沉稳 |
| `mintlify` | `#00d4a4` 薄荷绿 | 文档优先 |
| `resend` | `#ff801f` 强调橙 | 极简开发者（亮色变体） |
| `supabase` | `#3ecf8e` 翡翠绿 | 开源洁净 |
| `cal` | `#111111` 近黑 | 预约级极简 |
| `posthog` | `#f7a501` 黄橙 | 米色底 · 顽皮工程感 |
| `framer` | `#0099ff` 蓝 | 海报级紧致（亮色变体） |
| `minimal` | `#333333` 中性 | 无品牌基线 |

## Markdown 支持

| Markdown | 输出 HTML | 样式 |
|----------|-----------|------|
| `# 标题` | `<h1>` | `font_heading` 26px 居中 |
| `## 标题` | `<h2>` | `font_heading` 20px 左对齐 |
| `### 标题` | `<h3>` | `font_body` 16px 加粗 |
| `> 引用` | `<section>` 带左边框 | 斜体 `font_heading` 15px |
| `- 列表` / `1. 列表` | `<ul>` / `<ol>` | 15px 默认间距 |
| `\|表格\|` | `<table>` | 简洁数据表 |
| `**加粗**` / `__加粗__` | `<strong>` | 主题强调色 |
| `[链接](url)` | `<a>` | 主题强调色下划线 |
| `` `代码` `` | `<code>` | 等宽 13px，下划线安全 |
| `---` | 分隔线 | 40px 短横线居中 |
| `![alt](url)` | `<img>` | 圆角阴影 + 占位提示 |
| 普通段落 | `<p>` | 15px / 1.8 行高 |

## Frontmatter 元数据

在 Markdown 文件开头添加：

```markdown
---
title: 文章标题
author: 作者名
date: 2026 年 5 月
series: 系列标签 · 副标题
disclaimer: 以上内容为个人学习笔记，非专业分析
---

正文从这里开始...
```

字段全部可选。

## 发布工作流

### Step 1: 生成 HTML

```bash
python3 generate_wechat_html.py article.md -t stripe -o article_wechat.html
```

### Step 2: 粘贴到公众号

1. 打开公众号后台 → 新建图文消息
2. 点击编辑器工具栏的「<>」进入"源代码模式"
3. 将生成的 `<section>...</section>` 全部粘贴
4. 再次点击「<>」退回可视化模式预览

### Step 3: 处理图片

- 可视化模式下删除占位提示
- 手动上传图片到微信素材库
- 替换为微信素材库链接

### Step 4: 预览检查

- iOS + Android + PC 端微信各预览一次
- 确认链接跳转正常

## 与其他 skill 的组合

本 skill **不做**草稿上传 / 封面图生成 / 代码高亮 / AI 痕迹去除。要这些功能：

- 草稿上传：`wechat-publish` 或 `JimLiu/baoyu-skills` 的 `baoyu-post-to-wechat`
- 封面 / 信息图 / 去 AI 痕迹：`md2wechat`
- 代码高亮 / 数学 / Mermaid：`JimLiu/baoyu-skills` 的 `baoyu-markdown-to-html`

## 自定义主题

把符合 schema 的 JSON 放进 `themes/` 即可被识别；或用绝对路径传给 `-t`。
schema 详见 [README.zh.md](README.zh.md#自定义主题)。

## 注意事项

1. **图片必须手动上传**：微信不支持外部图片链接，生成时会插入占位提示
2. **外链会有安全提示**：`<a>` 标签指向的外部链接会触发微信安全确认窗口
3. **不支持复杂布局**：放弃 position、grid、动画等高级 CSS
4. **class 无效**：所有样式必须内联
5. **id 会被过滤**：公众号后台会自动删除所有 id 属性
6. **品牌主题是"近似气质"**：公众号会剥掉自定义字体、渐变、深色 surface，得到的是品牌的色与排版近似，不是像素级还原

## 技术依赖

- Python 3.8+（仅标准库）
- 微信公众号后台编辑器

## License

MIT。详见 [LICENSE](LICENSE)。品牌主题派生自 [voltagent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)（MIT）；详见 [ATTRIBUTION.md](ATTRIBUTION.md)。
