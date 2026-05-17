# Attribution

This project derives 15 of its 16 themes from brand DESIGN.md files in
[voltagent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)
(MIT-licensed). Each upstream DESIGN.md is a third-party interpretation of a
public brand's design language — not an official artifact from the brand
owner. This project further degrades those tokens to a WeChat-safe inline-style
subset; substantial design fidelity is lost in that translation, and the
WeChat-rendered output should be understood as **brand-inspired**, not
brand-faithful.

Brand names, logos, and visual identities are property of their respective
owners. Use of brand-mapped color tokens here is referential and does not
imply affiliation with, sponsorship by, or endorsement from the brand owners.
If a brand owner objects to inclusion, open an issue and we will remove the
theme.

## Upstream theme sources

| Theme | Upstream DESIGN.md | Brand owner (reference) |
|---|---|---|
| `claude` | [voltagent claude](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/claude) | Anthropic |
| `stripe` | [voltagent stripe](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/stripe) | Stripe |
| `vercel` | [voltagent vercel](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/vercel) | Vercel |
| `apple` | [voltagent apple](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/apple) | Apple |
| `linear` | [voltagent linear.app](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/linear.app) | Linear |
| `notion` | [voltagent notion](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/notion) | Notion Labs |
| `figma` | [voltagent figma](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/figma) | Figma |
| `airbnb` | [voltagent airbnb](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/airbnb) | Airbnb |
| `slack` | [voltagent slack](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/slack) | Slack Technologies / Salesforce |
| `mintlify` | [voltagent mintlify](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/mintlify) | Mintlify |
| `resend` | [voltagent resend](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/resend) | Resend |
| `supabase` | [voltagent supabase](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/supabase) | Supabase |
| `cal` | [voltagent cal](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/cal) | Cal.com |
| `posthog` | [voltagent posthog](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/posthog) | PostHog |
| `framer` | [voltagent framer](https://github.com/VoltAgent/awesome-design-md/tree/main/design-md/framer) | Framer |

`minimal` is in-house (no brand attribution).

### Theme not derived from voltagent/awesome-design-md

| Theme | Source DESIGN.md | Trademark holder (referential) |
|---|---|---|
| `economist` | [`docs/economist-design.md`](docs/economist-design.md) — original DESIGN.md interpretation included in this repo | The Economist Newspaper Limited |

The `economist` theme's source DESIGN.md was authored independently as
part of this repository, not derived from voltagent/awesome-design-md.
It is an original interpretation of the editorial design language
commonly associated with The Economist magazine. **It is not affiliated
with, endorsed by, or derived from any official Economist publication
or asset.** "The Economist" is a trademark of The Economist Newspaper
Limited; use of the name here is descriptive (to identify the visual
style being referenced), not commercial or associative. See the
preamble in [`docs/economist-design.md`](docs/economist-design.md) for
the full disclaimer.

## What is preserved from each upstream

For each brand, this project extracts a small set of color tokens
(primary/accent, body-ink, muted, hairline, canvas) and maps them onto a
flat WeChat-safe theme schema. Typography is reduced to a single
WeChat-renderable font fallback chain — proprietary brand fonts (Geist,
Copernicus, Sohne, SF Pro, Cal Sans, etc.) are not bundled and would not
load in the WeChat editor regardless.

## What is dropped

Gradients, dark hero surfaces, custom proprietary fonts, animations,
multi-tier typography hierarchies, illustrations, mesh backgrounds, atmospheric
color washes, brand-specific component shapes (cards, pills, dashboard
chrome), and any effect that requires CSS beyond WeChat's inline-style
whitelist.

For three brands whose canonical surface is dark (Linear, Resend, Framer),
this project ships a **light interpretation** that preserves the signature
accent on a light canvas. This is a deliberate departure from the upstream
specification, made because long-form WeChat articles on dark backgrounds
are uncomfortable to read on most readers' devices.

## License chain

- This project: MIT
- voltagent/awesome-design-md upstream: MIT
- Brand identities themselves: property of their respective owners; not
  redistributed by this project. Only color hex codes and font-fallback
  chains (which are not copyrightable) are derived.

## Upstream MIT License (voltagent/awesome-design-md)

The following is the verbatim license text from
<https://github.com/VoltAgent/awesome-design-md/blob/main/LICENSE>, preserved
here per OSS-derivative best practice:

```
MIT License

Copyright (c) 2026 VoltAgent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
