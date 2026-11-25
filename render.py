#!/usr/bin/env python3
"""Render the front page of 'The World Today' for Wednesday, 25 November 2026.

A 1024x1024 newspaper front page drawn with Pillow: a big serif masthead,
one lead story and five more world stories, each with a small pictogram
drawn in code. No photos, no downloaded assets, no network calls.

Stories, each checked against wire reporting dated 25 November 2026:
  1. LEAD  China launches Shenzhou-24; first foreign astronaut (Pakistan)
           reaches the Tiangong station
  2. Australia and the Solomon Islands sign a security pact in Sydney
  3. Zelenskiy confirms a Ukrainian drone hit a Russian cargo ship
  4. Houthis hit Riyadh's tallest tower; 11 people injured
  5. WHO evacuates staff from a hospital in Akwe, DR Congo (Ebola zone)
  6. Cartagena standoff: 10 of about 30 hostages freed from a supermarket
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024
MARGIN = 40
RIGHT = W - MARGIN

PAPER = (247, 243, 232)
INK = (26, 30, 38)
TEAL = (13, 77, 77)
RUST = (138, 28, 28)
GOLD = (178, 140, 44)
GREY = (97, 93, 83)
PALE = (198, 188, 160)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font_file(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(size):
    return font_file("DejaVuSerif-Bold.ttf", size)


def serif_r(size):
    return font_file("DejaVuSerif.ttf", size)


def sans_b(size):
    return font_file("DejaVuSans-Bold.ttf", size)


def sans_r(size):
    return font_file("DejaVuSans.ttf", size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; every returned line fits inside max_w."""
    out, cur = [], ""
    for word in text.split():
        cand = word if not cur else cur + " " + word
        if d.textlength(cand, font=fnt) <= max_w:
            cur = cand
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def para(d, x, y, text, fnt, max_w, step, color=INK):
    """Draw a wrapped paragraph starting at (x, y); return y below it."""
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=color)
        y += step
    return y


def hline(d, y, weight=1, color=INK, x0=MARGIN, x1=RIGHT):
    d.line([(x0, y), (x1, y)], fill=color, width=weight)


# ---------------------------------------------------------------- pictograms

def pic_rocket(d, cx, cy, s):
    """Shenzhou-24 lifting off: body, nose cone, fins, flame, stars."""
    # flame
    d.polygon([(cx - 13, cy + s - 6), (cx + 13, cy + s - 6),
               (cx, cy + s + 26)], fill=GOLD)
    d.polygon([(cx - 7, cy + s - 6), (cx + 7, cy + s - 6),
               (cx, cy + s + 14)], fill=RUST)
    # fins
    d.polygon([(cx - 22, cy + s - 26), (cx - 22, cy + s - 2),
               (cx - 40, cy + s + 2), (cx - 22, cy + s - 12)], fill=RUST)
    d.polygon([(cx + 22, cy + s - 26), (cx + 22, cy + s - 2),
               (cx + 40, cy + s + 2), (cx + 22, cy + s - 12)], fill=RUST)
    # body
    d.rectangle([cx - 22, cy - s + 18, cx + 22, cy + s - 6], fill=TEAL)
    # nose cone
    d.polygon([(cx - 22, cy - s + 18), (cx + 22, cy - s + 18),
               (cx, cy - s - 16)], fill=RUST)
    # window
    d.ellipse([cx - 9, cy - 18, cx + 9, cy], fill=PAPER, outline=INK, width=2)
    # exhaust smoke puffs
    for ox, oy, r in ((-30, s + 18, 7), (28, s + 22, 8), (0, s + 32, 6)):
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r],
                  outline=GREY, width=2)
    # stars
    for sx, sy in ((cx - 46, cy - s + 4), (cx + 48, cy - 10),
                   (cx - 44, cy + 6)):
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)


def pic_pacific(d, cx, cy, s):
    """Pacific map: Australia, Solomon Islands, dashed pact arrow."""
    d.rounded_rectangle([cx - s - 8, cy - s, cx + s + 8, cy + s],
                        radius=12, outline=TEAL, width=4)
    # Australia: simplified blob, lower left
    d.polygon([(cx - s + 4, cy + 8), (cx - s + 18, cy - 8),
               (cx - s + 44, cy - 12), (cx - s + 52, cy + 2),
               (cx - s + 40, cy + 22), (cx - s + 14, cy + 26)],
              fill=TEAL)
    # Solomon Islands: three dots, upper right
    for ix, iy in ((cx + 22, cy - 26), (cx + 36, cy - 18),
                   (cx + 48, cy - 10)):
        d.ellipse([ix - 5, iy - 5, ix + 5, iy + 5], fill=RUST)
    # dashed arrow from Australia to the Solomons
    x0, y0 = cx - s + 40, cy - 8
    x1, y1 = cx + 24, cy - 24
    steps = 7
    for k in range(steps):
        t0 = k / steps
        t1 = (k + 0.55) / steps
        d.line([(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0),
                (x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)],
               fill=GOLD, width=3)
    # arrowhead
    d.polygon([(x1, y1), (x1 - 10, y1 - 2), (x1 - 4, y1 + 8)], fill=GOLD)


def pic_ship(d, cx, cy, s):
    """Cargo ship on waves, with containers and a mast."""
    # containers
    d.rectangle([cx - s + 4, cy - 34, cx - s + 26, cy - 12], fill=RUST)
    d.rectangle([cx - s + 30, cy - 34, cx - s + 52, cy - 12], fill=GOLD)
    d.rectangle([cx - s + 56, cy - 34, cx - s + 78, cy - 12], fill=TEAL)
    # bridge tower
    d.rectangle([cx + s - 26, cy - 52, cx + s - 6, cy - 12], fill=INK)
    d.rectangle([cx + s - 22, cy - 46, cx + s - 10, cy - 38],
                fill=PAPER)
    # mast + flag (kept short so it stays below the kicker above)
    d.line([(cx + s - 16, cy - 52), (cx + s - 16, cy - 62)],
           fill=INK, width=3)
    d.polygon([(cx + s - 16, cy - 62), (cx + s + 2, cy - 58),
               (cx + s - 16, cy - 54)], fill=RUST)
    # hull
    d.polygon([(cx - s, cy - 12), (cx + s, cy - 12),
               (cx + s - 14, cy + 16), (cx - s + 14, cy + 16)], fill=TEAL)
    # waves (kept inside the pictogram column, clear of the body text)
    for wy in (cy + 26, cy + 38):
        for k in range(3):
            x0 = cx - s + 2 + k * 24
            d.arc([x0, wy - 6, x0 + 20, wy + 6], 180, 360,
                  fill=TEAL, width=3)


def pic_tower(d, cx, cy, s):
    """Riyadh's tallest tower: stepped skyscraper, impact burst on top."""
    # main shaft with setbacks
    d.rectangle([cx - 26, cy - s + 26, cx + 26, cy + s - 4], fill=TEAL)
    d.rectangle([cx - 18, cy - s + 6, cx + 18, cy - s + 26], fill=TEAL)
    d.rectangle([cx - 10, cy - s - 8, cx + 10, cy - s + 6], fill=TEAL)
    # antenna (short, so it stays below the kicker above)
    d.line([(cx, cy - s - 8), (cx, cy - s - 14)], fill=INK, width=3)
    # windows
    for row in range(4):
        yy = cy - s + 40 + row * 16
        for col in range(3):
            xx = cx - 18 + col * 14
            d.rectangle([xx, yy, xx + 8, yy + 8], fill=PAPER)
    # impact burst at the top corner
    bx, by = cx - 26, cy - s + 14
    for ang in range(0, 360, 30):
        rad = math.radians(ang)
        x0 = bx + int(math.cos(rad) * 8)
        y0 = by + int(math.sin(rad) * 8)
        x1 = bx + int(math.cos(rad) * 20)
        y1 = by + int(math.sin(rad) * 20)
        d.line([(x0, y0), (x1, y1)], fill=RUST, width=3)
    d.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=GOLD)
    # ground line
    d.line([(cx - 34, cy + s - 4), (cx + 34, cy + s - 4)],
           fill=INK, width=3)


def pic_hospital(d, cx, cy, s):
    """Hospital building with a big cross sign and an ambulance cross."""
    # sign post + cross emblem above the roof
    d.rectangle([cx - 24, cy - s - 2, cx + 24, cy - s + 30],
                fill=RUST)
    d.rectangle([cx - 6, cy - s + 4, cx + 6, cy - s + 24], fill=PAPER)
    d.rectangle([cx - 18, cy - s + 10, cx + 18, cy - s + 18], fill=PAPER)
    # building
    d.rectangle([cx - s + 6, cy - s + 30, cx + s - 6, cy + s - 4],
                fill=TEAL)
    # windows
    for row in range(2):
        yy = cy - s + 46 + row * 22
        for col in range(4):
            xx = cx - s + 16 + col * 20
            d.rectangle([xx, yy, xx + 11, yy + 11], fill=PAPER)
    # door
    d.rectangle([cx - 9, cy + s - 24, cx + 9, cy + s - 4], fill=PAPER)
    # small cross badge on the wall
    d.ellipse([cx + s - 24, cy + s - 26, cx + s - 6, cy + s - 8],
              fill=GOLD)
    d.text((cx + s - 21, cy + s - 25), "+", font=sans_b(15), fill=RUST)


def pic_market(d, cx, cy, s):
    """Supermarket storefront: striped awning, windows, door, cart."""
    # awning with alternating stripes
    for k in range(6):
        x0 = cx - s + 4 + k * 16
        col = RUST if k % 2 == 0 else PAPER
        d.polygon([(x0, cy - s + 6), (x0 + 16, cy - s + 6),
                   (x0 + 16, cy - s + 26), (x0, cy - s + 26)], fill=col)
    d.rectangle([cx - s + 4, cy - s + 6, cx + s - 4, cy - s + 26],
                outline=INK, width=2)
    # storefront
    d.rectangle([cx - s + 4, cy - s + 26, cx + s - 4, cy + s - 4],
                outline=TEAL, width=4)
    # windows with goods
    d.rectangle([cx - s + 12, cy - s + 38, cx - 8, cy + s - 26],
                fill=TEAL)
    d.rectangle([cx - s + 18, cy - s + 44, cx - s + 34, cy - s + 60],
                fill=GOLD)
    d.rectangle([cx - s + 40, cy - s + 44, cx - s + 56, cy - s + 60],
                fill=RUST)
    d.rectangle([cx - s + 18, cy - s + 66, cx - s + 34, cy - s + 82],
                fill=RUST)
    d.rectangle([cx - s + 40, cy - s + 66, cx - s + 56, cy - s + 82],
                fill=GOLD)
    # door
    d.rectangle([cx + 2, cy - s + 38, cx + s - 12, cy + s - 26],
                fill=PAPER, outline=INK, width=2)
    d.ellipse([cx + s - 20, cy - 6, cx + s - 16, cy - 2], fill=RUST)
    # shopping cart in front (kept clear of the footer rule below)
    d.polygon([(cx - s + 14, cy + s - 8), (cx + s - 6, cy + s - 8),
               (cx + s - 14, cy + s + 6), (cx - s + 22, cy + s + 6)],
              outline=RUST, width=3)
    for wx in (cx - s + 26, cx + s - 16):
        d.ellipse([wx - 4, cy + s + 8, wx + 4, cy + s + 16], fill=INK)


# ------------------------------------------------------------------- page

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead block ----
    hline(d, 28, 2)
    d.text((MARGIN, 40), "WEDNESDAY, 25 NOVEMBER 2026",
           font=sans_b(18), fill=INK)
    tag = "WORLD EDITION  \u2022  No. 329"
    d.text((RIGHT - d.textlength(tag, font=sans_b(16)), 42), tag,
           font=sans_b(16), fill=GREY)

    name = "The World Today"
    nw = d.textlength(name, font=serif_b(88))
    d.text(((W - nw) / 2, 64), name, font=serif_b(88), fill=INK)

    motto = "S I X   S T O R I E S   F R O M   A R O U N D   T H E   G L O B E"
    mw = d.textlength(motto, font=sans_b(15))
    d.text(((W - mw) / 2, 162), motto, font=sans_b(15), fill=TEAL)

    hline(d, 190, 3)
    hline(d, 196, 1)

    # ---- lead story: Shenzhou-24 ----
    y = 212
    d.text((MARGIN, y), "LEAD STORY  \u2014  SPACE", font=sans_b(17),
           fill=RUST)
    y += 30
    for line in ("China launches Shenzhou-24",
                 "carrying first foreign astronaut"):
        d.text((MARGIN, y), line, font=serif_b(37), fill=INK)
        y += 45
    y += 4
    y = para(
        d, MARGIN, y,
        "Shenzhou-24 lifted off from Jiuquan at 00:18 UTC on Wednesday, "
        "carrying commander Tang Hongbo, Wu Yi and Pakistan's Muhammad "
        "Zeeshan Ali \u2014 the first foreign astronaut to visit China's "
        "Tiangong space station.",
        sans_r(19), 606, 25)
    pic_rocket(d, 856, 318, 74)

    hline(d, 450, 2, PALE)

    # ---- grid: four stories, two columns by two rows ----
    stories = [
        ("SECURITY", "Australia, Solomons sign security pact",
         "Signed in Sydney on Wednesday, the pact makes Canberra the "
         "Solomons' partner of choice for defence. The islands' security "
         "deal with China was reportedly scrapped.",
         pic_pacific, (46, 54, 46)),
        ("UKRAINE", "Zelenskiy confirms Ukraine hit Russian ship",
         "Kyiv confirmed a drone strike on a Russian cargo ship in the "
         "Gulf of Finland on Saturday. All 16 crew were evacuated; "
         "Norway urged caution.",
         pic_ship, (46, 58, 44)),
        ("MIDDLE EAST", "Houthis hit Riyadh's tallest tower",
         "A strike hit a tower in Riyadh's financial district, injuring "
         "11 people \u2014 two Indians, two Saudis, three Nepalis and "
         "four Egyptians, civil defence said.",
         pic_tower, (46, 58, 44)),
        ("HEALTH", "WHO evacuates staff from DR Congo hospital",
         "WHO staff were evacuated from a hospital in Akwe, Ituri, after "
         "sheltering three days from fighting. The area is an Ebola "
         "outbreak zone.",
         pic_hospital, (46, 52, 44)),
    ]
    col_w = 457
    col_x = [MARGIN, MARGIN + col_w + 30]
    row_y = [466, 656]
    for i, (kick, head, body, pic, (px, py, ps)) in enumerate(stories):
        x = col_x[i % 2]
        yy = row_y[i // 2]
        d.text((x, yy), kick, font=sans_b(15), fill=RUST)
        yy += 24
        pic(d, x + px, yy + py, ps)
        tx = x + 104
        for line in wrap(d, head, serif_b(23), col_w - 104):
            d.text((tx, yy), line, font=serif_b(23), fill=INK)
            yy += 28
        yy += 6
        para(d, tx, yy, body, sans_r(16), col_w - 104, 21)
        if i % 2 == 0:
            d.line([(x + col_w + 15, row_y[i // 2] - 4),
                    (x + col_w + 15, row_y[i // 2] + 176)],
                   fill=PALE, width=1)
    hline(d, 644, 1, PALE)

    # ---- bottom strip: Cartagena standoff ----
    y = 860
    hline(d, 848, 2, PALE)
    pic_market(d, MARGIN + 46, y + 54, 48)
    tx = MARGIN + 112
    d.text((tx, y), "COLOMBIA", font=sans_b(15), fill=RUST)
    d.text((tx, y + 24), "Cartagena standoff: 10 of 30 hostages freed",
           font=serif_b(27), fill=INK)
    para(
        d, tx, y + 62,
        "Armed men holding about 30 people in a Cartagena \u00c9xito "
        "supermarket after a failed cash-truck robbery freed 10 elderly "
        "women hostages; about 20 remain held, President Abelardo de la "
        "Espriella said.",
        sans_r(16), RIGHT - tx, 21)

    # ---- footer ----
    hline(d, 984, 1)
    d.text((MARGIN, 994),
           "Sources: Xinhua  \u2022  Reuters  \u2022  WHO  \u2022  Sky News"
           "  \u2022  AP",
           font=sans_r(14), fill=GREY)
    foot_r = "Compiled Wednesday, 25 November 2026 (UTC)"
    d.text((RIGHT - d.textlength(foot_r, font=sans_r(14)), 994),
           foot_r, font=sans_r(14), fill=GREY)

    return img


def main():
    img = build()
    out = os.path.join(BASE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
