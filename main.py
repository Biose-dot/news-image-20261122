#!/usr/bin/env python3
"""Draw the make.fun news-image-20261122 entry: a one-page newspaper
front page summing up the world news of Sunday 22 November 2026.

Python 3 stdlib + PIL only. No network, no wall-clock time, no random
numbers: the output is fully deterministic. Writes entry.png into
$MAKEFUN_OUTPUT_DIR (default /output), 1024x1024, under 1 MiB.

Run:  python3 main.py
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
RULE = (17, 17, 17)
ACCENT = (158, 27, 27)          # deep newspaper red
SEA = (38, 84, 124)             # Banda Sea blue
SEA_LIGHT = (120, 165, 198)
LAND = (214, 196, 150)
MUTED = (90, 84, 72)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def fit_serif(draw, text, start, max_w):
    """Largest serif-bold size at or below `start` that fits `max_w`."""
    size = start
    while size > 40 and draw.textlength(text, font=SERIF_B(size)) > max_w:
        size -= 2
    return SERIF_B(size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw wrapped paragraph; returns y after the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def headline(draw, x, y, text, fnt, max_w, leading):
    return para(draw, x, y, text, fnt, max_w, leading)


def rule(draw, x0, y, x1, width=2):
    draw.line([(x0, y), (x1, y)], fill=RULE, width=width)


def kicker(draw, x, y, text):
    draw.text((x, y), text, font=SANS_B(17), fill=ACCENT)


def draw_banda_panel(draw, x0, y0, x1, y1):
    """Geometric illustration of the Banda Sea quake: stylised sea,
    Timor-Leste landmass, epicentre rings and wave arcs. No photos."""
    draw.rectangle([x0, y0, x1, y1], fill=SEA)
    # stylised Timor island (elongated landmass, lower half)
    land = [
        (x0 + 18, y1 - 78), (x0 + 70, y1 - 108), (x0 + 150, y1 - 96),
        (x0 + 235, y1 - 112), (x0 + 300, y1 - 88), (x0 + 318, y1 - 58),
        (x0 + 260, y1 - 40), (x0 + 170, y1 - 46), (x0 + 90, y1 - 38),
        (x0 + 30, y1 - 52),
    ]
    draw.polygon(land, fill=LAND, outline=(120, 100, 60))
    # small island dots north-east
    for cx, cy, r in ((x0 + 268, y0 + 62, 9), (x0 + 292, y0 + 88, 6),
                      (x0 + 240, y0 + 46, 5)):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=LAND)
    # wave arcs across the sea
    for i, yy in enumerate((y0 + 52, y0 + 84, y0 + 116)):
        draw.arc([x0 + 20 + i * 8, yy, x0 + 210 - i * 8, yy + 34],
                 start=200, end=340, fill=SEA_LIGHT, width=3)
    # epicentre: concentric rings in the sea, upper centre
    ex, ey = x0 + 165, y0 + 118
    for r, wdt in ((58, 3), (40, 3), (24, 4)):
        draw.ellipse([ex - r, ey - r, ex + r, ey + r],
                     outline=(255, 255, 255), width=wdt)
    draw.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=ACCENT)
    draw.text((ex + 66, ey - 16), "M6.8", font=SANS_B(30), fill=(255, 255, 255))
    # labels
    draw.text((x0 + 16, y0 + 12), "BANDA SEA", font=SANS_B(20),
              fill=(255, 255, 255))
    draw.text((x0 + 96, y1 - 30), "TIMOR-LESTE", font=SANS_B(16),
              fill=(60, 48, 20))


def story(draw, x, y, w, kick, head, body, head_size=25, body_size=17):
    kicker(draw, x, y, kick)
    y += 26
    y = headline(draw, x, y, head, SANS_B(head_size), w, head_size + 5)
    y += 4
    y = para(draw, x, y, body, SANS(body_size), w, body_size + 5)
    return y


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28                      # margin
    rx = W - mx                  # right edge

    # ---- Masthead ----
    d.text((W // 2, 18), "THE WORLD TODAY",
           font=fit_serif(d, "THE WORLD TODAY", 88, rx - mx),
           fill=INK, anchor="ma")
    rule(d, mx, 122, rx, 4)
    d.text((W // 2, 134), "SUNDAY 22 NOVEMBER 2026", font=SANS_B(36),
           fill=ACCENT, anchor="ma")
    d.text((W // 2, 178), "The day's world news in one page  •  Banda Sea  •  Mexico  •  Washington  •  Antalya",
           font=SANS(17), fill=MUTED, anchor="ma")
    rule(d, mx, 206, rx, 2)

    # ---- Lead story: Banda Sea quake ----
    lx, lw = mx, 600
    kicker(d, lx, 222, "LEAD STORY  —  BANDA SEA")
    y = 250
    y = headline(d, lx, y, "MAGNITUDE 6.8 QUAKE SHAKES BANDA SEA",
                 SANS_B(50), lw, 56)
    y += 8
    y = para(d, lx, y,
             "A magnitude 6.8 earthquake struck the Banda Sea off "
             "Timor-Leste on Sunday 22 November. Officials said there "
             "was no tsunami threat.",
             SANS(21), lw, 28)
    # lead illustration panel, right of the lead text
    px0, py0, px1, py1 = 656, 222, rx, 512
    draw_banda_panel(d, px0, py0, px1, py1)
    para(d, px0, py1 + 8, "The quake struck offshore; no tsunami threat was issued.",
         SANS(14), px1 - px0, 18, color=MUTED)
    rule(d, mx, 560, rx, 2)

    # ---- Row 2: three stories ----
    col_w = 304
    gap = 16
    xs = [mx, mx + col_w + gap, mx + 2 * (col_w + gap)]
    y2 = 578
    story(d, xs[0], y2, col_w, "MEXICO",
          "Cartel leader seized; 11 killed",
          "Security forces arrested a cartel leader in northern "
          "Mexico; 11 people were killed.")
    story(d, xs[1], y2, col_w, "WASHINGTON",
          "Trump seeks lasting nuclear deal with Iran",
          "Trump is pursuing a permanent nuclear deal with Iran.")
    story(d, xs[2], y2, col_w, "WASHINGTON",
          "Democrats retake Congress in midterm win",
          "Democrats won back Congress in the US midterm elections.")
    rule(d, mx, 748, rx, 2)

    # ---- Row 3: three stories ----
    y3 = 764
    story(d, xs[0], y3, col_w, "ANTALYA  •  COP31",
          "Climate summit at risk as talks overrun",
          "The COP31 climate summit risked failure as negotiations "
          "ran over with no deal yet.")
    story(d, xs[1], y3, col_w, "KYIV",
          "Zelenskyy sets out 20-point peace plan",
          "President Zelenskyy presented a 20-point peace plan for "
          "Ukraine.")
    story(d, xs[2], y3, col_w, "OSLO",
          "Norway court scraps contested oil licences",
          "Norway's Supreme Court cancelled contested oil licences.")
    rule(d, mx, 936, rx, 2)

    # ---- Bottom strip: also today ----
    d.text((mx, 948), "ALSO TODAY:", font=SANS_B(17), fill=ACCENT)
    para(d, mx + 128, 948,
         "US–China trade and tech tensions unresolved after APEC  •  "
         "NASA's Voyager, first human-made object a light-day from "
         "Earth  •  Bitcoin above $60,000  •  India 720/9, their highest "
         "Test score in New Zealand.",
         SANS(15), rx - (mx + 128), 19)

    # ---- Footer ----
    d.text((W // 2, 1002), "THE WORLD TODAY  •  SUNDAY 22 NOVEMBER 2026",
           font=SANS(13), fill=MUTED, anchor="ma")

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    img.save(out_path, format="PNG", optimize=True)
    print("wrote", out_path)


if __name__ == "__main__":
    main()
