#!/usr/bin/env python3
"""Render the 20 November 2026 world-news front page (1024x1024).

A dense broadsheet front page drawn with PIL and real TTF fonts:
  - Noto Serif Display Black for the masthead
  - Noto Serif Bold / Regular for headlines and body
  - DejaVu Sans for kickers, labels and briefs

Layout (top to bottom): masthead + date line, the TOP 3 lead stories,
9 smaller stories in a 3x3 grid, 24 one-line briefs in 2 columns,
and a footer with a confidence note and sources.

Run once:   python3 render_20nov.py
Writes:      entry.png  (1024x1024, deterministic)
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 28
CW = W - 2 * MARGIN  # content width: 968

PAPER = (248, 244, 234)
INK = (18, 18, 18)
GRAY = (74, 74, 74)
RED = (178, 28, 28)
RULE = (30, 30, 30)
FAINT = (205, 198, 184)

DISPLAY_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerif-Black.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, text, fnt, max_w, fill=INK, spacing=4):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def rule(draw, x, y, w, weight=2):
    draw.rectangle([x, y, x + w, y + weight - 1], fill=RULE)


def kicker(draw, x, y, text, size=12):
    fnt = font(SANS_BOLD, size)
    draw.text((x, y), text.upper(), font=fnt, fill=RED)
    return y + size + 5


def section_head(draw, x, y, text):
    """Small section header with a rule above it; returns y below it."""
    rule(draw, x, y, CW, 2)
    y += 7
    fnt = font(SANS_BOLD, 12)
    draw.text((x, y), text.upper(), font=fnt, fill=INK)
    return y + 12 + 6


# ---------------------------------------------------------------- content
MASTHEAD = "THE WORLD"
DATE_LINE = "FRIDAY, 20 NOVEMBER 2026"
EDITION = "THE DAY'S WORLD NEWS  •  ONE PAGE  •  No. 325"

LEAD = {
    "kicker": "The lead  •  War in Ukraine",
    "head": "RUSSIA SMASHES KYIV'S BRIDGES — 3 DEAD",
    "body": (
        "An overnight ballistic-missile attack on Kyiv into Friday hit three "
        "Dnipro bridges — Podilsko-Voskresenskyi, Darnytskyi and Pivdennyi — "
        "the biggest strikes on the capital's river crossings since the war "
        "began. Mayor Klitschko: 3 killed, about 15 injured; fires in "
        "Obolonskyi and Podilskyi districts. Putin vowed \"painful\" "
        "retaliation after Ukraine's third strike this week on the Kerch Bridge."
    ),
    "facts": (
        "3 KILLED  •  ~15 INJURED  •  3 DNIPRO BRIDGES HIT  •  "
        "PUTIN VOWS \"PAINFUL\" RETALIATION"
    ),
}

TOP2 = {
    "kicker": "Markets",
    "head": "ASIA'S AI ROUT — NIKKEI -5%, TAIEX -6%",
    "body": (
        "Asian shares crashed Friday, the worst week since 2020, as "
        "Anthropic's debut failed to restore faith in the AI trade. Nikkei "
        "-5.06% at 56,436.65; Taiex -6.23% at 36,033.29, its worst week since "
        "1991; Kospi -5.7%. SoftBank -14.6%, TSMC -5.2%, Foxconn -5.4%. US "
        "stocks fell a fifth straight day on Thursday (S&P -2%, Nasdaq -2.2%)."
    ),
}

TOP3 = {
    "kicker": "Weather",
    "head": "CYCLONE AKVAN MAKES LANDFALL IN INDIA",
    "body": (
        "The third storm to hit India in under a month, Akvan made landfall "
        "Friday morning near Gopalpur on the Odisha–Andhra Pradesh coast, "
        "70–80 kph with gusts to 90 kph (IMD). More than 120,000 were "
        "evacuated in Odisha and 9,299 shelters opened; \"no damage or "
        "untoward incident reported so far\". It weakened to a deep depression "
        "within hours."
    ),
}

SMALL9 = [
    ("COP31", "Fossil fuels erased from draft",
     "Closing day in Antalya: draft slimmed 144 to 80 paragraphs, drops every "
     "mention of fossil fuels; 35% electrification target survives."),
    ("US / Iran", "Trump: no new Iran strikes in 2026",
     "\"I am not rushing into any decision [on Iran]. We will see what happens "
     "after the beginning of the year.\" Netanyahu presses for a joint campaign."),
    ("Tech", "Anthropic slips after record IPO",
     "Shares fell ~5% post-market; debut closed $97.17 (+17% on the $83 "
     "offer). Total raise $107.3bn; joins MSCI Large Cap on 30 Nov."),
    ("Asia", "Prabowo meets Xi in Shenzhen",
     "Indonesia's President Prabowo met China's Xi at Kylin Villa, discussing "
     "economy, investment and South China Sea joint development."),
    ("Crime", "US sanctions Comancheros, 'Ndrangheta",
     "OFAC sanctioned the Australia-based biker gang and Italy's 'Ndrangheta "
     "under EO 14059 for aiding cartels; 'Ndrangheta in 80+ countries."),
    ("Tech", "US approved 879,000 AI chips for China",
     "Commerce Dept approved 879,000 Nvidia H200 / AMD MI325X shipments to "
     "China, Dec 2025–May 2026, of 3.4m requested: Tencent 150,000."),
    ("Gulf", "Saudis intercept Houthi missile",
     "Saudi air defences destroyed a Houthi ballistic missile aimed at the "
     "southern region Friday; drones also intercepted, alerts for Jazan."),
    ("Italy", "Italy: 24-hour general strike",
     "CGIL, Italy's biggest union, struck nationwide Friday against the "
     "Meloni government's 2027 budget — buses, trams, metros, schools stop."),
    ("Tech", "Samsung's new mobile chief",
     "Samsung named Won-Joon Choi head of Mobile eXperience (MX), ending TM "
     "Roh's near-7-year run; Roh stays co-CEO and DX head."),
]

BRIEFS = [
    "M5.6 quake SE of Loyalty Islands — 00:49 UTC, 10 km deep; no tsunami.",
    "NFL: Texans rout Colts 26-3 — C.J. Stroud threw 3 TDs, first home win.",
    "NATO jets scrambled as Russian missiles reportedly breached Polish airspace.",
    "UK to send Ukraine 1,000+ long-range drones — 1,000 km range, £260m.",
    "Trump pardons Pete Rose posthumously — 4,256-hit king, banned since 1989.",
    "Tbilisi gas explosion kills 6, incl. 2 children, in a 5-storey block.",
    "Tower-block fire in Fontenay-sous-Bois, Paris — 1 dead, ~30 injured.",
    "Genoa airport shut ~2 hours by drones — flights held, incl. ITA AZ1392.",
    "Houthi missile damages Riyadh's 80-storey PIF Tower. (Thu, reported Fri.)",
    "US Senate rejects Iran war-powers resolution 51-48 on Thursday night.",
    "Bukele launches third-term candidacy in El Salvador on Thursday night.",
    "Israel's first ground operation into unoccupied Gaza since the ceasefire.",
    "Iran claims it shot down a US MQ-9 drone east of Hormuz. (Unverified.)",
    "U-17 World Cup opens in Qatar — France 3-1 Haiti, Australia 2-0 Argentina.",
    "White House taps Kirsten Davies as cyber chief after widespread US outages.",
    "US court limits Agriculture Secretary Rollins' religious emails to staff.",
    "Kamala Harris meets Emmanuel Macron in Paris amid 2028 speculation.",
    "13,000 march in Tokyo against Takaichi government policies.",
    "Senegal migrant boat capsizes, 4 killed, amid a migration surge.",
    "Spain general strike disrupts ports and factories.",
    "Europe-wide youth protests over living costs, housing and education.",
    "Thai PM Anutin meets Putin on the APEC sidelines in Shenzhen.",
    "Google adds Mac computer control to Gemini.",
    "Broadcom patches critical VMware vCenter flaw, urges immediate updates.",
]

FOOTER_NOTE = (
    "HOW SURE ARE WE:  Figures are as reported on 20 November 2026. Where a number was "
    "still moving (markets, the cyclone track) we give the day's reported value. "
    "Sources: Reuters, AP, Bloomberg, USGS, Samsung, UN, US Treasury."
)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x = MARGIN
    y = 22

    # ---- masthead ----
    mast = font(DISPLAY_BLACK, 88)
    tw = d.textlength(MASTHEAD, font=mast)
    d.text(((W - tw) / 2, y), MASTHEAD, font=mast, fill=INK)
    y += 88 + 4
    rule(d, x, y, CW, 3)
    y += 7
    rule(d, x, y, CW, 1)
    y += 9
    # date / edition line
    dl = font(SANS_BOLD, 13)
    ed = font(SANS, 13)
    d.text((x, y), DATE_LINE, font=dl, fill=INK)
    ew = d.textlength(EDITION, font=ed)
    d.text((W - MARGIN - ew, y), EDITION, font=ed, fill=GRAY)
    y += 13 + 8
    rule(d, x, y, CW, 2)
    y += 10

    # ---- LEAD story (TOP 3 #1) ----
    y = kicker(d, x, y, LEAD["kicker"], size=13)
    head = font(SERIF_BLACK, 34)
    y = draw_lines(d, x, y, LEAD["head"], head, CW, spacing=2)
    y += 2
    body = font(SERIF_REG, 16)
    y = draw_lines(d, x, y, LEAD["body"], body, CW, spacing=3)
    y += 3
    facts = font(SANS_BOLD, 12)
    y = draw_lines(d, x, y, LEAD["facts"], facts, CW, fill=RED, spacing=2)
    y += 6
    rule(d, x, y, CW, 2)
    y += 8

    # ---- TOP 3 #2 and #3, two columns (both start at the same top) ----
    col_w = (CW - 24) // 2
    start_y = y
    bottom = start_y
    for i, story in enumerate((TOP2, TOP3)):
        cx = x + i * (col_w + 24)
        cy = kicker(d, cx, start_y, story["kicker"], size=12)
        hd = font(SERIF_BOLD, 21)
        cy = draw_lines(d, cx, cy, story["head"], hd, col_w, spacing=1)
        cy += 1
        bd = font(SERIF_REG, 14)
        cy = draw_lines(d, cx, cy, story["body"], bd, col_w, spacing=2)
        bottom = max(bottom, cy)
    col_y = bottom
    # vertical divider between the two columns
    mid = x + col_w + 12
    d.line([mid, y, mid, col_y - 4], fill=FAINT, width=1)
    y = col_y + 4
    rule(d, x, y, CW, 2)
    y += 6

    # ---- SMALL 9 grid (3 cols x 3 rows) ----
    y = section_head(d, x, y, "More of the day")
    gap = 16
    cell_w = (CW - 2 * gap) // 3
    cell_h = 75
    for row in range(3):
        row_y = y + row * cell_h
        for col in range(3):
            s = SMALL9[row * 3 + col]
            cx = x + col * (cell_w + gap)
            cy = kicker(d, cx, row_y, s[0], size=10)
            hd = font(SERIF_BOLD, 15)
            cy = draw_lines(d, cx, cy, s[1], hd, cell_w, spacing=0)
            bd = font(SERIF_REG, 12)
            draw_lines(d, cx, cy, s[2], bd, cell_w, spacing=1)
        # faint row divider (not after the last row)
        if row < 2:
            d.line([x, row_y + cell_h - 8, x + CW, row_y + cell_h - 8],
                   fill=FAINT, width=1)
    y += 3 * cell_h - 4
    rule(d, x, y, CW, 2)
    y += 6

    # ---- BRIEFS 24 (2 cols x 12 rows) ----
    y = section_head(d, x, y, "In brief")
    bcol_w = (CW - 24) // 2
    bf = font(SANS, 11)
    row_h = 17
    for i, b in enumerate(BRIEFS):
        col = 0 if i < 12 else 1
        row = i % 12
        bx = x + col * (bcol_w + 24)
        by = y + row * row_h
        d.rectangle([bx, by + 4, bx + 5, by + 9], fill=RED)
        # keep each brief to one line: shorten only if it would overflow
        txt = b
        while d.textlength(txt, font=bf) > bcol_w - 12 and len(txt) > 20:
            txt = txt.rsplit(" ", 1)[0] + "…"
        d.text((bx + 10, by), txt, font=bf, fill=INK)
    y += 12 * row_h + 2
    rule(d, x, y, CW, 2)
    y += 6

    # ---- footer: confidence note ----
    ff = font(SERIF_ITALIC, 12)
    y = draw_lines(d, x, y, FOOTER_NOTE, ff, CW, fill=GRAY, spacing=2)
    y += 2
    fin = font(SANS_BOLD, 10)
    tag = "THE WORLD  •  20 NOVEMBER 2026  •  ONE DAY, ONE PAGE"
    tw = d.textlength(tag, font=fin)
    d.text(((W - tw) / 2, y), tag, font=fin, fill=GRAY)
    print("final y:", y)

    img.save("entry.png", format="PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
