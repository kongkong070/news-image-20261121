#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026.

One 1024x1024 PNG, Pillow only, fully deterministic: no timestamps, no
randomness, fixed font files and fixed draw order.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 232)
INK = (22, 21, 19)
RED = (179, 38, 30)
BLUE = (31, 78, 121)
GOLD = (201, 162, 39)
GREY = (90, 88, 84)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None, align="left", max_w=None):
    if leading is None:
        leading = int(fnt.size * 1.18)
    for line in lines:
        if align == "center":
            w = draw.textlength(line, font=fnt)
            draw.text((x + (max_w - w) / 2, y), line, font=fnt, fill=fill)
        else:
            draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def scene_lead(d, x0, y0, x1, y1):
    # Night sky over Poland: missile trail, explosion, houses, NATO jets.
    d.rectangle([x0, y0, x1, y1], fill=(18, 30, 55))
    for sx, sy in [(x0 + 30, y0 + 22), (x0 + 120, y0 + 14), (x0 + 260, y0 + 30),
                   (x0 + 380, y0 + 16), (x0 + 210, y0 + 48), (x0 + 60, y0 + 58)]:
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(220, 220, 200))
    # missile trail: bright arc from upper left to the blast
    bx, by = x1 - 90, y0 + 78
    for i in range(24):
        t = i / 23
        px = x0 + 40 + t * (bx - x0 - 40)
        py = y0 + 150 - t * t * 95
        r = 2 + int(3 * t)
        d.ellipse([px - r, py - r, px + r, py + r], fill=(255, 210, 120))
    d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=(255, 255, 255))
    # explosion burst
    cx, cy = x1 - 55, y0 + 95
    for r, col in [(46, (255, 120, 30)), (34, (255, 170, 60)), (22, (255, 220, 130))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    # two jets, top right
    for jx, jy in [(x1 - 190, y0 + 26), (x1 - 150, y0 + 44)]:
        d.polygon([(jx, jy), (jx + 34, jy + 6), (jx, jy + 12)], fill=(200, 200, 210))
        d.polygon([(jx + 8, jy + 2), (jx + 16, jy - 6), (jx + 20, jy + 4)], fill=(200, 200, 210))
    # ground and houses
    gy = y1 - 52
    d.rectangle([x0, gy, x1, y1], fill=(38, 52, 36))
    for hx in (x0 + 24, x0 + 110, x0 + 210, x0 + 300):
        d.rectangle([hx, gy - 26, hx + 56, gy], fill=(20, 20, 24))
        d.polygon([(hx - 4, gy - 26), (hx + 28, gy - 44), (hx + 60, gy - 26)], fill=(12, 12, 14))
        d.rectangle([hx + 20, gy - 16, hx + 30, gy - 6], fill=(255, 210, 90))
    # smoke column from the blast
    d.ellipse([cx - 26, cy + 30, cx + 6, cy + 78], fill=(120, 120, 120))
    d.ellipse([cx - 14, cy + 44, cx + 18, cy + 86], fill=(90, 90, 90))


def scene_trump(d, x0, y0, x1, y1):
    # US flag, podium and microphone.
    d.rectangle([x0, y0, x1, y1], fill=(214, 226, 238))
    fw, fh = x1 - x0 - 90, 84
    fx, fy = x0 + 14, y0 + 12
    for i in range(7):
        col = (178, 34, 34) if i % 2 == 0 else (245, 245, 245)
        d.rectangle([fx, fy + i * (fh // 7), fx + fw, fy + (i + 1) * (fh // 7)], fill=col)
    d.rectangle([fx, fy, fx + int(fw * 0.42), fy + 4 * (fh // 7)], fill=(30, 50, 110))
    for r in range(3):
        for c in range(5):
            d.ellipse([fx + 8 + c * 22, fy + 6 + r * 13,
                       fx + 12 + c * 22, fy + 10 + r * 13], fill=(255, 255, 255))
    # podium
    px0, px1 = x0 + 70, x1 - 60
    py0 = y1 - 46
    d.polygon([(px0, py0), (px1, py0), (px1 - 14, y1), (px0 + 14, y1)], fill=(96, 64, 40))
    d.rectangle([px0 - 8, py0 - 8, px1 + 8, py0], fill=(70, 46, 28))
    # microphone
    d.line([x0 + 150, py0 - 8, x0 + 150, py0 - 34], fill=(40, 40, 40), width=3)
    d.ellipse([x0 + 142, py0 - 44, x0 + 158, py0 - 30], fill=(40, 40, 40))
    # small gold seal disc on the podium
    cx = (px0 + px1) // 2
    d.ellipse([cx - 12, py0 + 12, cx + 12, py0 + 36], fill=(201, 162, 39))
    d.ellipse([cx - 6, py0 + 18, cx + 6, py0 + 30], fill=(96, 64, 40))


def scene_denmark(d, x0, y0, x1, y1):
    # Ministry building, Danish flag, suitcase.
    d.rectangle([x0, y0, x1, y1], fill=(232, 228, 218))
    d.rectangle([x0 + 18, y0 + 42, x1 - 70, y1 - 6], fill=(150, 148, 140))
    d.polygon([(x0 + 12, y0 + 42), ((x0 + x1) // 2 - 20, y0 + 18),
               (x1 - 64, y0 + 42)], fill=(110, 108, 100))
    for cx in (x0 + 44, x0 + 84, x0 + 124, x0 + 164):
        d.rectangle([cx, y0 + 58, cx + 16, y1 - 6], fill=(60, 60, 64))
    # Danish flag on a pole
    d.rectangle([x1 - 52, y0 + 8, x1 - 48, y1 - 6], fill=(80, 80, 80))
    d.rectangle([x1 - 48, y0 + 10, x1 - 6, y0 + 36], fill=(200, 16, 46))
    d.rectangle([x1 - 48, y0 + 20, x1 - 6, y0 + 26], fill=(255, 255, 255))
    d.rectangle([x1 - 34, y0 + 10, x1 - 28, y0 + 36], fill=(255, 255, 255))
    # suitcase, bottom right
    sx0, sy0 = x1 - 66, y1 - 34
    d.rectangle([sx0, sy0, sx0 + 52, sy0 + 26], fill=(120, 72, 32))
    d.rectangle([sx0 + 20, sy0 - 8, sx0 + 32, sy0], fill=(90, 54, 24))
    d.line([sx0 + 26, sy0, sx0 + 26, sy0 + 26], fill=(90, 54, 24), width=3)


def scene_rikers(d, x0, y0, x1, y1):
    # Island jail in the East River, with a bridge to the mainland.
    d.rectangle([x0, y0, x1, y1], fill=(178, 208, 224))
    d.ellipse([x0 + 8, y0 + 40, x1 - 8, y1 - 4], fill=(120, 122, 110))
    # jail block with bars
    bx0, bx1 = x0 + 34, x1 - 40
    by0, by1 = y0 + 18, y0 + 62
    d.rectangle([bx0, by0, bx1, by1], fill=(70, 72, 76))
    d.rectangle([bx0, by0, bx1, by0 + 7], fill=(50, 52, 56))
    for wx in range(bx0 + 12, bx1 - 8, 18):
        d.rectangle([wx, by0 + 12, wx + 8, by1 - 5], fill=(255, 220, 120))
        d.line([wx + 4, by0 + 12, wx + 4, by1 - 5], fill=(40, 40, 40), width=2)
    # bridge to the right edge
    d.line([x1 - 40, y0 + 52, x1, y0 + 46], fill=(60, 60, 60), width=5)
    d.line([x1 - 40, y0 + 52, x1 - 40, y0 + 34], fill=(60, 60, 60), width=4)
    # small boat on the water
    d.polygon([(x0 + 22, y1 - 12), (x0 + 52, y1 - 12), (x0 + 44, y1 - 4),
               (x0 + 30, y1 - 4)], fill=(90, 60, 40))


def scene_anc(d, x0, y0, x1, y1):
    # South African flag (red top, blue bottom, green Y, black hoist
    # triangle) with a ballot box standing in front of it.
    mid = (y0 + y1) // 2
    d.rectangle([x0, y0, x1, mid], fill=(222, 41, 16))
    d.rectangle([x0, mid, x1, y1], fill=(0, 35, 102))
    d.polygon([(x0, y0), (x0, y1), (x0 + 96, mid)], fill=(0, 0, 0))
    # green Y drawn as thick lines, white-fimbriated
    ym = x0 + 150
    for wdt, col in [(18, (255, 255, 255)), (10, (0, 122, 61))]:
        d.line([x0, y0, ym, mid], fill=col, width=wdt)
        d.line([x0, y1, ym, mid], fill=col, width=wdt)
        d.line([ym, mid, x1, mid], fill=col, width=wdt)
    # ballot box, right of centre, VOTE printed inside it
    bx0, bx1 = x0 + 250, x0 + 386
    by0, by1 = y0 + 22, y1 - 12
    d.rectangle([bx0, by0 + 14, bx1, by1], fill=(245, 245, 245))
    d.polygon([(bx0 - 8, by0 + 14), (bx1 + 8, by0 + 14), (bx1, by0), (bx0, by0)],
              fill=(220, 220, 220))
    d.rectangle([bx0 + 46, by0 + 4, bx1 - 46, by0 + 10], fill=(40, 40, 40))
    d.rectangle([bx0 + 54, by0 - 12, bx1 - 54, by0 + 4], fill=(255, 255, 255))
    d.text((bx0 + 38, by0 + 24), "VOTE", font=font(SANSB, 22), fill=(179, 38, 30))


def scene_kane(d, x0, y0, x1, y1):
    # Football pitch, goal, ball and a seated player holding his ankle,
    # with a red-cross medical badge in the corner.
    d.rectangle([x0, y0, x1, y1], fill=(46, 139, 68))
    d.rectangle([x0, y0, x1, y1], outline=(255, 255, 255), width=2)
    d.ellipse([x0 + 150, y0 + 12, x1 - 150, y1 - 12], outline=(255, 255, 255), width=3)
    d.line([x0 + (x1 - x0) // 2, y0, x0 + (x1 - x0) // 2, y1],
           fill=(255, 255, 255), width=3)
    # goal, right side
    d.rectangle([x1 - 66, y0 + 26, x1 - 10, y1 - 26], outline=(255, 255, 255), width=4)
    for gx in range(x1 - 62, x1 - 12, 10):
        d.line([gx, y0 + 28, gx, y1 - 28], fill=(220, 220, 220), width=1)
    # ball
    bx, by = x1 - 130, y0 + 44
    d.ellipse([bx - 14, by - 14, bx + 14, by + 14], fill=(255, 255, 255),
              outline=(20, 20, 20), width=2)
    d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(20, 20, 20))
    # seated player, left side: head, red torso leaning back, legs out
    px, py = x0 + 58, y0 + 32
    d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=(240, 200, 160))
    d.polygon([(px + 2, py + 8), (px + 30, py + 28), (px + 20, py + 38),
               (px - 8, py + 18)], fill=(178, 34, 34))
    d.polygon([(px + 24, py + 34), (px + 78, py + 42), (px + 76, py + 50),
               (px + 22, py + 42)], fill=(255, 255, 255))
    d.ellipse([px + 74, py + 36, px + 86, py + 48], fill=(20, 20, 20))
    # red-cross medical badge, top-left corner
    cx, cy = x0 + 22, y0 + 22
    d.rectangle([cx - 13, cy - 13, cx + 13, cy + 13], fill=(255, 255, 255))
    d.rectangle([cx - 4, cy - 10, cx + 4, cy + 10], fill=(200, 20, 20))
    d.rectangle([cx - 10, cy - 4, cx + 10, cy + 4], fill=(200, 20, 20))


def story_cell(d, x0, y0, x1, y1, kicker, headline, deck, scene):
    d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255), outline=(150, 148, 140), width=2)
    pad = 12
    y = y0 + 10
    d.text((x0 + pad, y), kicker, font=font(SANSB, 15), fill=RED)
    y += 22
    sy0 = y
    sy1 = y + 84
    d.rectangle([x0 + pad, sy0, x1 - pad, sy1], outline=(150, 148, 140), width=1)
    scene(d, x0 + pad, sy0, x1 - pad, sy1)
    y = sy1 + 8
    hf = font(SANSB, 21)
    lines = wrap(d, headline, hf, x1 - x0 - 2 * pad)
    y = text_block(d, x0 + pad, y, lines, hf, leading=25)
    y += 2
    df = font(SANS, 15)
    dlines = wrap(d, deck, df, x1 - x0 - 2 * pad)
    text_block(d, x0 + pad, y, dlines, df, fill=(60, 58, 54), leading=19)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 28
    # masthead
    title = "THE WORLD TODAY"
    tf = font(SERIF, 58)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 22), title, font=tf, fill=INK)
    d.rectangle([m, 100, W - m, 102], fill=INK)
    date = "SATURDAY  21  NOVEMBER  2026"
    df = font(SANSB, 30)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 110), date, font=df, fill=RED)
    d.rectangle([m, 148, W - m, 150], fill=INK)
    # lead story
    lx0, ly0, lx1, ly1 = m, 162, W - m, 484
    d.rectangle([lx0, ly0, lx1, ly1], fill=(255, 255, 255), outline=INK, width=3)
    d.text((lx0 + 16, ly0 + 10), "WAR IN EUROPE  —  LEAD", font=font(SANSB, 16), fill=RED)
    hf = font(SANSB, 40)
    head = "RUSSIAN MISSILES LAND IN POLAND"
    hw = d.textlength(head, font=hf)
    d.text((lx0 + 16, ly0 + 34), head, font=hf, fill=INK)
    scene_lead(d, lx0 + 16, ly0 + 96, lx0 + 470, ly1 - 14)
    dx = lx0 + 492
    dw2 = lx1 - 16 - dx
    deckf = font(SANS, 20)
    deck = ("Tusk calls the strike a deliberate provocation as NATO jets "
            "scramble. It came hours after Russia's huge attack on Kyiv — "
            "and days after the Shenzhen peace declaration.")
    lines = wrap(d, deck, deckf, dw2)
    text_block(d, dx, ly0 + 110, lines, deckf, leading=27)
    d.text((dx, ly1 - 44), "No one was hurt in the blast.",
           font=font(SANSB, 18), fill=BLUE)
    # grid: row A three cells, row B two cells
    gap = 12
    cw3 = (W - 2 * m - 2 * gap) // 3
    row_a_y0, row_a_y1 = 498, 748
    stories_a = [
        ("WASHINGTON", "Trump hails 'very good' Putin talks",
         "Home from Shenzhen, he also threatens a 'tremendous tax' on US firms building AI data centres abroad.",
         scene_trump),
        ("COPENHAGEN", "Denmark expels envoy in rapper 'murder plot'",
         "Police say two men were held over a plan to kill Ukrainian rapper Kyivstoner.",
         scene_denmark),
        ("NEW YORK", "Mamdani: Rikers Island jail to close by 2032",
         "The mayor's plan replaces the jail with four borough jails and cuts inmate numbers.",
         scene_rikers),
    ]
    for i, (kick, head, deck, scene) in enumerate(stories_a):
        x0 = m + i * (cw3 + gap)
        story_cell(d, x0, row_a_y0, x0 + cw3, row_a_y1, kick, head, deck, scene)
    cw2 = (W - 2 * m - gap) // 2
    row_b_y0, row_b_y1 = 760, 992
    stories_b = [
        ("SOUTH AFRICA", "ANC scrambles for coalition deals after election setback",
         "The ruling party won just 31% and lost most big cities; talks must end by 27 November.",
         scene_anc),
        ("SPORT", "Kane out for months with ankle ligament tear",
         "England's captain was hurt in Bayern's draw with Cologne and will miss the rest of 2026.",
         scene_kane),
    ]
    for i, (kick, head, deck, scene) in enumerate(stories_b):
        x0 = m + i * (cw2 + gap)
        story_cell(d, x0, row_b_y0, x0 + cw2, row_b_y1, kick, head, deck, scene)
    # footer
    ff = font(SANS, 14)
    foot = "Stories first reported 20–21 November 2026  ·  Sources: BBC, Reuters, AP, CNN"
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 1002), foot, font=ff, fill=GREY)
    img.save("entry.png", "PNG", optimize=True)


if __name__ == "__main__":
    main()
