# render.py — fresh render for news-image-20261120 V1 (v2: fixed geometry)
# "THE DAY, WITH CONSEQUENCES" — 1024x1024 cream-paper front page, 36 stories.
# Drawn with PIL only. Run: python3 render.py  -> writes entry.png beside this file.
import hashlib
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (246, 241, 227)
PAPER2 = (238, 231, 211)
INK = (18, 16, 12)
INK2 = (58, 54, 46)
RED = (178, 34, 28)
GOLD = (176, 132, 16)
GOLD_BG = (201, 162, 39)
GREY = (150, 144, 128)

F = "/usr/share/fonts/truetype"
SERIF = f"{F}/liberation/LiberationSerif-Regular.ttf"
SERIF_B = f"{F}/liberation/LiberationSerif-Bold.ttf"
SERIF_I = f"{F}/liberation/LiberationSerif-Italic.ttf"
SERIF_BI = f"{F}/liberation/LiberationSerif-BoldItalic.ttf"
SANS = f"{F}/dejavu/DejaVuSans.ttf"
SANS_B = f"{F}/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_lines(d, x, y, lines, fnt, fill=INK, lh=None, align="left", max_w=None):
    if lh is None:
        lh = int(fnt.size * 1.18)
    for ln in lines:
        xx = x
        if align == "center" and max_w is not None:
            xx = x + (max_w - d.textlength(ln, font=fnt)) / 2
        d.text((xx, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def hrule(d, x0, x1, y, fill=INK, w=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


def fit_font(d, text, path, size, max_w):
    while size > 8 and d.textlength(text, font=font(path, size)) > max_w:
        size -= 0.5
    return font(path, size)


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
MX = 24
CW = W - 2 * MX

# ---------------------------------------------------------------- masthead
hrule(d, MX, W - MX, 8, w=3)
hrule(d, MX, W - MX, 12, w=1)
d.text((W / 2, 14), "THE WORLD TODAY", font=font(SERIF_B, 46), fill=INK, anchor="ma")
d.text((W / 2, 62), "FRIDAY, 20 NOVEMBER 2026  ·  36 STORIES, ONE FRIDAY  ·  WORLD EDITION",
       font=font(SANS_B, 11), fill=INK2, anchor="ma")
hrule(d, MX, W - MX, 84, w=1)
d.text((W / 2, 88), "THE DAY, WITH CONSEQUENCES", font=font(SERIF_B, 38), fill=INK, anchor="ma")
hrule(d, MX, W - MX, 130, w=2)

# ---------------------------------------------------------------- number strip (6 cells)
NUMBERS = [
    ("~30", "BALLISTIC MISSILES\nFIRED AT KYIV"),
    ("3", "KILLED IN KYIV"),
    ("300,000+", "EVACUATED FROM\nAKVAN'S PATH"),
    ("423", "RESCUE TEAMS\nDEPLOYED"),
    ("$120bn", "COP31 FINANCE\nUNRESOLVED"),
    ("46", "SHIPS WAITING\nAT HORMUZ"),
]
ny0, ny1 = 136, 184
cell_w = CW / 6
for i, (num, lab) in enumerate(NUMBERS):
    x0 = MX + i * cell_w
    if i:
        d.line([(x0, ny0 + 4), (x0, ny1 - 4)], fill=GREY, width=1)
    d.text((x0 + cell_w / 2, ny0 + 2), num, font=font(SERIF_B, 24), fill=GOLD, anchor="ma")
    text_lines(d, x0, ny0 + 28, lab.split("\n"), font(SANS_B, 9), fill=INK, lh=11, align="center", max_w=cell_w)
hrule(d, MX, W - MX, 186, w=1)

# ---------------------------------------------------------------- region strip
d.text((W / 2, 192), "Europe 9   ·   Asia 9   ·   Middle East 3   ·   Americas 7   ·   Africa 2   ·   Oceania 5   ·   Space 1",
       font=font(SANS_B, 12), fill=INK, anchor="ma")
hrule(d, MX, W - MX, 210, w=1)

# ---------------------------------------------------------------- three lead cards
LEADS = [
    dict(n=1, kick="KYIV, UKRAINE  |  WAR",
         head="KYIV HIT BY SEVEN WAVES OF MISSILES",
         body="Russia fired ~30 ballistic missiles at Kyiv from 01:25 local. Three water workers were killed; bridges, energy and transport sites were hit, with fires in three districts. Embassies were damaged; power and water were cut.",
         so="Damage to energy, transport and water infrastructure compounds the disruption for Kyiv residents.",
         src="Kyiv Post · Reuters · Kyiv Independent"),
    dict(n=2, kick="ODISHA, INDIA  |  CYCLONE",
         head="AKVAN MAKES LANDFALL IN ODISHA",
         body="Cyclone Akvan came ashore near Gopalpur at about 8am local / 02:00 UTC. Winds reached 70–100 km/h, gusting 110; 300,000+ people were evacuated and 423 rescue teams deployed. Schools shut, trains cancelled; no deaths by midday.",
         so="With mass evacuations underway, the immediate priority is protecting people as the cyclone crosses the coast.",
         src="IMD · PTI · The Hindu"),
    dict(n=3, kick="ANTALYA, TURKIYE  |  CLIMATE",
         head="COP31 ENTERS ITS FINAL DAY DEADLOCKED",
         body="The closing draft omits fossil fuels; $120bn in adaptation finance remains unresolved. Hosts push a “35 by 35” clean-power goal as talks approach their final day. Negotiations may run into the weekend.",
         so="Without agreement on fossil fuels and finance, the summit’s closing text remains contested.",
         src="UN News · Reuters · AFP"),
]
LX0, LX1 = 216, 436
col_w = (CW - 24) / 3
for i, L in enumerate(LEADS):
    x0 = MX + i * (col_w + 12)
    x1 = x0 + col_w
    iy0, iy1 = LX0, LX0 + 64
    d.rectangle([x0, iy0, x1, iy1], fill=PAPER2, outline=INK, width=1)
    if L["n"] == 1:
        d.rectangle([x0, iy1 - 26, x1, iy1], fill=(38, 34, 30))
        rnd = random.Random(7)
        bx = x0 + 6
        while bx < x1 - 10:
            bw = rnd.randint(12, 26)
            bh = rnd.randint(12, 24)
            d.rectangle([bx, iy1 - bh, bx + bw, iy1], fill=(18, 16, 12))
            for wy in range(iy1 - bh + 4, iy1 - 4, 6):
                d.rectangle([bx + 3, wy, bx + 5, wy + 2], fill=GOLD_BG)
            bx += bw + 3
        for tx in (x0 + 30, x0 + 120, x0 + 220):
            d.arc([tx - 40, iy0 + 2, tx + 40, iy0 + 46], 200, 340, fill=RED, width=2)
            d.ellipse([tx + 26, iy0 + 10, tx + 32, iy0 + 16], fill=GOLD_BG)
        d.arc([x0 + 60, iy1 - 18, x1 - 60, iy1 + 12], 180, 360, fill=INK, width=2)
        for fx in (x0 + 90, x0 + 200):
            d.polygon([(fx, iy1 - 10), (fx + 5, iy1 - 2), (fx + 10, iy1 - 10)], fill=RED)
    elif L["n"] == 2:
        cx, cy = x0 + col_w * 0.42, iy0 + 34
        for r, col in ((26, INK), (20, RED), (14, INK), (8, GOLD_BG)):
            d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=col, width=3)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
        d.polygon([(x0 + col_w * 0.78, iy0 + 4), (x1, iy0 + 4), (x1, iy1), (x0 + col_w * 0.72, iy1)], fill=(214, 205, 180))
        d.line([(x0 + col_w * 0.72, iy0 + 4), (x0 + col_w * 0.78, iy1 - 4)], fill=GOLD_BG, width=3)
        d.line([(x0 + 12, iy1 - 12), (x0 + 52, iy1 - 12)], fill=INK, width=2)
        d.polygon([(x0 + 52, iy1 - 17), (x0 + 52, iy1 - 7), (x0 + 60, iy1 - 12)], fill=INK)
        sx, sy = x0 + col_w - 34, iy1 - 22
        d.polygon([(sx, sy), (sx + 22, sy), (sx + 11, sy - 10)], fill=RED)
        d.rectangle([sx + 3, sy, sx + 19, sy + 9], outline=INK, width=2)
    else:
        gx, gy = x0 + col_w / 2, iy0 + 24
        d.ellipse([gx - 20, gy - 20, gx + 20, gy + 20], outline=INK, width=2, fill=(214, 205, 180))
        d.pieslice([gx - 20, gy - 20, gx + 20, gy + 20], 270, 90, fill=RED)
        d.line([(gx, gy - 20), (gx, gy + 20)], fill=INK, width=2)
        d.arc([gx - 20, gy - 20, gx + 20, gy + 20], 0, 360, fill=INK, width=2)
        d.polygon([(x0 + 14, iy1 - 20), (x0 + col_w / 2, iy1 - 34), (x1 - 14, iy1 - 20)], outline=INK, width=2)
        d.line([(x0 + 14, iy1 - 20), (x1 - 14, iy1 - 20)], fill=INK, width=2)
        for dx in (x0 + 52, x1 - 66):
            d.ellipse([dx, iy1 - 16, dx + 14, iy1 - 4], fill=INK)
            d.pieslice([dx - 2, iy1 - 6, dx + 16, iy1 + 2], 180, 360, fill=INK)
        d.rectangle([x0 + col_w / 2 - 14, iy1 - 18, x0 + col_w / 2 + 14, iy1 - 2], fill=(255, 255, 255), outline=RED, width=2)
        for ly in (iy1 - 14, iy1 - 10, iy1 - 6):
            d.line([(x0 + col_w / 2 - 10, ly), (x0 + col_w / 2 + 10, ly)], fill=INK2, width=1)
    yy = iy1 + 5
    d.text((x0, yy), f"{L['n']} — {L['kick']}", font=font(SANS_B, 10), fill=RED)
    yy += 14
    hl = wrap(d, L["head"], font(SERIF_B, 16), col_w)
    yy = text_lines(d, x0, yy, hl, font(SERIF_B, 16), lh=18)
    yy += 2
    bl = wrap(d, L["body"], font(SERIF, 10.5), col_w)
    yy = text_lines(d, x0, yy, bl, font(SERIF, 10.5), lh=12.5)
    yy += 2
    sl = wrap(d, "SO WHAT: " + L["so"], font(SERIF_BI, 10.5), col_w)
    yy = text_lines(d, x0, yy, sl, font(SERIF_BI, 10.5), lh=12.5, fill=RED)
    yy += 2
    d.text((x0, yy), L["src"], font=font(SANS, 8.5), fill=INK2)
    print(f"lead {L['n']}: head {len(hl)} lines, body {len(bl)} lines, so {len(sl)} lines, ends y={yy}")
    if i < 2:
        d.line([(x1 + 6, LX0), (x1 + 6, LX1)], fill=GREY, width=1)
hrule(d, MX, W - MX, 440, w=1)

# ---------------------------------------------------------------- THE DAY BY HOURS (2 lines)
hy0 = 446
d.text((MX, hy0), "THE DAY BY HOURS", font=font(SANS_B, 11), fill=RED)
hours = [
    ("00:49 UTC", "New Caledonia quake"),
    ("01:25", "Kyiv barrage"),
    ("02:00 UTC", "Akvan landfall"),
    ("morning", "Asia markets plunge"),
    ("midday", "COP31 final day"),
    ("P.M.", "Brussels reset summit"),
    ("evening", "Las Vegas practice"),
]
hx = MX + 150
line = 0
for t, what in hours:
    seg_w = (d.textlength(t, font=font(SANS_B, 10.5)) + 4
             + d.textlength(what, font=font(SERIF, 10.5)) + 16)
    if hx + seg_w > W - MX and line == 0:
        line = 1
        hx = MX + 150
    yy = hy0 + line * 14
    d.text((hx, yy), t, font=font(SANS_B, 10.5), fill=GOLD)
    w_t = d.textlength(t, font=font(SANS_B, 10.5))
    d.text((hx + w_t + 4, yy), what, font=font(SERIF, 10.5), fill=INK)
    hx += seg_w
hrule(d, MX, W - MX, 476, w=1)

# ---------------------------------------------------------------- ten tiles, 2 columns x 5 rows
TILES = [
    (4, "TAIPEI / SEOUL / TOKYO", "ASIA’S AI SELL-OFF DEEPENS",
     "Taiex fell 6.22%, down 2,393.60 pts to 36,033.29; 150 stocks limit-down. Worst week since 1991 (–17%); KOSPI –5.4%, Nikkei –4.9%. Curbs launched 20 Nov.",
     "The sell-off spreads across the region’s equity markets."),
    (5, "TOKYO", "JAPAN INFLATION EDGES UP",
     "October core inflation reached 2.2%; headline was 2.3%. Core stayed above 2% for a second month.",
     "A December BoJ hike is now eyed."),
    (6, "BEIJING", "CHINA HOLDS LENDING RATES",
     "The 1-year LPR stayed at 3.0% and the 5-year at 3.5%, as expected — the 18th month without a change.",
     "Borrowing benchmarks remain unchanged."),
    (7, "BRUSSELS", "FIRST EU–UK RESET SUMMIT OPENS",
     "Costa and von der Leyen host UK PM Burnham. A food deal, a carbon-market link and 100,000 youth places are on the table.",
     "The reset now depends on turning proposals into agreements."),
    (8, "S. SAUDI ARABIA", "SAUDI DEFENCES INTERCEPT MISSILE, DRONES",
     "Air defences intercepted a Houthi missile and drones over the south; alerts sounded in Jazan, Abha and Khamis Mushait. Saudi airstrikes hit Sanaa Friday.",
     "The cross-border threat remains active despite the alerts ending."),
    (9, "HORMUZ", "STRAIT SHUT, OIL NEAR $92.50",
     "The Strait of Hormuz stayed shut, with Brent crude near $92.50. Forty-six ships were waiting; Gulf war-risk cover was up 200x.",
     "Shipping delays and sharply higher war-risk cover weigh on Gulf trade."),
    (10, "SAN SALVADOR", "BUKELE FILES FOR THIRD TERM",
     "Bukele filed to run for a third term at Thursday night’s deadline, 20 Nov UTC. Supporters cheered; rights groups objected. Vote 28 Feb 2027.",
     "The filing puts the next presidential contest in motion."),
    (11, "SENEGAL / CANARY IS.", "BOAT CAPSIZES OFF SENEGAL",
     "Four people died and dozens were missing after a boat carrying 50–100 people capsized. Canary Islands arrivals reached 24,364 this year.",
     "The disaster adds urgency to the risks of the Atlantic crossing."),
    (12, "ROME", "ITALY’S CGIL HOLDS 24-HOUR STRIKE",
     "Unions rallied in ~100 squares against the 2027 budget; transit was hit.",
     "The budget dispute spills into transport and public life."),
    (13, "MERCURY", "BEPICOLOMBO REACHES MERCURY",
     "The spacecraft reached Mercury after an 8-year, 6bn-mile trip. Orbit insertion is set for Saturday.",
     "Arrival sets up Saturday’s planned orbit insertion."),
]
ty0 = 482
row_h = 50
tile_w = (CW - 12) / 2
for r in range(5):
    for c in range(2):
        n, city, head, body, cons = TILES[r * 2 + c]
        x0 = MX + c * (tile_w + 12)
        yy = ty0 + r * row_h
        d.text((x0, yy), str(n), font=font(SERIF_B, 14), fill=GOLD)
        hl_text = f"{city} — {head}"
        hf = fit_font(d, hl_text, SERIF_B, 12, tile_w - 20)
        d.text((x0 + 20, yy + 1), hl_text, font=hf, fill=INK)
        yy += 14
        bl = wrap(d, body, font(SERIF, 10), tile_w - 20)
        yy = text_lines(d, x0 + 20, yy, bl[:2], font(SERIF, 10), lh=11)
        cl = wrap(d, "→ " + cons, font(SANS, 10), tile_w - 20)
        text_lines(d, x0 + 20, yy, cl[:1], font(SANS, 10), lh=11, fill=RED)
        print(f"tile {n}: body {len(bl)} lines (showing {min(2, len(bl))}), cons {len(cl)} lines, head size {hf.size}")
    hrule(d, MX, W - MX, ty0 + (r + 1) * row_h - 1, fill=GREY, w=1)
ty1 = ty0 + 5 * row_h

# ---------------------------------------------------------------- map + ALSO zone
zy0 = ty1 + 6
d.text((MX, zy0), "WHERE IT HAPPENED", font=font(SANS_B, 11), fill=INK)
d.text((MX + 470, zy0), "ALSO — STORIES 14–36", font=font(SANS_B, 11), fill=INK)
zy0 += 16
map_x0, map_y0, map_w, map_h = MX, zy0, 440, 160
d.rectangle([map_x0, map_y0, map_x0 + map_w, map_y0 + map_h], outline=INK, width=1, fill=(240, 234, 216))

CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80), (-85, 70), (-75, 62), (-60, 55), (-55, 47), (-65, 44), (-75, 39), (-80, 32), (-85, 30), (-90, 21), (-95, 19), (-105, 22), (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)],
    "SA": [(-80, 10), (-75, 5), (-60, 5), (-50, 0), (-40, -5), (-35, -10), (-40, -20), (-48, -28), (-55, -35), (-65, -45), (-70, -55), (-73, -40), (-72, -25), (-77, -12), (-80, -5)],
    "EU": [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59), (18, 56), (21, 55), (24, 59), (30, 60), (28, 65), (25, 71), (18, 70), (12, 66), (5, 60), (5, 58), (-5, 50), (-10, 43)],
    "AF": [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (40, 15), (43, 11), (51, 11), (48, 0), (40, -10), (35, -20), (32, -29), (25, -34), (18, -35), (12, -18), (9, -1), (9, 4), (-8, 5), (-15, 11), (-17, 15), (-16, 20), (-10, 30)],
    "AS": [(30, 36), (35, 36), (40, 35), (48, 30), (55, 25), (58, 25), (62, 25), (66, 25), (70, 22), (75, 20), (80, 15), (85, 20), (90, 22), (95, 16), (100, 10), (105, 8), (108, 12), (110, 20), (115, 23), (120, 28), (122, 32), (127, 35), (130, 38), (135, 42), (140, 45), (142, 50), (142, 55), (158, 60), (162, 65), (170, 66), (178, 65), (170, 70), (160, 70), (150, 72), (140, 72), (130, 72), (120, 73), (110, 74), (100, 76), (90, 75), (80, 73), (70, 72), (60, 69), (50, 68), (45, 66), (40, 64), (35, 62), (32, 60), (30, 58), (28, 55), (30, 50), (35, 45), (40, 42), (35, 40)],
    "OC": [(113, -22), (114, -30), (115, -35), (120, -34), (130, -32), (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11), (136, -12), (132, -12), (126, -14), (122, -17), (118, -20)],
}


def proj(lon, lat):
    x = map_x0 + 6 + (lon + 170) / 360 * (map_w - 12)
    y = map_y0 + 6 + (75 - lat) / 130 * (map_h - 12)
    return (x, y)


for pts in CONTINENTS.values():
    d.polygon([proj(lo, la) for lo, la in pts], fill=(216, 207, 182), outline=INK2)
for lon in (-120, -60, 0, 60, 120):
    x, _ = proj(lon, 0)
    d.line([(x, map_y0 + 6), (x, map_y0 + map_h - 6)], fill=(225, 218, 196), width=1)

PINS = {1: (31, 50), 2: (85, 20), 3: (30, 37), 4: (127, 35), 5: (139, 35), 6: (116, 40),
        7: (4, 51), 8: (43, 17), 9: (56, 26), 10: (-89, 14), 11: (-17, 15), 12: (12, 42)}
GREY_DOTS = [(174, -41), (165, -22), (-115, 36), (-160, -21), (151, -34), (127, 37), (-48, -16),
             (36, 50), (33, 48), (35, 48), (7, 45), (114, 22), (35, 32), (-17, 15), (-72, 19),
             (-99, 19), (-47, -24), (-79, 44), (116, 40)]
for lo, la in GREY_DOTS:
    x, y = proj(lo, la)
    d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=GREY)
for n, (lo, la) in PINS.items():
    x, y = proj(lo, la)
    d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=GOLD_BG, outline=INK, width=1)
    d.text((x, y - 5), str(n), font=font(SANS_B, 8), fill=INK, anchor="ma")
ix, iy = map_x0 + map_w - 52, map_y0 + 8
d.ellipse([ix, iy, ix + 26, iy + 26], fill=(190, 184, 170), outline=INK, width=1)
d.ellipse([ix + 7, iy + 8, ix + 11, iy + 12], fill=(150, 144, 128))
d.ellipse([ix + 15, iy + 15, ix + 19, iy + 19], fill=(150, 144, 128))
d.text((ix + 13, iy + 28), "13 MERCURY", font=font(SANS_B, 8), fill=INK, anchor="ma")
d.text((MX, map_y0 + map_h + 4), "36 stories, one Friday — from Kyiv and Odisha to Mercury.",
       font=font(SERIF_I, 11), fill=INK)

ALSO = [
    (14, "WELLINGTON", "Phillips 118 vs India; NZ 368, India 159–1 at stumps"),
    (15, "NEW CALEDONIA", "M5.6 quake SE of Loyalty Islands, 00:49 UTC; no tsunami"),
    (16, "LAS VEGAS", "Russell fastest in wet GP practice, 1:47.272; rain hit session one"),
    (17, "COOK ISLANDS", "Cyclone Xavier nears; emergency for Nassau; cat 2–3 weekend"),
    (18, "SYDNEY", "Man charged with terror offences; police: no public threat"),
    (19, "SEOUL", "Ruling party moves to impeach Chief Justice Cho Hee-dae"),
    (20, "BRASILIA", "Lula meets Chief Raoni as Brazil recognises Indigenous land"),
    (21, "KHARKIV", "Drone hits a hospital; at least four hurt"),
    (22, "KRYVYI RIH", "Drone attack cuts power to hospitals and heating"),
    (23, "DNIPRO", "Five injured in drone attack"),
    (24, "TURIN", "ATP Finals group stage ends; semi-finals Saturday"),
    (25, "ANTALYA", "France calls fossil-fuel gap a “black mark”"),
    (26, "SEOUL", "Appeal court upholds Kakao founder Kim’s acquittal"),
    (27, "HONG KONG", "Hang Seng about 20% off January peak"),
    (28, "SYDNEY", "Retailer General Pants enters administration"),
    (29, "ODISHA", "Patrapur records 209 mm of rain as Akvan crosses"),
    (30, "BEIT SHEMESH", "Haredi protesters clash with Israeli police"),
    (31, "DAKAR", "Four bodies found after migrant boat capsized"),
    (32, "PORT-AU-PRINCE", "Police say raid killed 34 gang suspects"),
    (33, "MEXICO CITY", "Nation marks 116th Revolution Day"),
    (34, "SAO PAULO", "Markets shut for Black Consciousness Day"),
    (35, "TORONTO", "Alcaraz-Cobolli, Medvedev-Tiafoe close ATP groups"),
    (36, "BEIJING", "State media: Xi for three-way talks"),
]
ax0 = MX + 470
acol_w = (W - MX - ax0 - 8) / 3
cols = [ALSO[0:8], ALSO[8:16], ALSO[16:23]]
for ci, col in enumerate(cols):
    cx = ax0 + ci * (acol_w + 4)
    yy = zy0
    for n, city, txt in col:
        lines = wrap(d, f"{n} {city} — {txt}", font(SERIF, 8.5), acol_w)
        for li, ln in enumerate(lines):
            if li == 0:
                wnum = d.textlength(f"{n} ", font=font(SERIF_B, 8.5))
                d.text((cx, yy), f"{n} ", font=font(SERIF_B, 8.5), fill=GOLD)
                d.text((cx + wnum, yy), ln[len(str(n)) + 1:], font=font(SERIF, 8.5), fill=INK)
            else:
                d.text((cx, yy), ln, font=font(SERIF, 8.5), fill=INK)
            yy += 10
        yy += 1.5
    print(f"ALSO col {ci}: ends y={yy:.1f}")
zy1 = map_y0 + map_h + 20

# ---------------------------------------------------------------- DATE CHECK red box
dy0 = zy1 + 4
d.rectangle([MX, dy0, W - MX, dy0 + 62], outline=RED, width=2)
d.text((MX + 8, dy0 + 5), "DATE CHECK — 19 NOVEMBER, NOT TODAY’S STORY LIST:",
       font=font(SANS_B, 10.5), fill=RED)
dc = ("Shenzhen trilateral summit + peace declaration · ICJ Myanmar genocide ruling 9–6 · Anthropic IPO debut: opened $111.50 (+34% vs $83), "
      "briefly ~$2.01tn fully-diluted, closed $97.17 (+17%), ~$1.75tn · UK £260m drone package for Ukraine, 1,000+ long-range drones · US sanctions on "
      "Comancheros and ‘Ndrangheta, incl. Toronto faction and Vescio network · US Senate rejects Iran war-powers resolution 51–48 · Houthi missile strike "
      "on Riyadh’s PIF Tower · Tanker mine incidents in the Strait of Hormuz · Georgia gas explosion, Ponichala, Tbilisi — 6 dead · UK + Norway £100m+ for "
      "two Ukrainian naval craft · Serbia: Aleksandar Cupic elected speaker, 140 votes · Suneung exam 551,864 sit · COP31 first draft · Voyager 1 one "
      "light-day · Van Gogh $190.4m · Pew projection Islam largest by 2035. Anthropic’s debut and the ~$2tn figure were Thursday’s news — not a Friday surge.")
dcl = wrap(d, dc, font(SERIF, 8), CW - 16)
text_lines(d, MX + 8, dy0 + 19, dcl, font(SERIF, 8), lh=10)
print(f"DATE CHECK: {len(dcl)} lines, box ends {dy0 + 62}")
dy1 = dy0 + 62

# ---------------------------------------------------------------- sources line
srcs = ("SOURCES: Kyiv Post · Reuters · Kyiv Independent · IMD · PTI · The Hindu · UN News · AFP · AP · Bloomberg · Morningstar · "
        "PBOC · EU Council · Al Jazeera · CGIL · ICC · USGS · Formula1.com · RNZ Pacific · ESA · BBC · ABC · SBS · Yonhap · Ukrinform · ATP · Xinhua.")
sl = wrap(d, srcs, font(SERIF, 8.5), CW)
text_lines(d, MX, dy1 + 5, sl, font(SERIF, 8.5), lh=10)
print(f"sources: {len(sl)} lines, ends y={dy1 + 5 + len(sl) * 10}")

img.save("entry.png", optimize=True)
data = open("entry.png", "rb").read()
print("entry.png", len(data), "bytes, sha256", hashlib.sha256(data).hexdigest())
