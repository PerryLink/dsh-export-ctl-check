#!/usr/bin/env python3
"""Generate README image assets for dsh-export-ctl-check (docs/assets/).

Outputs (idempotent overwrite):
  dsh-export-ctl-check-flow-light.svg / -dark.svg
      Hero workflow diagram. Two hand-written SVG files (vector — never
      rasterized to webp). Text inside is command-surface tokens only
      (export_ctl_check, rules/export-ctl-check.yaml, ...), so all five
      README languages share the same pair.
      There is no UI half and no benchmark data, so no screenshot and no
      evidence chart is generated — nothing is faked.

Run once:  python scripts/gen-readme-assets.py
Requires:  Pillow (bundled with the DSH runtime Python) for the CJK font probe.
"""
from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw, ImageFont  # noqa: F401 — font probe below

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")

# --- palette: PerryLink family (accent) + GitHub page backgrounds ----------
FAMILY = "#4B67B4"   # family accent (badges use labelColor #2B3245)
GREEN = {"light": "#16a34a", "dark": "#3fb950"}
SKIN = {
    "light": dict(bg="#ffffff", box="#f6f8fa", border="#d0d7de",
                  text="#1f2328", sub="#57606a"),
    "dark": dict(bg="#0d1117", box="#161b22", border="#30363d",
                 text="#f0f6fc", sub="#8b949e"),
}

# --- CJK font probe: never let a future localized label render as tofu ------
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyh.ttc",      # Microsoft YaHei
    r"C:\Windows\Fonts\simhei.ttf",    # SimHei
    r"C:\Windows\Fonts\Deng.ttf",      # DengXian
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/PingFang.ttc",
]
FONT_PATH = next((p for p in FONT_CANDIDATES if os.path.exists(p)), None)
if FONT_PATH is None:
    sys.exit("FATAL: no CJK font found (looked for msyh.ttc, simhei.ttf, "
             "Deng.ttf, Noto Sans CJK, PingFang). Refusing to render Chinese "
             "as tofu boxes; install one of the probed fonts and re-run.")

WEBP_QUALITY = 90  # used only if a future benchmark chart is added


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size)


# ---------------------------------------------------------------------------
# Hero workflow SVG (light + dark)
# ---------------------------------------------------------------------------
# (title, subtitle, title font-size) — command/config tokens only.
FLOW_NODES = [
    ("input", "JSON · YAML", 16),
    ("export_ctl_check", "file | material", 16),
    ("rules/export-ctl-check.yaml", "EC-001 … EC-008", 14),
    ("report", "findings + skipped", 16),
]


def flow_svg(skin: str) -> str:
    s = SKIN[skin]
    w, h = 1200, 400
    nw, nh, gap = 240, 100, 40
    y0 = 150
    xs = [60 + i * (nw + gap) for i in range(len(FLOW_NODES))]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" '
        f'aria-label="dsh-export-ctl-check workflow">',
        '<title>dsh-export-ctl-check workflow</title>',
        f'<rect width="{w}" height="{h}" rx="18" fill="{s["bg"]}"/>',
        f'<text x="60" y="62" fill="{s["text"]}" font-family="ui-sans-serif,'
        f'system-ui,sans-serif" font-size="30" font-weight="700">'
        f'dsh-export-ctl-check</text>',
        f'<text x="60" y="94" fill="{s["sub"]}" font-family="ui-monospace,'
        f'monospace" font-size="16">export_ctl_check · JSON / YAML in · '
        f'findings + skipped out</text>',
        f'<line x1="60" y1="116" x2="1140" y2="116" stroke="{s["border"]}"/>',
    ]
    for i, (label, sub, title_size) in enumerate(FLOW_NODES):
        x = xs[i]
        accent = GREEN[skin] if i == len(FLOW_NODES) - 1 else (
            FAMILY if i == 1 else s["border"])
        parts.append(
            f'<rect x="{x}" y="{y0}" width="{nw}" height="{nh}" rx="14" '
            f'fill="{s["box"]}" stroke="{accent}" stroke-width="2"/>')
        parts.append(
            f'<text x="{x + nw // 2}" y="{y0 + 42}" fill="{s["text"]}" '
            f'text-anchor="middle" font-family="ui-monospace,monospace" '
            f'font-size="{title_size}" font-weight="700">{label}</text>')
        parts.append(
            f'<text x="{x + nw // 2}" y="{y0 + 70}" fill="{s["sub"]}" '
            f'text-anchor="middle" font-family="ui-monospace,monospace" '
            f'font-size="13">{sub}</text>')
        if i < len(FLOW_NODES) - 1:
            ax = x + nw + 7
            ay = y0 + nh // 2
            parts.append(
                f'<path d="M{ax} {ay}h{gap - 14}" stroke="{s["sub"]}" '
                f'stroke-width="3"/>')
            parts.append(
                f'<path d="M{ax + gap - 16} {ay - 7}l10 7-10 7" fill="none" '
                f'stroke="{s["sub"]}" stroke-width="3" '
                f'stroke-linecap="round" stroke-linejoin="round"/>')
    # rule-pack bar under the tool and the rules node
    bx, bw, by, bh = 340, 560, 288, 56
    for cx in (xs[1] + nw // 2, xs[2] + nw // 2):
        parts.append(
            f'<path d="M{cx} {y0 + nh}v{by - y0 - nh}" '
            f'stroke="{FAMILY}" stroke-width="2" stroke-dasharray="5 5"/>')
    parts.append(
        f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="12" '
        f'fill="{s["box"]}" stroke="{FAMILY}" stroke-width="2"/>')
    parts.append(
        f'<text x="{bx + bw // 2}" y="{by + 35}" fill="{s["text"]}" '
        f'text-anchor="middle" font-family="ui-monospace,monospace" '
        f'font-size="14">8 rules · kind-capped severity · '
        f'skipped[] carries a reason</text>')
    parts.append(
        f'<text x="60" y="382" fill="{s["sub"]}" font-family="ui-monospace,'
        f'monospace" font-size="13">read-only · no network · no model call · '
        f'no writes · original material never modified</text>')
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for skin in ("light", "dark"):
        with open(os.path.join(OUT, f"dsh-export-ctl-check-flow-{skin}.svg"),
                  "w", encoding="utf-8", newline="\n") as fh:
            fh.write(flow_svg(skin))
    print("wrote 2 SVG hero assets to docs/assets/")


if __name__ == "__main__":
    main()
