#!/usr/bin/env python3
"""Render THE WORLD — Friday 20 November 2026, a one-page newspaper front page.

Draws the day's world news (TOP3 + SMALL9 + 24 briefs) with Pillow onto a
1024x1024 canvas: masthead, lead story, two-column section, a 3x3 grid, an
in-brief list, and a footer legend. Deterministic: same input, same bytes.
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 28
CW = W - 2 * MARGIN  # 968 content width
GUTTER = 16
COLW = (CW - GUTTER) // 2  # 476
CELLW = (CW - 2 * GUTTER) // 3  # 312
BLACK = (0, 0, 0)
RED = (178, 24, 24)
GREY = (90, 90, 90)

FONT_DIR = "/usr/share/fonts/truetype"
MASTHEAD = os.path.join(FONT_DIR, "noto", "NotoSerif-Black.ttf")
BOLD = os.path.join(FONT_DIR, "noto", "NotoSerif-Bold.ttf")
REGULAR = os.path.join(FONT_DIR, "noto", "NotoSerif-Regular.ttf")
ITALIC = os.path.join(FONT_DIR, "noto", "NotoSerif-Italic.ttf")
KICKER = os.path.join(FONT_DIR, "dejavu", "DejaVuSans-Bold.ttf")


def font(path, size):
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, path, start, max_width, max_lines, min_size=10):
    """Shrink the font until the text wraps into at most max_lines."""
    size = start
    while size > min_size:
        fnt = font(path, size)
        if len(wrap(draw, text, fnt, max_width)) <= max_lines:
            return fnt
        size -= 1
    return font(path, min_size)


def draw_wrapped(draw, x, y, text, fnt, max_width, lh, color=BLACK):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=color)
        y += lh
    return y


def rule(draw, x0, x1, y, width=1):
    draw.line([(x0, y), (x1, y)], fill=BLACK, width=width)


def main():
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN

    # ---- Masthead ----
    f_mast = fit_lines(d, "THE WORLD", MASTHEAD, 88, CW, 1, min_size=60)
    d.text((W // 2, 10), "THE WORLD", font=f_mast, fill=BLACK, anchor="ma")
    bbox = d.textbbox((W // 2, 10), "THE WORLD", font=f_mast, anchor="ma")
    y = bbox[3] + 8
    rule(d, x0, x1, y, 4)
    y += 10
    f_date = font(BOLD, 14)
    d.text((x0, y), "FRIDAY, 20 NOVEMBER 2026", font=f_date, fill=BLACK)
    right = "THE DAY'S WORLD NEWS  •  ONE PAGE  •  No. 325"
    d.text((x1, y), right, font=f_date, fill=BLACK, anchor="ra")
    y += 22
    rule(d, x0, x1, y, 1)
    y += 8

    # ---- Lead story (full width) ----
    f_kick = font(KICKER, 14)
    d.text((x0, y), "THE LEAD  •  WAR IN UKRAINE", font=f_kick, fill=RED)
    y += 20
    lead_head = "RUSSIA SMASHES KYIV'S BRIDGES — 3 DEAD"
    f_lead = fit_lines(d, lead_head, BOLD, 44, CW, 1, min_size=30)
    d.text((x0, y), lead_head, font=f_lead, fill=BLACK)
    y += 48
    lead_body = (
        "An overnight ballistic-missile attack on Kyiv into Friday hit three "
        "Dnipro bridges — Podilsko-Voskresenskyi, Darnytskyi and Pivdennyi — "
        "the biggest strikes on the capital's river crossings since the war "
        "began. Mayor Klitschko: 3 killed, about 15 injured; fires in "
        "Obolonskyi and Podilskyi districts. Putin vowed “painful” "
        "retaliation after Ukraine's third strike this week on the Kerch Bridge."
    )
    y = draw_wrapped(d, x0, y, lead_body, font(REGULAR, 15), CW, 18)
    y += 4
    d.text((x0, y), "3 KILLED  •  ~15 INJURED  •  3 DNIPRO BRIDGES HIT  •  PUTIN VOWS “PAINFUL” RETALIATION",
           font=font(KICKER, 13), fill=RED)
    y += 20
    rule(d, x0, x1, y, 1)
    y += 6

    # ---- Two-column stories ----
    stories = [
        ("MARKETS", "ASIA'S AI ROUT — NIKKEI -5%, TAIEX -6%",
         "Asian shares crashed Friday, the worst week since 2020, as "
         "Anthropic's debut failed to restore faith in the AI trade. Nikkei "
         "-5.06% at 56,436.65; Taiex -6.23% at 36,033.29, its worst week "
         "since 1991; Kospi -5.7%. SoftBank -14.6%, TSMC -5.2%, Foxconn "
         "-5.4%. US stocks fell a fifth straight day Thursday (S&P -2%, "
         "Nasdaq -2.2%)."),
        ("WEATHER", "CYCLONE AKVAN MAKES LANDFALL IN INDIA",
         "The third storm to hit India in under a month, Akvan made landfall "
         "Friday morning near Gopalpur on the Odisha–Andhra Pradesh coast, "
         "70–80 kph with gusts to 90 kph (IMD). More than 120,000 were "
         "evacuated in Odisha and 9,299 shelters opened; “no damage or "
         "untoward incident reported so far”. It weakened to a deep "
         "depression within hours."),
    ]
    col_y = y
    base_y = y
    for i, (kick, head, body) in enumerate(stories):
        cx = x0 + i * (COLW + GUTTER)
        yy = base_y
        d.text((cx, yy), kick, font=f_kick, fill=RED)
        yy += 20
        f_head = fit_lines(d, head, BOLD, 26, COLW, 2, min_size=20)
        yy = draw_wrapped(d, cx, yy, head, f_head, COLW, 28)
        yy += 2
        yy = draw_wrapped(d, cx, yy, body, font(REGULAR, 13), COLW, 16)
        col_y = max(col_y, yy)
    y = col_y + 6
    rule(d, x0, x1, y, 1)
    y += 6

    # ---- SMALL9 grid ----
    d.text((x0, y), "MORE OF THE DAY", font=font(BOLD, 15), fill=BLACK)
    y += 20
    rule(d, x0, x1, y, 1)
    y += 6
    small = [
        ("COP31", "Fossil fuels erased from draft",
         "Closing day in Antalya: draft slimmed 144 to 80 paragraphs, drops "
         "fossil fuels; 35% target survives."),
        ("US / IRAN", "Trump: no new Iran strikes in 2026",
         "“I am not rushing into any decision [on Iran].” Netanyahu presses "
         "for a joint campaign."),
        ("TECH", "Anthropic slips after record IPO",
         "Shares fell ~5% post-market; debut closed $97.17 (+17%). Total "
         "raise $107.3bn; MSCI Large Cap 30 Nov."),
        ("ASIA", "Prabowo meets Xi in Shenzhen",
         "Indonesia's Prabowo met China's Xi at Kylin Villa, discussing "
         "economy, investment and South China Sea."),
        ("CRIME", "US sanctions Comancheros, ’Ndrangheta",
         "OFAC sanctioned the Comanchero gang and ’Ndrangheta under EO 14059 "
         "for aiding cartels."),
        ("TECH", "US approved 879,000 AI chips for China",
         "US approved 879,000 Nvidia H200 / AMD MI325X chips for China, Dec "
         "2025–May 2026; 3.4m sought."),
        ("GULF", "Saudis intercept Houthi missile",
         "Saudi defences destroyed a Houthi ballistic missile aimed at the "
         "south; drones also intercepted."),
        ("ITALY", "Italy: 24-hour general strike",
         "CGIL, Italy's biggest union, struck nationwide against the Meloni "
         "2027 budget; transport and schools stop."),
        ("TECH", "Samsung's new mobile chief",
         "Samsung named Won-Joon Choi head of Mobile eXperience (MX), "
         "ending TM Roh's near-7-year run."),
    ]
    grid_top = y
    row_h = 90
    for idx, (kick, head, body) in enumerate(small):
        r, c = divmod(idx, 3)
        cx = x0 + c * (CELLW + GUTTER)
        cy = grid_top + r * row_h
        d.text((cx, cy), kick, font=font(KICKER, 11), fill=RED)
        cy += 15
        f_h = fit_lines(d, head, BOLD, 16, CELLW, 2, min_size=12)
        cy = draw_wrapped(d, cx, cy, head, f_h, CELLW, 19)
        draw_wrapped(d, cx, cy, body, font(REGULAR, 12), CELLW, 15)
    y = grid_top + 3 * row_h + 2
    rule(d, x0, x1, y, 1)
    y += 6

    # ---- IN BRIEF ----
    d.text((x0, y), "IN BRIEF", font=font(BOLD, 15), fill=BLACK)
    y += 20
    briefs = [
        "M5.6 quake SE of Loyalty Islands — 00:49 UTC, 10 km deep; no tsunami.",
        "NFL: Texans rout Colts 26–3 — C.J. Stroud threw 3 TDs, first home win.",
        "NATO jets scrambled as Russian missiles reportedly breached Polish airspace.",
        "UK to send Ukraine 1,000+ long-range drones — 1,000 km range, £260m package.",
        "Trump pardons Pete Rose posthumously — 4,256-hit king, banned since 1989.",
        "Tbilisi gas explosion kills 6, incl. 2 children, in a 5-storey block.",
        "Tower-block fire in Fontenay-sous-Bois, Paris — 1 dead, ~30 injured.",
        "Genoa airport shut ~2 hours by drones — flights held, incl. ITA AZ1392.",
        "Houthi missile damages Riyadh's 80-storey PIF Tower. (Thu, reported Fri.)",
        "US Senate rejects Iran war-powers resolution 51–48 on Thursday night.",
        "Bukele launches third-term candidacy in El Salvador on Thursday night.",
        "Israel's first ground operation into unoccupied Gaza since the October ceasefire.",
        "Iran claims it shot down a US MQ-9 drone east of Hormuz. (Unverified.)",
        "U-17 World Cup opens in Qatar — France 3–1 Haiti, Australia 2–0 Argentina.",
        "White House taps Kirsten Davies as cyber chief after widespread US outages.",
        "US court sets interim limits on Agriculture Secretary Rollins' religious emails.",
        "Kamala Harris meets Emmanuel Macron in Paris amid 2028 speculation.",
        "13,000 march in Tokyo against Takaichi government policies.",
        "Senegal migrant boat capsizes, 4 killed, amid a migration surge.",
        "Spain general strike disrupts ports and factories.",
        "Europe-wide youth protests over living costs, housing and education.",
        "Thai PM Anutin meets Putin on the APEC sidelines in Shenzhen.",
        "Google adds Mac computer control to Gemini.",
        "Broadcom patches critical VMware vCenter flaw, urges immediate updates.",
    ]
    left = briefs[:12]
    right = briefs[12:]
    for col, items in enumerate((left, right)):
        cx = x0 + col * (COLW + GUTTER)
        yy = y
        for item in items:
            size = 12
            while size > 10:
                f_b = font(REGULAR, size)
                if d.textlength(item, font=f_b) <= COLW - 14:
                    break
                size -= 1
            d.rectangle([cx, yy + 4, cx + 6, yy + 10], fill=RED)
            d.text((cx + 12, yy), item, font=f_b, fill=BLACK)
            yy += 13
    y += 12 * 13 + 4

    # ---- Footer ----
    legend = (
        "HOW SURE ARE WE: Figures are as reported on 20 November 2026. Where a "
        "number was still moving (markets, the cyclone track) we give the day's "
        "reported value. Sources: Reuters, AP, Bloomberg, USGS, Samsung, UN, "
        "US Treasury."
    )
    y = draw_wrapped(d, x0, y, legend, font(ITALIC, 11), CW, 13, color=GREY)
    y += 2
    d.text((W // 2, y), "THE WORLD  •  20 NOVEMBER 2026  •  ONE DAY, ONE PAGE",
           font=font(BOLD, 12), fill=BLACK, anchor="ma")
    y += 14
    print("final y:", y, "canvas:", H)

    img.save(OUT, "PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
