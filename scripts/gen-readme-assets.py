#!/usr/bin/env python3
"""README visuals for dsh-export-ctl-check — read off what this package ships.

Outputs (docs/assets/, idempotent overwrite):

  dsh-export-ctl-check-hero-{zh,en}-{light,dark}.webp   1440x576
  dsh-export-ctl-check-flow-v5-{light,dark}.svg         1100x660

Both figures are derived from this package's own artifacts, never from a
generic checker template:

  * `src/model.ts` — the register contract: 4 optional header scalars
    (exporter / contractNo / checkedAt / listVersion), 13 canonical columns
    (itemNo, itemName, hsCode, controlCode, controlList, category, endUse,
    endUser, destination, licenseNo, licenseAt, controlled, note), each with
    Chinese and English aliases; `rows[]` (also items / controls / 管制项) is
    the table that is actually read, and `REQUIRE_ANY_OF` refuses material
    where not one known column name is recognised.
  * `rules/export-ctl-check.yaml` — pack `2026.1`, 8 rules. Six check kinds
    appear: presence (EC-001, EC-005), conditionalPresence (EC-002, EC-003),
    presenceAny (EC-004), unique (EC-006), enum (EC-007), containsAny
    (EC-008). Four rules are `direct` (EC-002, EC-004, EC-005, EC-008) and
    four are `derived-from-principle` (EC-001, EC-003, EC-006, EC-007); the
    loader caps a derived rule at `warn`, which is why nothing in the pack is
    an `error`.
  * EC-001 -> EC-002 -> EC-003 is this pack's only conditional chain: the
    controlled column decides whether licenseNo is asked for, licenseNo
    decides whether licenseAt is asked for. The other five rules are
    independent of that chain. That chain is the spine of both figures.
  * `samples/quickstart/input/EC-001-unsafe.json` + its real run — one item
    (某型高性能传感器, licenseNo EX2026-0018, licenseAt 2026-02-25, controlled
    empty) producing `error 0 / warn 1 / info 0`, `issueCount 1`,
    `skippedCount 2`: EC-001 hits row 1's controlled cell; EC-002 is skipped
    because no row satisfies the controlled condition; EC-007 is skipped
    because `values` ships empty. The other five rules ran and found nothing.
  * `src/view.ts` + `src/index.ts` — the two output channels and the view:
    issues[] (found / expected / fix / locator) and skipped[] (rule + reason),
    rendered as markdown plus reportJson under the wording guard.

Hero: left column is the copy block (kicker / two-line wordmark / two value
lines / subtitle / meta / footer). The right side is this plugin's own
artifact for one item: an eight-cell scoreboard — one cell per rule, carrying
the canonical field, the observed cell and the state it reached in the real
quickstart run — followed by the single finding those cells produce and the
two skips. It is deliberately *not* a register row laid out as columns.

Flow: grammar = GATED LADDER WITH TWO EXITS, not a row of nodes. The
material and the rule pack are two inputs on the left; eight gates are stacked
in one ladder (the first three are the conditional chain, the rest are
independent), each gate leaving through exactly one of two exits; the two
exits converge on one report band on the right. Nothing is drawn as a
horizontal five-box pipeline.

Every label is measured before it is drawn; a label that would overflow aborts
the run instead of shipping clipped text. Node text inside the 1100px SVG is
13-13.5px (figure title 30px) and every annotation is >= 11px.

Old single-skin assets (…-flow.svg, …-hero.png, …-demo.*, quickstart.*) are
left on disk so existing external links keep resolving; the READMEs reference
only the new hero and flow-v5 pair.

Run once:  python scripts/gen-readme-assets.py
Requires:  Pillow + Windows fonts msyh.ttc / msyhbd.ttc / consola.ttf.
"""
from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from html import escape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")
NAME = "dsh-export-ctl-check"

FONT_FILES = {
    "cjk": r"C:\Windows\Fonts\msyh.ttc",
    "cjk_bold": r"C:\Windows\Fonts\msyhbd.ttc",
    "mono": r"C:\Windows\Fonts\consola.ttf",
    "mono_bold": r"C:\Windows\Fonts\consolab.ttf",
}
for _kind, _path in FONT_FILES.items():
    if not os.path.exists(_path):
        raise SystemExit(f"FATAL: font missing: {_path}")

RADIUS = 20
os.makedirs(OUT, exist_ok=True)

FONT_CSS_SANS = ("'Microsoft YaHei','Segoe UI','PingFang SC',"
                 "'Noto Sans CJK SC',sans-serif")
FONT_CSS_MONO = "Consolas,'Microsoft YaHei',ui-monospace,monospace"

SKIN = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", edge="#e6e2ef",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", ok="#15803d", warn="#b45309",
        pill="#ece7f9", band="#f5f2fb", grid="#e7e4f0",
        ok_bg="#e8f5ec", warn_bg="#fbf1e4", skip_bg="#eeeaf5",
        shadow=(43, 35, 80), shadow_alpha=52, glow=32,
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#1b2231", edge="#2e374b",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", ok="#3fb950", warn="#d9a441",
        pill="#242d42", band="#202839", grid="#2b3348",
        ok_bg="#1b2b22", warn_bg="#2f2718", skip_bg="#242b3a",
        shadow=(0, 0, 0), shadow_alpha=150, glow=44,
    ),
}

FLOW = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        panel="#ffffff", card="#ffffff", edge="#e6e2ef",
        band="#f5f2fb", pill="#ece7f9", tint="#f7f4ec",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", ok="#15803d", warn="#b45309",
        ok_bg="#e8f5ec", warn_bg="#fbf1e4", skip_bg="#eeeaf5",
        rule="#e7e4f0", shadow="#2b2440", shadow_op="0.14",
        dot="#cfc8e2", dot_op="0.5",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        panel="#1b2231", card="#1b2231", edge="#2e374b",
        band="#202839", pill="#242d42", tint="#2a2419",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", ok="#3fb950", warn="#d9a441",
        ok_bg="#1b2b22", warn_bg="#2f2718", skip_bg="#242b3a",
        rule="#2b3348", shadow="#000000", shadow_op="0.52",
        dot="#2a3346", dot_op="0.5",
    ),
}

# ---------------------------------------------------------------------------
# fonts + measuring
# ---------------------------------------------------------------------------
_font_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}
_MEASURE = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def font(size: float, kind: str = "cjk") -> ImageFont.FreeTypeFont:
    key = (kind, int(round(size)))
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONT_FILES[kind], key[1])
    return _font_cache[key]


def measure(text: str, size: float, kind: str = "cjk") -> float:
    return _MEASURE.textlength(text, font=font(size, kind))


def require_w(text: str, size: float, kind: str, max_w: float,
              what: str) -> None:
    got = measure(text, size, kind)
    if got > max_w + 0.4:
        raise SystemExit(f"FATAL: {what} overflows: {text!r} needs "
                         f"{got:.1f}px > {max_w:.0f}px")


def fit(text: str, kind: str, max_w: float, start: float,
        minimum: float) -> float:
    size = float(start)
    while size > minimum:
        if measure(text, size, kind) <= max_w:
            return size
        size -= 1
    raise SystemExit(f"FATAL: text does not fit {max_w:.0f}px at >= "
                     f"{minimum}px: {text!r}")


def fit_lines(lines: tuple[str, ...] | list[str], kind: str, max_w: float,
              start: float, minimum: float) -> float:
    return min(fit(line, kind, max_w, start, minimum) for line in lines)


def hx(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------------------
# raster primitives
# ---------------------------------------------------------------------------
def gradient(w: int, h: int, top: str, bottom: str) -> Image.Image:
    base = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(base)
    a, b = hx(top), hx(bottom)
    for y in range(h):
        t = 0.14 * (y / h) + 0.86 * (y / h) ** 1.35
        draw.line([(0, y), (w, y)],
                  fill=tuple(int(p + (q - p) * t) for p, q in zip(a, b)))
    return base


def glow(img: Image.Image, cx: int, cy: int, r: int, color: str,
         alpha: int) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rgb = hx(color)
    for i in range(10, 0, -1):
        rr = r * i / 10
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  fill=rgb + (int(alpha * (1 - i / 11)),))
    return Image.alpha_composite(img.convert("RGBA"),
                                 layer.filter(ImageFilter.GaussianBlur(26))
                                 ).convert("RGB")


def card(img: Image.Image, box: tuple[int, int, int, int], s: dict,
         radius: int = RADIUS, shadow: int = 22,
         fill: str | None = None, edge: str | None = None) -> Image.Image:
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([x0 + 2, y0 + max(4, shadow // 2), x1 + 2,
                         y1 + max(5, shadow // 2)],
                        radius=radius, fill=s["shadow"] + (s["shadow_alpha"],))
    base = Image.alpha_composite(img.convert("RGBA"),
                                 layer.filter(ImageFilter.GaussianBlur(shadow / 2)))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, radius=radius, fill=hx(fill or s["card"]),
                        outline=hx(edge or s["edge"]), width=2)
    return base.convert("RGB")


def pill(img: Image.Image, xy: tuple[float, float], text: str, s: dict,
         size: float = 16, fg: str | None = None, bg: str | None = None,
         kind: str = "cjk_bold") -> float:
    d = ImageDraw.Draw(img)
    f = font(size, kind)
    w = d.textlength(text, font=f)
    x, y = xy
    h = size + 22
    d.rounded_rectangle([x, y, x + w + 36, y + h], radius=h / 2,
                        fill=hx(bg or s["pill"]))
    d.text((x + 18, y + h / 2), text, font=f, fill=hx(fg or s["accent"]),
           anchor="lm")
    return x + w + 36


def chip_right(img: Image.Image, right: float, y: float, text: str, fg: str,
               bg: str, size: float = 12, height: float = 25,
               kind: str = "mono_bold", pad: float = 10) -> float:
    d = ImageDraw.Draw(img)
    w = d.textlength(text, font=font(size, kind)) + pad * 2
    x = right - w
    d.rounded_rectangle([x, y, right, y + height], radius=height / 2,
                        fill=hx(bg))
    d.text((x + pad, y + height / 2 + 0.5), text, font=font(size, kind),
           fill=hx(fg), anchor="lm")
    return x


def rich_line(img: Image.Image, x: float, y: float,
              runs: list[tuple[str, str, str]], size: float) -> float:
    """Draw runs of (text, colour, kind) left to right; return the end x."""
    d = ImageDraw.Draw(img)
    cursor = float(x)
    for text, color, kind in runs:
        d.text((cursor, y), text, font=font(size, kind), fill=hx(color),
               anchor="ls")
        cursor += measure(text, size, kind)
    return cursor


# ---------------------------------------------------------------------------
# hero copy + the eight-cell scoreboard for one item
# ---------------------------------------------------------------------------
HERO = {
    "zh": dict(
        kicker="DeepSeek Harness 插件 · 出口管制物项核对",
        title=("dsh-export-", "ctl-check"),
        value=("逐条核到「哪一行、哪一栏」，", "差什么、补什么——结论留给你。"),
        sub="8 条规则核台账闭环；不持有管制清单。",
        meta=[("export_ctl_check", "mono"),
              (" · 8 条规则 · ", "cjk"),
              ("EC-001..EC-008", "mono")],
        foot="Apache-2.0 · 只读 · 不联网 · 不调用模型 · 不写材料文件",
        card_title=("rows[0]", "  第 1 行"),
        card_sub="某型高性能传感器 · 许可证号 EX2026-0018 · 8 条规则的执行结果",
        chip_warn="warn 1",
        chip_skip="skipped 2",
        states={"hit": "命中", "pass": "通过", "skip": "跳过"},
        tiles=[
            ("EC-001", "controlled", "（空）", "hit", "cjk"),
            ("EC-002", "licenseNo", "EX2026-0018", "skip", "mono"),
            ("EC-003", "licenseAt", "2026-02-25", "pass", "mono"),
            ("EC-004", "endUse|endUser", "已填", "pass", "cjk"),
            ("EC-005", "destination", "已填", "pass", "cjk"),
            ("EC-006", "licenseNo", "无重复", "pass", "cjk"),
            ("EC-007", "category", "军民两用", "skip", "cjk"),
            ("EC-008", "itemName", "无占位符", "pass", "cjk"),
        ],
        find_head=("EC-001", "warn", "第 1 行 · controlled"),
        find_rows=[("found", "第 1 行「controlled」为空", 16),
                   ("expected", "「controlled」应填写", 15),
                   ("fix", "补填是否受控；本条只核对是否声明，不判断该判断是否正确", 14)],
        skips=[("EC-002", "跳过：没有满足「controlled」条件的行"),
               ("EC-007", "跳过：规则库未配置 values（category）")],
        source="samples/quickstart/input/EC-001-unsafe.json · 1 warn · 2 skipped",
    ),
    "en": dict(
        kicker="DeepSeek Harness plugin · export-control check",
        title=("dsh-export-", "ctl-check"),
        value=("Row by row, cell by cell:", "what is missing, and where."),
        sub="Register closure only; no control list held.",
        meta=[("export_ctl_check", "mono"),
              (" · 8 rules · ", "cjk"),
              ("EC-001..EC-008", "mono")],
        foot="Apache-2.0 · read-only · no network · no model call · no writes",
        card_title=("rows[0]", "  item 1"),
        card_sub="one item, eight rules — what each rule made of it",
        chip_warn="warn 1",
        chip_skip="skipped 2",
        states={"hit": "hit", "pass": "pass", "skip": "skipped"},
        tiles=[
            ("EC-001", "controlled", "(empty)", "hit", "mono"),
            ("EC-002", "licenseNo", "EX2026-0018", "skip", "mono"),
            ("EC-003", "licenseAt", "2026-02-25", "pass", "mono"),
            ("EC-004", "endUse|endUser", "filled", "pass", "mono"),
            ("EC-005", "destination", "filled", "pass", "mono"),
            ("EC-006", "licenseNo unique", "no duplicate", "pass", "mono"),
            ("EC-007", "category", "civil-military", "skip", "mono"),
            ("EC-008", "itemName", "no placeholder", "pass", "mono"),
        ],
        find_head=("EC-001", "warn", "row 1 · controlled"),
        find_rows=[("found", "controlled is empty on row 1", 16),
                   ("expected", "controlled should be filled", 15),
                   ("fix", "fill it in; the rule only checks that it is stated", 14)],
        skips=[("EC-002", "skipped: no row satisfies the controlled condition"),
               ("EC-007", "skipped: category values are not configured")],
        source="samples/quickstart/input/EC-001-unsafe.json · 1 warn · 2 skipped",
    ),
}


def hero(lang: str, skin: str) -> None:
    s = SKIN[skin]
    h = HERO[lang]
    W, H = 1440, 576
    img = gradient(W, H, s["bg_from"], s["bg_to"])
    img = glow(img, 1160, 30, 430, s["accent"], s["glow"])
    img = glow(img, 150, 570, 300, s["accent"], max(8, s["glow"] // 3))

    m, col_w = 56, 552
    d = ImageDraw.Draw(img)

    # ---- left copy column ---------------------------------------------------
    kicker_w = measure(h["kicker"], 19, "cjk_bold") + 36
    if kicker_w > 600:
        raise SystemExit(f"FATAL: kicker pill {kicker_w:.0f}px wide")
    pill(img, (m, 42), h["kicker"], s, size=19)
    d = ImageDraw.Draw(img)

    title_size = fit_lines(list(h["title"]), "mono_bold", col_w, 84, 72)
    for line in h["title"]:
        require_w(line, title_size, "mono_bold", col_w, "hero title")
    d.text((m - 1, 184), h["title"][0], font=font(title_size, "mono_bold"),
           fill=hx(s["text"]), anchor="ls")
    d.text((m - 1, 268), h["title"][1], font=font(title_size, "mono_bold"),
           fill=hx(s["accent"]), anchor="ls")

    value_size = fit_lines(list(h["value"]), "cjk_bold", col_w,
                           34 if lang == "zh" else 30, 26)
    for index, line in enumerate(h["value"]):
        require_w(line, value_size, "cjk_bold", col_w, "hero value line")
        d.text((m, 326 + index * 42), line, font=font(value_size, "cjk_bold"),
               fill=hx(s["text"]), anchor="ls")

    sub_size = fit(h["sub"], "cjk", col_w, 25, 21)
    require_w(h["sub"], sub_size, "cjk", col_w, "hero subtitle")
    d.text((m, 412), h["sub"], font=font(sub_size, "cjk"),
           fill=hx(s["sub"]), anchor="ls")

    meta_runs = [(text, s["faint"], kind) for text, kind in h["meta"]]
    meta_end = m + sum(measure(text, 20, kind) for text, kind in h["meta"])
    if meta_end > m + col_w:
        raise SystemExit("FATAL: hero meta overflows")
    rich_line(img, m + 1, 452, meta_runs, 20)

    d = ImageDraw.Draw(img)
    d.line([m + 1, 480, m + col_w - 4, 480], fill=hx(s["grid"]), width=2)
    foot_size = fit(h["foot"], "cjk", col_w, 16, 13)
    d.text((m + 1, 510), h["foot"], font=font(foot_size, "cjk"),
           fill=hx(s["faint"]), anchor="ls")

    # ---- right: eight cells, one per rule -----------------------------------
    img = card(img, (648, 40, 1392, 540), s, radius=20, shadow=26)
    d = ImageDraw.Draw(img)

    d.rounded_rectangle([648, 40, 1392, 122], radius=20, fill=hx(s["band"]))
    d.rectangle([648, 98, 1392, 122], fill=hx(s["band"]))
    d.line([648, 122, 1392, 122], fill=hx(s["edge"]), width=1)

    d.text((676, 86), h["card_title"][0], font=font(25, "mono_bold"),
           fill=hx(s["text"]), anchor="ls")
    tw = measure(h["card_title"][0], 25, "mono_bold")
    d.text((682 + tw, 87), h["card_title"][1], font=font(21, "cjk_bold"),
           fill=hx(s["accent"]), anchor="ls")
    require_w(h["card_sub"], 15, "cjk", 620, "card subtitle")
    d.text((676, 111), h["card_sub"], font=font(15, "cjk"),
           fill=hx(s["faint"]), anchor="ls")

    x = chip_right(img, 1364, 56, h["chip_skip"], s["accent"], s["pill"],
                   size=12.5, height=26)
    chip_right(img, x - 8, 56, h["chip_warn"], s["warn"], s["warn_bg"],
               size=12.5, height=26)

    state_style = {
        "hit": (s["warn"], s["warn_bg"]),
        "pass": (s["ok"], s["ok_bg"]),
        "skip": (s["sub"], s["skip_bg"]),
    }
    tw_, gap = 167, 12
    for index, (rule, field, observed, state, kind) in enumerate(h["tiles"]):
        col, row = index % 4, index // 4
        tx = 668 + col * (tw_ + gap)
        ty = 136 + row * 98

        d = ImageDraw.Draw(img)
        d.rounded_rectangle([tx, ty, tx + tw_, ty + 86], radius=14,
                            fill=hx(s["card"]), outline=hx(s["edge"]),
                            width=1)
        if state == "hit":
            d.rounded_rectangle([tx, ty, tx + tw_, ty + 86], radius=14,
                                fill=hx(s["warn_bg"]), outline=hx(s["warn"]),
                                width=2)
        d.text((tx + 14, ty + 27), rule, font=font(16, "mono_bold"),
               fill=hx(s["text"]), anchor="ls")
        fg, bg = state_style[state]
        chip_right(img, tx + tw_ - 10, ty + 12, h["states"][state], fg, bg,
                   size=12, height=22, kind="cjk_bold", pad=9)
        d = ImageDraw.Draw(img)
        require_w(field, 13.5, "mono", tw_ - 26, f"tile field {rule}")
        d.text((tx + 14, ty + 51), field, font=font(13.5, "mono"),
               fill=hx(s["sub"]), anchor="ls")
        obs_kind = kind
        require_w(observed, 14, obs_kind, tw_ - 26, f"tile value {rule}")
        d.text((tx + 14, ty + 74), observed,
               font=font(14, obs_kind),
               fill=hx(s["text"] if state != "skip" else s["sub"]),
               anchor="ls")

    d = ImageDraw.Draw(img)
    d.line([676, 338, 1364, 338], fill=hx(s["grid"]), width=1)

    # ---- the one finding the blank cell produces ----------------------------
    d.ellipse([678, 350, 690, 362], fill=hx(s["warn"]))
    d.text((702, 360), h["find_head"][0], font=font(17, "mono_bold"),
           fill=hx(s["text"]), anchor="ls")
    cw = measure(h["find_head"][0], 17, "mono_bold")
    sev_w = measure(h["find_head"][1], 11.5, "mono_bold") + 18
    d.rounded_rectangle([702 + cw + 10, 344, 702 + cw + 10 + sev_w, 364],
                        radius=10, fill=hx(s["warn_bg"]))
    d.text((702 + cw + 19, 354), h["find_head"][1],
           font=font(11.5, "mono_bold"), fill=hx(s["warn"]), anchor="ls")
    d.text((702 + cw + 18 + sev_w, 360), h["find_head"][2],
           font=font(14, "cjk"), fill=hx(s["sub"]), anchor="ls")

    for index, (tag, text, size) in enumerate(h["find_rows"]):
        y = 392 + index * 23
        d.text((676, y), tag, font=font(11, "mono"),
               fill=hx(s["sub"]), anchor="ls")
        require_w(text, size, "cjk", 600, f"finding {tag}")
        d.text((752, y), text, font=font(size, "cjk"),
               fill=hx(s["text"] if index < 2 else s["sub"]), anchor="ls")

    for index, (rule, text) in enumerate(h["skips"]):
        y = 470 + index * 20
        d.text((676, y), rule, font=font(11, "mono_bold"),
               fill=hx(s["faint"]), anchor="ls")
        require_w(text, 11.5, "cjk", 610, f"skip {rule}")
        d.text((740, y), text, font=font(11.5, "cjk"),
               fill=hx(s["sub"]), anchor="ls")

    require_w(h["source"], 11, "mono", 620, "source line")
    d.text((676, 524), h["source"], font=font(11, "mono"),
           fill=hx(s["faint"]), anchor="ls")
    d.rounded_rectangle([648, 40, 1392, 540], radius=20,
                        outline=hx(s["edge"]), width=2)

    name = f"{NAME}-hero-{lang}-{skin}.webp"
    img.save(os.path.join(OUT, name), "WEBP", quality=92, method=6)
    print(f"wrote {name} ({W}x{H})")


# ---------------------------------------------------------------------------
# flow: two inputs -> one ladder of eight gates -> two exits -> one report
# ---------------------------------------------------------------------------
# (rule id, check kind, field line, state in the quickstart run)
GATES = [
    ("EC-001", "presence", "controlled", "hit"),
    ("EC-002", "conditionalPresence", "controlled → licenseNo", "skip"),
    ("EC-003", "conditionalPresence", "licenseNo → licenseAt", "pass"),
    ("EC-004", "presenceAny", "endUse | endUser", "pass"),
    ("EC-005", "presence", "destination", "pass"),
    ("EC-006", "unique", "licenseNo（同表唯一）", "pass"),
    ("EC-007", "enum", "category（本机构取值）", "skip"),
    ("EC-008", "containsAny", "itemName（占位符词表）", "pass"),
]


class Svg:
    """Tiny SVG writer that measures every label before it is emitted."""

    def __init__(self, s: dict) -> None:
        self.s = s
        self.parts: list[str] = []
        self.bad: list[str] = []

    def add(self, markup: str) -> None:
        self.parts.append(markup)

    def _w(self, content: str, size: float, kind: str,
           tracking: float | None = None) -> float:
        got = measure(content, size, kind)
        if tracking:
            got += tracking * max(len(content) - 1, 0)
        return got

    def text(self, x: float, y: float, content: str, size: float, fill: str, *,
             anchor: str = "start", weight: int | None = None,
             mono: bool = False, max_w: float | None = None,
             opacity: float | None = None) -> None:
        kind = "mono" if mono else "cjk"
        if weight:
            kind += "_bold"
        if max_w is not None and self._w(content, size, kind) > max_w + 0.4:
            self.bad.append(f"{content!r} needs "
                            f"{self._w(content, size, kind):.1f}px > {max_w:.0f}px")
        attrs = [f'x="{x}"', f'y="{y}"', f'fill="{fill}"',
                 f'font-family="{FONT_CSS_MONO if mono else FONT_CSS_SANS}"',
                 f'font-size="{size}"']
        if anchor != "start":
            attrs.append(f'text-anchor="{anchor}"')
        if weight:
            attrs.append(f'font-weight="{weight}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        self.add(f'<text {" ".join(attrs)}>{escape(content)}</text>')

    def rich(self, x: float, y: float, runs: list[tuple[str, str, str]],
             size: float, *, anchor: str = "start",
             max_w: float | None = None) -> float:
        """Draw runs of (text, fill, kind[mono|cjk + optional bold])."""
        widths = [self._w(text, size, kind) for text, _, kind in runs]
        total = sum(widths)
        if max_w is not None and total > max_w + 0.4:
            self.bad.append(f"{''.join(r[0] for r in runs)!r} needs "
                            f"{total:.1f}px > {max_w:.0f}px")
        cursor = x - total if anchor == "end" else x
        for (text, fill, kind), width in zip(runs, widths):
            mono = kind.startswith("mono")
            attrs = [f'x="{cursor}"', f'y="{y}"', f'fill="{fill}"',
                     f'font-family="{FONT_CSS_MONO if mono else FONT_CSS_SANS}"',
                     f'font-size="{size}"']
            if kind.endswith("_bold"):
                attrs.append('font-weight="700"')
            self.add(f'<text {" ".join(attrs)}>{escape(text)}</text>')
            cursor += width
        return cursor

    def rect(self, x: float, y: float, w: float, h: float, *, fill: str,
             rx: float = 0, stroke: str | None = None, sw: float = 1.5,
             shadow: bool = False, dash: str | None = None,
             opacity: float | None = None) -> None:
        attrs = [f'x="{x}"', f'y="{y}"', f'width="{w}"', f'height="{h}"']
        if rx:
            attrs.append(f'rx="{rx}"')
        attrs.append(f'fill="{fill}"')
        if stroke:
            attrs += [f'stroke="{stroke}"', f'stroke-width="{sw}"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        if shadow:
            attrs.append('filter="url(#soft)"')
        self.add(f'<rect {" ".join(attrs)}/>')

    def line(self, x1: float, y1: float, x2: float, y2: float, *, stroke: str,
             sw: float = 1.5, dash: str | None = None,
             opacity: float | None = None) -> None:
        attrs = [f'x1="{x1}"', f'y1="{y1}"', f'x2="{x2}"', f'y2="{y2}"',
                 f'stroke="{stroke}"', f'stroke-width="{sw}"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        self.add(f'<line {" ".join(attrs)}/>')

    def path(self, d: str, *, stroke: str, sw: float = 1.5,
             fill: str = "none", dash: str | None = None,
             opacity: float | None = None) -> None:
        attrs = [f'd="{d}"', f'fill="{fill}"', f'stroke="{stroke}"',
                 f'stroke-width="{sw}"', 'stroke-linejoin="round"',
                 'stroke-linecap="round"']
        if dash:
            attrs.append(f'stroke-dasharray="{dash}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        self.add(f'<path {" ".join(attrs)}/>')

    def circle(self, cx: float, cy: float, r: float, *, fill: str,
               stroke: str | None = None, sw: float = 1.5) -> None:
        attrs = [f'cx="{cx}"', f'cy="{cy}"', f'r="{r}"', f'fill="{fill}"']
        if stroke:
            attrs += [f'stroke="{stroke}"', f'stroke-width="{sw}"']
        self.add(f'<circle {" ".join(attrs)}/>')

    def chip_right(self, right: float, y: float, label: str, fg: str, bg: str,
                   *, size: float = 11, pad: float = 9, height: float = 22,
                   mono: bool = False, weight: int | None = None) -> float:
        kind = "mono" if mono else "cjk"
        if weight:
            kind += "_bold"
        w = self._w(label, size, kind) + pad * 2
        x = right - w
        self.rect(x, y, w, height, fill=bg, rx=height / 2)
        self.text(x + pad, y + height / 2 + size * 0.35, label, size, fg,
                  mono=mono, weight=weight)
        return x

    def arrow_right(self, x1: float, x2: float, y: float, color: str,
                    sw: float = 1.6) -> None:
        self.path(f"M{x1} {y}H{x2 - 8}", stroke=color, sw=sw)
        self.add(f'<path d="M{x2} {y}l-9 -4.6v9.2z" fill="{color}"/>')

    def svg(self, w: int, h: int, title: str, desc: str) -> str:
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" '
                f'height="{h}" viewBox="0 0 {w} {h}" role="img" '
                f'aria-labelledby="title desc">')
        return "\n".join([head, f'<title id="title">{escape(title)}</title>',
                          f'<desc id="desc">{escape(desc)}</desc>',
                          *self.parts, "</svg>"]) + "\n"


def flow_svg(skin: str) -> str:
    f = FLOW[skin]
    W, H = 1100, 660
    v = Svg(f)

    v.add("<defs>")
    v.add(f'<linearGradient id="bg" x1="0" y1="0" x2="0.2" y2="1">'
          f'<stop offset="0" stop-color="{f["bg_from"]}"/>'
          f'<stop offset="1" stop-color="{f["bg_to"]}"/></linearGradient>')
    v.add(f'<filter id="soft" x="-30%" y="-30%" width="160%" height="180%">'
          f'<feDropShadow dx="0" dy="7" stdDeviation="9" '
          f'flood-color="{f["shadow"]}" flood-opacity="{f["shadow_op"]}"/>'
          f'</filter>')
    v.add(f'<pattern id="dots" width="24" height="24" '
          f'patternUnits="userSpaceOnUse">'
          f'<circle cx="1.2" cy="1.2" r="1.2" fill="{f["dot"]}"/></pattern>')
    v.add("</defs>")

    v.rect(0, 0, W, H, fill="url(#bg)")
    v.rect(0, 0, W, H, fill="url(#dots)", opacity=f["dot_op"])

    # ---- header -------------------------------------------------------------
    v.text(44, 56, NAME, 30, f["text"], weight=700, mono=True, max_w=620)
    v.text(44, 86, "条件链 controlled → licenseNo → licenseAt + 五条独立规则；"
                   "命中的进 issues[]，跑不了的进 skipped[]。", 15, f["sub"],
           max_w=790)
    v.chip_right(1056, 30, "rules/export-ctl-check.yaml · v2026.1 · 8 条",
                 f["accent"], f["pill"], size=11.5, pad=12, height=28,
                 mono=True)
    v.text(44, 112, "IN  ·  file | material  ·  JSON / YAML  ·  表头 4 栏 + "
                    "rows[]  ·  只读", 11, f["faint"], max_w=560)
    v.text(1056, 112, "OUT  ·  summary · issues[] · skipped[] · markdown · "
                      "reportJson", 11, f["faint"], mono=True, anchor="end",
           max_w=460)
    v.line(44, 126, 1056, 126, stroke=f["rule"], sw=1, opacity=0.75)

    # ---- input 1: the register ---------------------------------------------
    v.rect(44, 140, 256, 166, fill=f["panel"], rx=18, stroke=f["edge"],
           sw=1.5, shadow=True)
    v.text(64, 170, "IN · 台账", 13, f["text"], weight=700, max_w=90)
    v.chip_right(282, 156, "JSON / YAML", f["accent"], f["pill"], size=11,
                 height=21, mono=True)
    v.text(64, 198, "表头 4 栏（可选）：exporter、", 11, f["sub"], max_w=236)
    v.text(64, 216, "contractNo、listVersion、checkedAt", 11, f["sub"],
           max_w=236)
    v.text(64, 240, "rows[] · 每行一条物项", 11, f["sub"], mono=True,
           max_w=236)
    v.text(64, 262, "13 个规范栏目 · 别名归一", 11, f["sub"], max_w=236)
    v.text(64, 284, "requireAnyOf：至少一个已知栏名", 11, f["faint"],
           max_w=236)

    # ---- input 2: the rule pack --------------------------------------------
    v.rect(44, 318, 256, 160, fill=f["card"], rx=18, stroke=f["edge"],
           sw=1.5, shadow=True)
    v.text(64, 348, "RULES · 规则库", 13, f["text"], weight=700, max_w=150)
    v.chip_right(282, 334, "v2026.1 · 8 条", f["accent"], f["pill"], size=11,
                 height=21, mono=True)
    v.text(64, 376, "8 条规则 · 6 种 check kind", 11, f["sub"], max_w=236)
    v.text(64, 398, "EC-001 … EC-008", 11, f["sub"], mono=True, max_w=236)
    v.text(64, 420, "加载期校验引用六字段", 11, f["sub"], max_w=236)
    v.text(64, 442, "document / number / clause /", 11, f["faint"], mono=True,
           max_w=236)
    v.text(64, 460, "excerpt / kind / source", 11, f["faint"], mono=True,
           max_w=236)

    # ---- input 3: the boundary this pack will not cross --------------------
    v.rect(44, 490, 256, 76, fill=f["card"], rx=18, stroke=f["edge"],
           sw=1.5, shadow=True)
    v.rect(47, 502, 4, 52, fill=f["warn"], rx=2, opacity=0.75)
    v.text(66, 516, "BOUNDARY · 不持有管制清单", 12, f["text"], weight=700,
           max_w=228)
    v.text(66, 538, "发现不了「该申报受控却没申报」", 11, f["sub"],
           max_w=228)
    v.text(66, 556, "不判受控、不判许可、不下结论", 11, f["faint"],
           max_w=228)

    # ---- the two inputs merge ----------------------------------------------
    v.path("M300 223H314V399H300", stroke=f["accent"], sw=1.6, opacity=0.85)
    v.arrow_right(314, 330, 311, f["accent"], sw=1.6)

    # ---- the ladder: eight gates, one exit each ----------------------------
    v.rect(330, 140, 370, 426, fill=f["panel"], rx=18, stroke=f["edge"],
           sw=1.5, shadow=True)
    v.text(352, 170, "CHECK · 每行 × 8 条规则", 13, f["text"], weight=700,
           max_w=210)
    v.chip_right(682, 156, "EC-001 … EC-008", f["accent"], f["pill"], size=11,
                 height=21, mono=True)
    v.text(352, 186, "前 3 闸是条件链；状态列为 samples/quickstart 实测",
           10, f["faint"], max_w=316)

    gate_top, gate_h = 196, 46
    rail_x = 340
    # spine: the chain segment is drawn in the accent colour, the rest neutral
    v.rect(rail_x - 1.25, gate_top + 6, 2.5, 3 * gate_h - 6,
           fill=f["accent"], rx=1.25, opacity=0.7)
    v.rect(rail_x - 1.25, gate_top + 3 * gate_h, 2.5, 5 * gate_h - 6,
           fill=f["rule"], rx=1.25)
    state_style = {
        "hit": (f["warn"], f["warn_bg"], "命中 1"),
        "pass": (f["ok"], f["ok_bg"], "通过"),
        "skip": (f["sub"], f["skip_bg"], "跳过"),
    }
    for index, (rid, kind, field, state) in enumerate(GATES):
        y = gate_top + index * gate_h
        if index:
            v.line(352, y, 682, y, stroke=f["rule"], sw=1, opacity=0.7)
        v.circle(rail_x, y + 23, 3.4,
                 fill=f["accent"] if index < 3 else f["faint"])
        v.text(356, y + 20, rid, 13.5, f["text"], weight=700, mono=True,
               max_w=52)
        v.text(412, y + 20, kind, 11, f["faint"], mono=True, max_w=150)
        v.text(356, y + 38, field, 13, f["sub"], mono=True, max_w=232)
        fg, bg, label = state_style[state]
        v.chip_right(682, y + 11, label, fg, bg, size=10.5, height=22,
                     weight=700)

    # ---- ladder -> the two exits -------------------------------------------
    v.path("M700 384H715", stroke=f["accent"], sw=1.6, opacity=0.85)
    v.path("M715 300V470", stroke=f["accent"], sw=1.6, opacity=0.85)
    v.arrow_right(715, 730, 300, f["accent"], sw=1.6)
    v.arrow_right(715, 730, 470, f["accent"], sw=1.6)

    # ---- output: two channels, one report ----------------------------------
    v.rect(730, 140, 326, 60, fill=f["panel"], rx=16, stroke=f["edge"],
           sw=1.5, shadow=True)
    v.text(750, 164, "report · buildView()", 11, f["faint"], mono=True,
           max_w=150)
    v.text(1036, 164, "samples/quickstart", 11, f["faint"], mono=True,
           anchor="end", max_w=140)
    v.text(750, 188, "error 0 · warn 1 · info 0", 13, f["text"], weight=700,
           mono=True, max_w=180)
    v.text(1036, 188, "issues 1", 11, f["sub"], mono=True, anchor="end",
           max_w=70)

    v.rect(730, 208, 326, 180, fill=f["card"], rx=18, stroke=f["edge"],
           sw=1.5, shadow=True)
    v.rect(733, 220, 4, 156, fill=f["warn"], rx=2, opacity=0.9)
    v.text(754, 236, "EXIT A · issues[]", 13, f["text"], weight=700, mono=True,
           max_w=190)
    v.chip_right(1036, 222, "1 条 · warn", f["warn"], f["warn_bg"], size=10.5,
                 height=22)
    v.rich(754, 262, [("EC-001", f["accent"], "mono_bold"),
                      (" · warn · 第 1 行 · ", f["sub"], "cjk"),
                      ("controlled", f["sub"], "mono")], 11, max_w=268)
    v.text(754, 286, "第 1 行「controlled」为空", 13, f["text"], max_w=268)
    v.text(754, 310, "expected：「controlled」应填写", 11, f["sub"],
           max_w=268)
    v.text(754, 332, "fix：补填是否受控；本条只核对是否声明，", 11, f["sub"],
           max_w=268)
    v.text(754, 348, "不判断该判断是否正确。", 11, f["sub"], max_w=268)
    v.text(754, 372, "locator { row: 1, column: controlled }", 11, f["faint"],
           mono=True, max_w=268)

    v.rect(730, 396, 326, 170, fill=f["card"], rx=18, stroke=f["edge"],
           sw=1.5, shadow=True)
    v.rect(733, 408, 4, 146, fill=f["accent"], rx=2, opacity=0.55)
    v.text(754, 424, "EXIT B · skipped[]", 13, f["text"], weight=700,
           mono=True, max_w=200)
    v.chip_right(1036, 410, "2 条", f["accent"], f["pill"], size=10.5,
                 height=22)
    v.text(754, 450, "跑不了的检查逐条写原因，绝不静默通过", 11, f["sub"],
           max_w=268)
    v.rich(754, 476, [("EC-002 ", f["accent"], "mono_bold"),
                      ("没有满足「controlled」条件的行", f["sub"], "cjk")],
           10.5, max_w=268)
    v.rich(754, 496, [("EC-007 ", f["accent"], "mono_bold"),
                      ("规则库未配置 values（category）", f["sub"], "cjk")],
           10.5, max_w=268)
    v.text(754, 520, "skipped 只装没能执行的检查，不进 issues[]", 11,
           f["faint"], max_w=268)
    v.text(754, 544, "为空时报告写明「全部检查项均已执行」", 11, f["faint"],
           max_w=268)

    # ---- footer -------------------------------------------------------------
    v.line(44, 578, 1056, 578, stroke=f["rule"], sw=1, opacity=0.75)
    v.text(44, 602, "条件链只在条件成立时才换检查对象：controlled 命中 "
                    "conditionValues → 查 licenseNo；证号已填 → 查 licenseAt。",
           12, f["sub"], max_w=1000)
    v.text(44, 624, "issues[] 为空 ≠ 没问题：没能执行的检查进 skipped[] 并写明"
                    "原因；跑过而未命中的规则两栏都不进。", 11, f["sub"],
           max_w=1000)
    v.text(44, 646, "只读 · 不联网 · 不调用模型 · 不写材料文件 · 不持有管制清单，"
                    "也不判定是否受控或许可。", 11, f["faint"], max_w=760)
    v.text(1056, 646, "4 direct + 4 derived-from-principle · 只读", 11,
           f["faint"], anchor="end", max_w=300)

    if v.bad:
        raise SystemExit("FATAL: SVG label overflow:\n  " + "\n  ".join(v.bad))
    return v.svg(
        W, H,
        "dsh-export-ctl-check: two inputs, eight gates, two exits, one report",
        "A register (JSON or YAML: four optional header scalars, rows[] with "
        "13 canonical column aliases) and the versioned rule pack enter from "
        "the left. Eight gates are stacked in one ladder. The first three form "
        "the only conditional chain: EC-001 presence on controlled, EC-002 "
        "conditionalPresence asking for licenseNo when controlled holds one of "
        "the configured values, EC-003 conditionalPresence asking for "
        "licenseAt when licenseNo is filled. The other five are independent: "
        "EC-004 presenceAny over endUse and endUser, EC-005 presence on "
        "destination, EC-006 uniqueness of licenseNo, EC-007 enum over the "
        "institution's category values, EC-008 containsAny placeholder terms "
        "in itemName. Each gate leaves through exactly one exit: issues[] for "
        "what it found, skipped[] for what it could not run, with the reason. "
        "In the quickstart run one gate hits (EC-001: controlled empty on row "
        "1, warn), two are skipped (EC-002: no row satisfies the controlled "
        "condition; EC-007: values ship empty) and five pass. Both exits "
        "converge on one report, error 0 / warn 1 / info 0, issueCount 1, "
        "skippedCount 2, rulesetVersion 2026.1, rendered as markdown plus "
        "reportJson. Read-only, offline, no model call, no control list held.",
    )


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for skin in ("light", "dark"):
        for lang in ("zh", "en"):
            hero(lang, skin)
        name = f"{NAME}-flow-v5-{skin}.svg"
        text = flow_svg(skin)
        ET.fromstring(text)  # never ship malformed XML
        with open(os.path.join(OUT, name), "w", encoding="utf-8",
                  newline="\n") as fh:
            fh.write(text)
        print(f"wrote {name} (1100x660)")


if __name__ == "__main__":
    main()
