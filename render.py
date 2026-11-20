#!/usr/bin/env python3
"""news-image-20261120 — front-page render (rebuild of V1).

Draws a 1024x1024 newspaper front page with Pillow, from the design spec.
All facts come from the verified 20 Nov 2026 story list; 19 Nov events
appear ONLY in the DATE CHECK footer. Run:  python3 render.py
Writes entry.png next to this file.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
M = 20                      # outer margin
CW = W - 2 * M              # 984 content width

CREAM = (243, 235, 221)
TEAL = (7, 59, 58)
TEAL2 = (14, 90, 88)
TEAL3 = (24, 120, 116)
INK = (23, 35, 34)
RED = (200, 62, 58)
RED_D = (168, 44, 40)
GOLD = (201, 162, 74)
GOLD_L = (224, 190, 110)
WHITE = (255, 253, 246)
SEA = (62, 124, 122)
SEA_L = (94, 143, 138)
SKY_DUSK = (232, 165, 107)
GREY = (110, 110, 100)

FDIR = "/usr/share/fonts/truetype/liberation/"

def font(name, size):
    return ImageFont.truetype(FDIR + name, size)

SERIF_B = lambda s: font("LiberationSerif-Bold.ttf", s)
SERIF = lambda s: font("LiberationSerif-Regular.ttf", s)
SERIF_I = lambda s: font("LiberationSerif-Italic.ttf", s)
SANS = lambda s: font("LiberationSans-Regular.ttf", s)
SANS_B = lambda s: font("LiberationSans-Bold.ttf", s)
SANS_I = lambda s: font("LiberationSans-Italic.ttf", s)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(ov)

def tw(text, f):
    return d.textlength(text, font=f)

def wrap(text, f, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if tw(trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def para(x, y, text, f, max_w, color, lh=None):
    if lh is None:
        lh = int(f.size * 1.28)
    for ln in wrap(text, f, max_w):
        d.text((x, y), ln, font=f, fill=color)
        y += lh
    return y

def rrect(box, fill=None, outline=None, width=1, rad=4):
    d.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=width)

def hline(y, x0, x1, color, wdt=2):
    d.line([(x0, y), (x1, y)], fill=color, width=wdt)

# ---------------------------------------------------------------- masthead
y = 10
d.text((M, y), "THE WORLD TODAY", font=SANS_B(11), fill=TEAL)
right_top = "FRIDAY\u2019S NEWS  \u00b7  ONE PAGE  \u00b7  36 STORIES  \u00b7  6 CONTINENTS"
d.text((W - M - tw(right_top, SANS_B(11)), y), right_top, font=SANS_B(11), fill=INK)

y = 26
d.text((M, y), "THE WORLD TODAY", font=SERIF_B(30), fill=TEAL)
kick = "FRIDAY 20 NOVEMBER 2026"
d.text((W - M - tw(kick, SANS_B(12)), y + 12), kick, font=SANS_B(12), fill=GOLD)
hline(62, M, W - M, TEAL, 2)

y = 68
d.text((M, y), "FRIDAY, EVERYWHERE AT ONCE", font=SERIF_B(33), fill=TEAL)

y = 102
d.text((M, y), "Kyiv under fire  \u00b7  Akvan makes landfall  \u00b7  COP31 deadlocked  \u00b7  Asia\u2019s markets slide",
       font=SERIF_I(14), fill=RED)

# ---------------------------------------------------------------- number strip
NUMS = [
    ("300,000+", "evacuated in Odisha"),
    ("~30", "ballistic missiles fired at Kyiv"),
    ("\u22126.22%", "Taiex close"),
    ("2.3%", "Japan October headline CPI"),
    ("118", "Phillips vs India"),
    ("8 YEARS", "BepiColombo journey to Mercury"),
]
sy, sh = 122, 46
cell_w = CW / 6
for i, (num, lab) in enumerate(NUMS):
    x0 = M + i * cell_w
    d.rectangle([x0, sy, x0 + cell_w - 1, sy + sh], outline=TEAL, width=1)
    d.text((x0 + 8, sy + 4), num, font=SANS_B(20), fill=GOLD)
    d.text((x0 + 8, sy + 28), lab, font=SANS(9), fill=INK)
    d.line([(x0 + 8, sy + sh - 6), (x0 + 30, sy + sh - 6)], fill=RED, width=2)

# ---------------------------------------------------------------- region strip
REGIONS = [("EUROPE", "7", TEAL), ("AMERICAS", "8", TEAL2), ("ASIA-PACIFIC", "10", RED),
           ("MIDEAST", "3", TEAL), ("AFRICA", "3", TEAL2), ("OCEANIA", "4", TEAL),
           ("WORLD/SPACE", "1", GOLD)]
ry = 176
x = M
for name, n, col in REGIONS:
    label = f"{name} {n}"
    wdt = tw(label, SANS_B(10)) + 16
    rrect([x, ry, x + wdt, ry + 20], fill=col, rad=10)
    d.text((x + 8, ry + 4), label, font=SANS_B(10), fill=WHITE)
    x += wdt + 6
rlabel = "ALL STORIES: FRI 20 NOV 2026, ANY TIME ZONE"
d.text((W - M - tw(rlabel, SANS_B(9)), ry + 5), rlabel, font=SANS_B(9), fill=INK)

# ================================================================ LEAD ART
# All three illustrations are drawn from scratch here, differentiated
# from rank 1: bridge-at-dawn (not missile arcs), coastal overhead
# (not map spiral), negotiation hall (not globe/thermometer).

def fire_glow(cx, cy, r):
    """Orange fire glow: concentric translucent circles."""
    for k, (rr, a) in enumerate([(r, 90), (int(r * 0.62), 150), (int(r * 0.34), 230)]):
        od.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(255, 140, 40, a))
    od.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 220, 120, 255))

def draw_kyiv(x0, y0, w, h):
    """Dawn bridge over the Dnipro: sky, skyline, searchlights, fires,
    bridge silhouette in the foreground, red alert band on top."""
    # sky: dark teal top fading to dawn orange at the horizon
    for yy in range(h):
        t = yy / h
        r = int(7 + (232 - 7) * max(0, t - 0.55) / 0.45)
        g = int(59 + (165 - 59) * max(0, t - 0.55) / 0.45)
        b = int(58 + (107 - 58) * max(0, t - 0.55) / 0.45)
        d.line([(x0, y0 + yy), (x0 + w, y0 + yy)], fill=(r, g, b))
    # rising sun disc low on the horizon
    d.ellipse([x0 + w - 78, y0 + h - 62, x0 + w - 48, y0 + h - 32], fill=(255, 214, 130))
    # skyline silhouettes (dark teal) with a few lit windows
    skyline = [(0, 58, 26, 34), (30, 46, 22, 46), (56, 62, 30, 30), (90, 40, 18, 52),
               (112, 54, 26, 38), (142, 48, 20, 44), (166, 60, 30, 32), (200, 44, 16, 48),
               (220, 56, 26, 36), (250, 50, 22, 42), (276, 62, 30, 30)]
    for bx, by, bw, bh in skyline:
        d.rectangle([x0 + bx, y0 + h - 44 - bh + 22, x0 + bx + bw, y0 + h - 22], fill=(6, 38, 40))
    # tall tower with spire, left of centre
    d.rectangle([x0 + 96, y0 + 18, x0 + 104, y0 + h - 22], fill=(6, 38, 40))
    d.polygon([(x0 + 94, y0 + 18), (x0 + 106, y0 + 18), (x0 + 100, y0 + 6)], fill=(6, 38, 40))
    # golden domes
    for cx in (x0 + 150, x0 + 236):
        d.pieslice([cx - 9, y0 + h - 62, cx + 9, y0 + h - 44], 180, 360, fill=(201, 162, 74))
    # searchlight beams sweeping the sky (translucent pale gold)
    for (bx, by, tx, ty) in [(x0 + 60, y0 + h - 24, x0 + 130, y0 + 8),
                             (x0 + 190, y0 + h - 24, x0 + 120, y0 + 4),
                             (x0 + 260, y0 + h - 24, x0 + 300, y0 + 10)]:
        od.polygon([(bx - 4, by), (bx + 4, by), (tx + 7, ty), (tx - 7, ty)],
                   fill=(255, 240, 190, 60))
    # river band
    d.rectangle([x0, y0 + h - 22, x0 + w, y0 + h], fill=(38, 96, 96))
    for rx in range(0, w, 34):
        d.line([(x0 + rx, y0 + h - 10), (x0 + rx + 18, y0 + h - 10)], fill=(140, 190, 185), width=1)
    # fires glowing in three districts
    fire_glow(x0 + 44, y0 + h - 46, 12)
    fire_glow(x0 + 158, y0 + h - 52, 10)
    fire_glow(x0 + 208, y0 + h - 44, 11)
    # bridge silhouette across the foreground (deck + arch + cables)
    by = y0 + h - 26
    d.rectangle([x0, by, x0 + w, by + 7], fill=(4, 26, 28))
    d.arc([x0 + 30, by - 34, x0 + w - 30, by + 26], 180, 360, fill=(4, 26, 28), width=5)
    acx, acy, arx, ary = x0 + w / 2, by - 4, (w - 60) / 2, 30
    for cx in range(x0 + 46, x0 + w - 40, 26):
        t = (cx - acx) / arx
        top = acy - ary * math.sqrt(max(0.0, 1 - t * t))
        d.line([(cx, by), (cx, int(top))], fill=(4, 26, 28), width=2)
    for px in range(x0 + 8, x0 + w, 22):
        d.rectangle([px, by - 3, px + 3, by], fill=GOLD)
    # red alert band across the top
    d.rectangle([x0, y0, x0 + w, y0 + 15], fill=RED)
    d.text((x0 + 8, y0 + 3), "AIR ALERT  \u00b7  KYIV  \u00b7  01:25 LOCAL", font=SANS_B(9), fill=WHITE)

def draw_akvan(x0, y0, w, h):
    """Coastal view from directly above: sea left, land right, compact
    concentric cyclone rain bands offshore, wave lines, 3 red evacuation
    buses on the coast road, 2 red-roofed houses inland, red landfall flag."""
    # sea (left ~55%) and land (right)
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(196, 214, 196))
    coast = [(x0 + 168, y0), (x0 + 186, y0 + 26), (x0 + 172, y0 + 55),
             (x0 + 190, y0 + 84), (x0 + 176, y0 + 112), (x0 + 186, y0 + h)]
    d.polygon([(x0, y0)] + coast + [(x0, y0 + h)], fill=SEA)
    # sandy beach strip along the coast
    d.line([(x0 + 168, y0), (x0 + 186, y0 + 26), (x0 + 172, y0 + 55),
            (x0 + 190, y0 + 84), (x0 + 176, y0 + 112), (x0 + 186, y0 + h)],
           fill=(240, 225, 190), width=4)
    # wave lines on the open sea (left of the storm core)
    for wy, wx0, wx1 in [(y0 + 18, 8, 44), (y0 + 96, 10, 48), (y0 + 116, 30, 62)]:
        d.arc([x0 + wx0, wy - 6, x0 + wx1, wy + 6], 200, 340, fill=(220, 240, 235), width=2)
    # compact concentric cyclone rain bands offshore (core well left of coast)
    cx, cy = x0 + 92, y0 + 58
    for rr, col, wd in [(54, (255, 253, 246), 6), (42, (24, 120, 116), 5),
                        (30, (255, 253, 246), 5), (18, (7, 59, 58), 4)]:
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 150, 30, fill=col, width=wd)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=WHITE, outline=TEAL, width=2)
    # coastal road (cream line hugging the coast, inland side)
    road = [(x0 + 196, y0 + 4), (x0 + 210, y0 + 30), (x0 + 198, y0 + 58),
            (x0 + 214, y0 + 86), (x0 + 202, y0 + h - 4)]
    d.line(road, fill=(255, 253, 246), width=9)
    d.line(road, fill=(201, 162, 74), width=1)
    # three red evacuation buses moving away from the shore (up the road)
    for bx, by in [(x0 + 204, y0 + 24), (x0 + 200, y0 + 62), (x0 + 208, y0 + 98)]:
        d.rectangle([bx - 5, by - 11, bx + 5, by + 11], fill=RED, outline=WHITE, width=1)
        d.rectangle([bx - 5, by - 11, bx + 5, by - 4], fill=(255, 220, 120))
        d.rectangle([bx - 4, by + 1, bx + 4, by + 7], fill=(255, 253, 246))
    # two red-roofed houses inland
    for hx, hy in [(x0 + 248, y0 + 30), (x0 + 268, y0 + 84)]:
        d.rectangle([hx, hy, hx + 22, hy + 14], fill=(255, 253, 246), outline=TEAL, width=1)
        d.polygon([(hx - 2, hy), (hx + 11, hy - 10), (hx + 24, hy)], fill=RED)
        d.rectangle([hx + 9, hy + 6, hx + 13, hy + 14], fill=TEAL)
    # red landfall flag near the coast
    fx, fy = x0 + 176, y0 + 104
    d.line([(fx, fy), (fx, fy - 28)], fill=INK, width=2)
    d.polygon([(fx, fy - 28), (fx + 20, fy - 22), (fx, fy - 16)], fill=RED)
    d.text((fx + 4, fy + 2), "GOPALPUR", font=SANS_B(8), fill=INK)
    # rain streaks over land
    for sx in range(x0 + 232, x0 + w - 6, 20):
        d.line([(sx, y0 + 12), (sx - 4, y0 + 22)], fill=(120, 150, 145), width=1)

def draw_cop31(x0, y0, w, h):
    """Negotiation hall: flags above the chamber, ceiling lights, two
    delegate tables flanking a central podium with gold top and mic,
    white DRAFT document with red seal in the foreground."""
    # hall walls: teal with cream panel lines
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=TEAL2)
    d.rectangle([x0, y0, x0 + w, y0 + 26], fill=TEAL)
    for px in range(x0 + 14, x0 + w, 44):
        d.line([(px, y0 + 30), (px, y0 + h)], fill=(24, 120, 116), width=1)
    # ceiling lights: two rows of gold dots with glow
    for lx in range(x0 + 18, x0 + w - 8, 26):
        od.ellipse([lx - 7, y0 + 30, lx + 7, y0 + 44], fill=(255, 220, 120, 70))
        d.ellipse([lx - 3, y0 + 33, lx + 3, y0 + 39], fill=GOLD_L)
    # flags hung above the chamber
    flag_cols = [RED, GOLD, WHITE, (40, 110, 180), (30, 140, 90), RED, GOLD, WHITE]
    for i, col in enumerate(flag_cols):
        fx = x0 + 16 + i * 38
        d.line([(fx + 11, y0 + 2), (fx + 11, y0 + 16)], fill=INK, width=1)
        d.rectangle([fx, y0 + 4, fx + 22, y0 + 15], fill=col, outline=INK, width=1)
    # floor
    d.rectangle([x0, y0 + h - 26, x0 + w, y0 + h], fill=(5, 40, 42))
    # delegate tables left and right, with seated delegates
    for tx in (x0 + 8, x0 + w - 88):
        d.rectangle([tx, y0 + 62, tx + 80, y0 + 74], fill=(196, 178, 140))
        d.rectangle([tx, y0 + 62, tx + 80, y0 + 66], fill=GOLD)
        for j, dc in enumerate([(200, 62, 58), (255, 253, 246), (201, 162, 74), (120, 180, 170)]):
            dx = tx + 12 + j * 18
            d.ellipse([dx - 5, y0 + 48, dx + 5, y0 + 58], fill=dc, outline=INK, width=1)
            d.pieslice([dx - 7, y0 + 57, dx + 7, y0 + 71], 180, 360, fill=dc, outline=INK, width=1)
        # name plates + papers on the table
        for j in range(4):
            d.rectangle([tx + 8 + j * 18, y0 + 68, tx + 18 + j * 18, y0 + 72], fill=WHITE)
    # central podium with gold top and microphone
    px0 = x0 + w // 2 - 26
    d.rectangle([px0, y0 + 58, px0 + 52, y0 + 96], fill=TEAL)
    d.rectangle([px0 - 4, y0 + 52, px0 + 56, y0 + 60], fill=GOLD)
    d.line([(px0 + 40, y0 + 54), (px0 + 30, y0 + 40)], fill=INK, width=2)
    d.ellipse([px0 + 27, y0 + 36, px0 + 33, y0 + 42], fill=INK)
    d.ellipse([x0 + w // 2 - 8, y0 + 66, x0 + w // 2 + 8, y0 + 82], fill=GOLD, outline=WHITE, width=1)
    d.text((x0 + w // 2 - 4, y0 + 69), "31", font=SANS_B(9), fill=TEAL)
    # foreground: white DRAFT document with red seal (drawn on the main
    # layer so it stays opaque and legible, overlapping the podium base)
    dx0, dy0 = x0 + w // 2 - 8, y0 + h - 40
    d.rectangle([dx0, dy0, dx0 + 118, dy0 + 36], fill=WHITE, outline=INK, width=1)
    d.text((dx0 + 8, dy0 + 4), "DRAFT", font=SANS_B(11), fill=INK)
    for ly in range(dy0 + 20, dy0 + 33, 4):
        d.line([(dx0 + 8, ly), (dx0 + 72, ly)], fill=(150, 150, 140), width=1)
    d.ellipse([dx0 + 82, dy0 + 6, dx0 + 110, dy0 + 32], fill=RED, outline=WHITE, width=1)
    d.text((dx0 + 88, dy0 + 14), "COP", font=SANS_B(8), fill=WHITE)

# ---------------------------------------------------------------- lead cards
LEADS = [
    dict(num="01", tag="KYIV", art=draw_kyiv,
         bar="01:25 LOCAL  \u00b7  7 WAVES  \u00b7  ~30 MISSILES",
         head="Kyiv hit by seven-wave overnight barrage",
         body=("Russia fired about 30 ballistic missiles in seven overnight waves "
               "beginning at 01:25 local. Three water workers were killed; bridges, "
               "energy and transport were hit, fires burned in three districts, Dutch "
               "and Austrian embassies were damaged, and power and water were cut."),
         what="SO WHAT \u2014 The barrage hit essential services as well as the capital\u2019s transport links.",
         src="Kyiv Post \u00b7 Reuters \u00b7 Kyiv Independent"),
    dict(num="02", tag="ODISHA / AKVAN", art=draw_akvan,
         bar="LANDFALL 02:00 UTC  \u00b7  GUSTS 110 KM/H  \u00b7  300,000+ EVACUATED",
         head="Cyclone Akvan makes landfall in Odisha",
         body=("Akvan made landfall near Gopalpur around 8am (02:00 UTC), with winds "
               "of 70\u2013100 km/h and gusts to 110. More than 300,000 people were "
               "evacuated; 423 rescue teams, schools shut and trains cancelled. "
               "No deaths were reported by midday."),
         what="SO WHAT \u2014 Mass evacuations preceded landfall; no deaths had been reported by midday.",
         src="IMD \u00b7 PTI \u00b7 The Hindu"),
    dict(num="03", tag="ANTALYA / COP31", art=draw_cop31,
         bar="FINAL DAY  \u00b7  $120BN FINANCE GAP",
         head="COP31 ends in a finance deadlock",
         body=("On COP31\u2019s final day, the draft omitted fossil fuels and the $120bn "
               "adaptation-finance question remained unresolved. Hosts pushed a "
               "\u201c35 by 35\u201d clean-power goal. Talks may run into the weekend."),
         what="SO WHAT \u2014 The final-day draft leaves the fossil-fuel and adaptation-finance questions unresolved.",
         src="UN News \u00b7 Reuters \u00b7 AFP"),
]
LY, LH, LW, LG = 202, 288, 320, 12
for i, L in enumerate(LEADS):
    x0 = M + i * (LW + LG)
    d.rectangle([x0, LY, x0 + LW, LY + LH], outline=TEAL, width=1)
    L["art"](x0 + 1, LY + 1, LW - 2, 124)
    # data bar
    d.rectangle([x0, LY + 125, x0 + LW, LY + 141], fill=TEAL)
    d.text((x0 + 8, LY + 129), L["bar"], font=SANS_B(9), fill=GOLD_L)
    # number + tag
    d.text((x0 + 8, LY + 146), L["num"], font=SANS_B(11), fill=RED)
    d.text((x0 + 34, LY + 146), L["tag"], font=SANS_B(11), fill=TEAL)
    # headline (2 lines max)
    hy = LY + 162
    for ln in wrap(L["head"], SERIF_B(15), LW - 16)[:2]:
        d.text((x0 + 8, hy), ln, font=SERIF_B(15), fill=INK)
        hy += 18
    # body (~35 words, 5 lines max)
    by = hy + 3
    by = para(x0 + 8, by, L["body"], SANS(10), LW - 16, INK, lh=12)
    # SO WHAT (red, 2 lines max)
    wy = by + 3
    wy = para(x0 + 8, wy, L["what"], SANS_B(10), LW - 16, RED, lh=12)
    d.text((x0 + 8, LY + LH - 13), L["src"], font=SANS_I(8), fill=GREY)

# ---------------------------------------------------------------- hours strip
HY = 496
d.text((M, HY), "THE DAY BY HOURS", font=SANS_B(11), fill=TEAL)
hline(HY + 16, M, W - M, RED, 2)
HOURS = [("00:49 UTC", "New Caledonia quake"), ("01:25 local", "Kyiv barrage"),
         ("02:00 UTC", "Akvan landfall"), ("Morning", "Asia markets plunge"),
         ("Midday", "COP31 final day"), ("P.M.", "Brussels reset summit"),
         ("Evening", "Las Vegas practice")]
hx = M
for t, lab in HOURS:
    d.ellipse([hx, HY + 22, hx + 7, HY + 29], fill=GOLD, outline=TEAL, width=1)
    d.text((hx + 10, HY + 20), t, font=SANS_B(9), fill=TEAL)
    d.text((hx + 10, HY + 31), lab, font=SANS(8), fill=INK)
    hx += 142

# ---------------------------------------------------------------- feature tiles
def strip_chart(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=TEAL)
    for gx in range(x0 + 20, x0 + w, 22):
        d.line([(gx, y0 + 3), (gx, y0 + h - 3)], fill=TEAL3, width=1)
    d.line([(x0 + 6, y0 + 6), (x0 + w - 6, y0 + 6)], fill=RED, width=1)
    pts = [(x0 + 8, y0 + 6), (x0 + 50, y0 + 10), (x0 + 95, y0 + 14),
           (x0 + 140, y0 + 22), (x0 + w - 8, y0 + 28)]
    d.line(pts, fill=RED, width=3)
    d.text((x0 + 8, y0 + h - 11), "TAIEX  KOSPI  NIKKEI", font=SANS_B(7), fill=WHITE)

def strip_bars(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=CREAM)
    vals = [1.6, 1.9, 2.1, 2.2]
    for i, v in enumerate(vals):
        bx = x0 + 22 + i * 34
        bh = int(v / 2.5 * (h - 12))
        d.rectangle([bx, y0 + h - 5 - bh, bx + 20, y0 + h - 5], fill=TEAL2)
    ly = y0 + h - 5 - int(2.0 / 2.5 * (h - 12))
    for dx in range(x0 + 6, x0 + w - 4, 8):
        d.line([(dx, ly), (dx + 4, ly)], fill=GOLD, width=2)
    d.text((x0 + w - 34, ly - 9), "2%", font=SANS_B(8), fill=GOLD)
    d.text((x0 + 8, y0 + 2), "2.2%", font=SANS_B(8), fill=RED)

def strip_flat(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=TEAL)
    my = y0 + h // 2
    d.line([(x0 + 8, my), (x0 + w - 8, my)], fill=GOLD, width=3)
    for dx in range(x0 + 20, x0 + w - 10, 26):
        d.ellipse([dx - 2, my - 2, dx + 2, my + 2], fill=WHITE)
    d.text((x0 + 8, y0 + 3), "1-YR 3.0%", font=SANS_B(8), fill=WHITE)
    d.text((x0 + w - 62, y0 + h - 12), "5-YR 3.5%", font=SANS_B(8), fill=GOLD_L)

def strip_flags(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=CREAM)
    # EU flag
    d.rectangle([x0 + 14, y0 + 5, x0 + 82, y0 + h - 5], fill=(30, 60, 150))
    for k in range(8):
        a = k * math.pi / 4
        sx = x0 + 48 + int(11 * math.cos(a)); sy = y0 + h // 2 + int(7 * math.sin(a))
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=GOLD)
    # UK flag (simplified)
    d.rectangle([x0 + 100, y0 + 5, x0 + w - 14, y0 + h - 5], fill=(30, 60, 150))
    d.line([(x0 + 100, y0 + h // 2), (x0 + w - 14, y0 + h // 2)], fill=WHITE, width=5)
    d.line([(x0 + (100 + w - 14) // 2, y0 + 5), (x0 + (100 + w - 14) // 2, y0 + h - 5)], fill=WHITE, width=5)
    d.line([(x0 + 100, y0 + h // 2), (x0 + w - 14, y0 + h // 2)], fill=RED, width=2)
    d.line([(x0 + (100 + w - 14) // 2, y0 + 5), (x0 + (100 + w - 14) // 2, y0 + h - 5)], fill=RED, width=2)

def strip_intercept(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(6, 30, 40))
    for sx, sy in [(30, 8), (70, 14), (120, 6), (160, 12), (90, 20)]:
        d.ellipse([x0 + sx, y0 + sy, x0 + sx + 1, y0 + sy + 1], fill=WHITE)
    d.arc([x0 + 10, y0 - 6, x0 + w - 20, y0 + h + 6], 300, 60, fill=GOLD_L, width=2)
    bx, by = x0 + w - 42, y0 + 8
    for dx, dy in [(0, 0), (6, 0), (-6, 0), (0, 6), (0, -6), (4, 4), (-4, -4)]:
        d.line([(bx, by), (bx + dx, by + dy)], fill=GOLD, width=1)
    d.ellipse([bx - 2, by - 2, bx + 2, by + 2], fill=WHITE)

def strip_tanker(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA)
    for wy in (y0 + h - 8, y0 + h - 4):
        d.line([(x0 + 4, wy), (x0 + w - 4, wy)], fill=(220, 240, 235), width=1)
    for tx in (x0 + 12, x0 + 92):
        d.polygon([(tx, y0 + 16), (tx + 58, y0 + 16), (tx + 52, y0 + 24), (tx + 6, y0 + 24)],
                  fill=(10, 40, 42))
        d.rectangle([tx + 20, y0 + 9, tx + 30, y0 + 16], fill=(10, 40, 42))
    # oil barrel
    d.rectangle([x0 + w - 30, y0 + 8, x0 + w - 12, y0 + 26], fill=RED)
    d.ellipse([x0 + w - 30, y0 + 5, x0 + w - 12, y0 + 11], fill=(230, 90, 85))

def strip_ballot(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=CREAM)
    d.rectangle([x0 + 22, y0 + 12, x0 + 82, y0 + h - 5], fill=TEAL)
    d.rectangle([x0 + 34, y0 + 8, x0 + 70, y0 + 12], fill=TEAL)
    d.line([(x0 + 40, y0 + 9), (x0 + 64, y0 + 9)], fill=GOLD, width=2)
    d.rectangle([x0 + 44, y0 - 2, x0 + 60, y0 + 8], fill=WHITE, outline=INK, width=1)
    d.text((x0 + 100, y0 + 8), "2027", font=SANS_B(16), fill=GOLD)
    d.text((x0 + 100, y0 + 24), "VOTE", font=SANS_B(8), fill=TEAL)

def strip_boat(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(150, 195, 195))
    for wy in (y0 + 20, y0 + 26):
        d.arc([x0 + 6, wy - 5, x0 + w - 6, wy + 5], 200, 340, fill=WHITE, width=2)
    d.polygon([(x0 + 70, y0 + 24), (x0 + 120, y0 + 24), (x0 + 112, y0 + 14),
               (x0 + 78, y0 + 14)], fill=(10, 40, 42))
    d.line([(x0 + 95, y0 + 14), (x0 + 95, y0 + 2)], fill=INK, width=2)
    for dx in (80, 92, 104):
        d.ellipse([x0 + dx, y0 + 8, x0 + dx + 5, y0 + 13], fill=INK)

def strip_strike(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=CREAM)
    # Italian flag: green / white / red vertical bands
    for i, col in enumerate([(0, 140, 70), WHITE, RED]):
        d.rectangle([x0 + 12 + i * 18, y0 + 5, x0 + 30 + i * 18, y0 + h - 5], fill=col,
                    outline=INK, width=1)
    # raised fist (gold silhouette)
    fx, fy = x0 + 110, y0 + 2
    d.rounded_rectangle([fx, fy + 8, fx + 30, fy + 24], radius=4, fill=GOLD)
    for k in range(4):
        d.rounded_rectangle([fx + 2 + k * 7, fy, fx + 8 + k * 7, fy + 12], radius=2, fill=GOLD)
    d.rectangle([fx + 6, fy + 22, fx + 24, y0 + h - 3], fill=GOLD)

def strip_cricket(x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=TEAL)
    # bat, angled
    d.polygon([(x0 + 30, y0 + 26), (x0 + 44, y0 + 24), (x0 + 78, y0 + 6),
               (x0 + 70, y0 + 2)], fill=(240, 225, 190))
    d.line([(x0 + 76, y0 + 4), (x0 + 92, y0 + 12)], fill=(240, 225, 190), width=4)
    # red ball
    d.ellipse([x0 + 100, y0 + 14, x0 + 112, y0 + 26], fill=RED, outline=WHITE, width=1)
    # gold 118 badge
    d.ellipse([x0 + w - 52, y0 + 4, x0 + w - 8, y0 + 28], fill=GOLD, outline=WHITE, width=1)
    d.text((x0 + w - 46, y0 + 10), "118", font=SANS_B(11), fill=TEAL)

TILES = [
    dict(num="04", tag="TAIPEI / SEOUL / TOKYO", art=strip_chart,
         head="AI sell-off hits Asian markets",
         body=("Taiex \u22126.22% to 36,033.29 (\u22122,393.60); below 36,000 intraday. "
               "150 limit-down; worst week since 1991 (\u221217%). TSMC below NT$2,000; "
               "KOSPI \u22125.4%, Nikkei \u22124.9%."),
         cons="\u2192 Risk-off trading spread across Asia.",
         src="AP \u00b7 Bloomberg"),
    dict(num="05", tag="TOKYO \u2014 ECONOMY", art=strip_bars,
         head="Japan core inflation stays above target",
         body=("Core inflation was 2.2% in October; headline inflation was 2.3%. "
               "Core inflation was above 2% for a second month."),
         cons="\u2192 A BoJ hike is eyed in December.",
         src="Reuters \u00b7 Jiji"),
    dict(num="06", tag="BEIJING \u2014 RATES", art=strip_flat,
         head="China holds lending rates for 18th month",
         body="The 1-year LPR stays at 3.0%. The 5-year LPR stays at 3.5%.",
         cons="\u2192 Both lending rates remain unchanged.",
         src="PBOC \u00b7 Reuters"),
    dict(num="07", tag="BRUSSELS \u2014 EUROPE", art=strip_flags,
         head="First EU\u2013UK reset summit",
         body=("Costa and von der Leyen host UK PM Burnham. Food deal, carbon-market "
               "link and 100,000 youth places are on the agenda."),
         cons="\u2192 The summit puts trade, climate and youth ties on the agenda.",
         src="EU Council \u00b7 Reuters"),
    dict(num="08", tag="RIYADH / S. SAUDI \u2014 CONFLICT", art=strip_intercept,
         head="Saudi defences intercept missile and drones",
         body=("Houthi ballistic missile and drones intercepted over Jazan, Abha and "
               "Khamis Mushait. Saudi airstrikes hit Sanaa Friday."),
         cons="\u2192 Interceptions over Saudi Arabia and strikes in Sanaa mark the day\u2019s conflict.",
         src="Reuters"),
    dict(num="09", tag="HORMUZ \u2014 ENERGY", art=strip_tanker,
         head="Strait stays shut as shipping waits",
         body=("Brent trades near $92.50; 46 ships are waiting. "
               "Gulf war-risk cover is up 200x."),
         cons="\u2192 Ships wait as war-risk cover surges.",
         src="Reuters \u00b7 Al Jazeera"),
    dict(num="10", tag="SAN SALVADOR \u2014 POLITICS", art=strip_ballot,
         head="Bukele files for third term",
         body=("Filing came by the Thu night deadline, 20 Nov UTC; supporters cheer. "
               "Rights groups object; the vote is 28 Feb 2027."),
         cons="\u2192 A contested third-term bid heads toward the February 2027 vote.",
         src="AP \u00b7 Al Jazeera"),
    dict(num="11", tag="SENEGAL / CANARY \u2014 MIGRATION", art=strip_boat,
         head="Migrant boat capsizes off Senegal",
         body=("Four dead; dozens missing from 50\u2013100 aboard. "
               "Canary arrivals surge to 24,364 this year."),
         cons="\u2192 The capsizing toll and missing count come amid rising Canary arrivals.",
         src="Al Jazeera \u00b7 AFP"),
    dict(num="12", tag="ROME \u2014 LABOUR", art=strip_strike,
         head="Italy\u2019s CGIL calls 24-hour general strike",
         body=("Unions rally in ~100 squares against the 2027 budget. "
               "Transit is hit."),
         cons="\u2192 Transit services are affected during the 24-hour stoppage.",
         src="CGIL \u00b7 AFP"),
    dict(num="13", tag="WELLINGTON \u2014 CRICKET", art=strip_cricket,
         head="Phillips makes history against India",
         body=("His 118 makes him the first NZ batter with centuries in all 3 formats "
               "vs India in a year. NZ 368; India 159-1 at stumps on day two."),
         cons="\u2192 New Zealand lead India at stumps on day two.",
         src="ICC \u00b7 AP"),
]

TW, TG, TH = 188, 11, 144
TY = 540
for idx, T in enumerate(TILES):
    row, col = divmod(idx, 5)
    x0 = M + col * (TW + TG)
    y0 = TY + row * (TH + 6)
    d.rectangle([x0, y0, x0 + TW, y0 + TH], outline=TEAL, width=1)
    T["art"](x0 + 1, y0 + 1, TW - 2, 32)
    tx = x0 + 6
    d.text((tx, y0 + 36), f"{T['num']}  {T['tag']}", font=SANS_B(8), fill=RED)
    hy = y0 + 47
    for ln in wrap(T["head"], SANS_B(12), TW - 12)[:2]:
        d.text((tx, hy), ln, font=SANS_B(12), fill=INK)
        hy += 14
    by = hy + 2
    blines = wrap(T["body"], SANS(9), TW - 12)
    for ln in blines[:4]:
        d.text((tx, by), ln, font=SANS(9), fill=INK)
        by += 11
    cy = by + 2
    for ln in wrap(T["cons"], SANS_B(9), TW - 12)[:2]:
        d.text((tx, cy), ln, font=SANS_B(9), fill=RED)
        cy += 11
    d.text((tx, y0 + TH - 10), T["src"], font=SANS_I(7), fill=GREY)
    print(f"tile {T['num']}: head {len(wrap(T['head'], SANS_B(12), TW-12))} lines, "
          f"body {len(blines)} lines, cons {len(wrap(T['cons'], SANS_B(9), TW-12))} lines")

# ---------------------------------------------------------------- bottom: map + ALSO
BY = 840
MAP_W = 310
d.text((M, BY), "THE WORLD IN ONE DAY", font=SANS_B(11), fill=TEAL)
map_x, map_y, map_w, map_h = M, BY + 14, MAP_W, 82
d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=TEAL)
# rough continents (lighter teal blobs)
d.polygon([(map_x + 12, map_y + 18), (map_x + 66, map_y + 10), (map_x + 78, map_y + 26),
           (map_x + 52, map_y + 38), (map_x + 20, map_y + 34)], fill=TEAL3)          # N America
d.polygon([(map_x + 58, map_y + 46), (map_x + 84, map_y + 44), (map_x + 88, map_y + 62),
           (map_x + 72, map_y + 76), (map_x + 60, map_y + 60)], fill=TEAL3)          # S America
d.polygon([(map_x + 140, map_y + 12), (map_x + 168, map_y + 10), (map_x + 172, map_y + 26),
           (map_x + 150, map_y + 32), (map_x + 140, map_y + 22)], fill=TEAL3)        # Europe
d.polygon([(map_x + 142, map_y + 38), (map_x + 172, map_y + 36), (map_x + 178, map_y + 56),
           (map_x + 162, map_y + 70), (map_x + 146, map_y + 54)], fill=TEAL3)        # Africa
d.polygon([(map_x + 176, map_y + 10), (map_x + 262, map_y + 8), (map_x + 272, map_y + 26),
           (map_x + 240, map_y + 40), (map_x + 196, map_y + 38), (map_x + 178, map_y + 24)],
          fill=TEAL3)                                                               # Asia
d.polygon([(map_x + 252, map_y + 56), (map_x + 282, map_y + 54), (map_x + 286, map_y + 66),
           (map_x + 258, map_y + 70)], fill=TEAL3)                                  # Australia
# SPACE / Mercury inset (top-left ocean area)
d.rectangle([map_x + 6, map_y + 4, map_x + 108, map_y + 22], outline=GOLD, width=1)
d.text((map_x + 10, map_y + 6), "SPACE / MERCURY", font=SANS_B(7), fill=GOLD_L)
d.text((map_x + 10, map_y + 13), "BepiColombo arrives", font=SANS(7), fill=WHITE)
# numbered red pins 1-13 (nudged so the Europe/Asia clusters stay legible)
PINS = {1: (186, 20), 2: (226, 38), 3: (176, 36), 4: (256, 38), 5: (272, 28),
        6: (246, 24), 7: (156, 22), 8: (192, 40), 9: (206, 30), 10: (80, 42),
        11: (140, 42), 12: (168, 27), 13: (298, 64)}
for n, (px, py) in PINS.items():
    cx, cy = map_x + px, map_y + py
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED, outline=WHITE, width=1)
    lbl = str(n)
    d.text((cx - tw(lbl, SANS_B(7)) / 2, cy - 4), lbl, font=SANS_B(7), fill=WHITE)
d.text((M, BY + 100), "1\u20133 LEAD  \u00b7  4\u201313 FEATURE \u2014 36 stories, one Friday.",
       font=SANS_B(8), fill=TEAL)

# ALSO list (23 more stories, 3 columns)
AX = M + MAP_W + 12
d.text((AX, BY), "ALSO ON FRIDAY 20 NOVEMBER \u2014 23 MORE STORIES", font=SANS_B(11), fill=TEAL)
ALSO = [
    ("14", "NEW CALEDONIA", "M5.6 quake; no tsunami"),
    ("15", "LAS VEGAS", "Russell fastest wet practice, 1:47.272"),
    ("16", "COOK ISLANDS", "Cyclone Xavier nears atoll"),
    ("17", "MERCURY", "BepiColombo arrives; orbit insertion Sat"),
    ("18", "SYDNEY", "Man charged with terror offences; no threat"),
    ("19", "SEOUL", "Ruling party moves to impeach top judge"),
    ("20", "BRASILIA", "Lula meets Chief Raoni; land recognised"),
    ("21", "SEOUL", "Bill adopted to impeach chief justice"),
    ("22", "BEIJING", "State media: Xi for three-way talks"),
    ("23", "KHARKIV", "Drone hits hospital; at least four hurt"),
    ("24", "KRYVYI RIH", "Drone attack cuts power to hospitals"),
    ("25", "DNIPRO", "Five injured in drone attack"),
    ("26", "TURIN", "ATP Finals groups end; semis Saturday"),
    ("27", "ANTALYA", "France calls fossil-fuel gap \u201cblack mark\u201d"),
    ("28", "SEOUL", "Court upholds Kakao founder acquittal"),
    ("29", "TAIPEI", "Taiex set for worst week since 1991"),
    ("30", "HONG KONG", "Hang Seng ~20% off January peak"),
    ("31", "SYDNEY", "General Pants enters administration"),
    ("32", "ODISHA", "209mm rain at Patrapur as Akvan crosses"),
    ("33", "BEIT SHEMESH", "Haredi protesters clash with police"),
    ("34", "DAKAR", "Four bodies found after boat capsized"),
    ("35", "PORT-AU-PRINCE", "Raid killed 34 gang suspects"),
    ("36", "MEXICO CITY", "Nation marks 116th Revolution Day"),
]
COL_W = 214
also_bottom = 0
for ci in range(3):
    cx = AX + ci * (COL_W + 8)
    cy = BY + 16
    for n, place, fact in ALSO[ci * 8:(ci + 1) * 8]:
        line = f"{n} {place} \u2014 {fact}"
        for ln in wrap(line, SANS(8), COL_W):
            d.text((cx, cy), ln, font=SANS(8), fill=INK)
            cy += 10
    also_bottom = max(also_bottom, cy)
print("also bottom:", also_bottom)

# ---------------------------------------------------------------- DATE CHECK
DY = 952
d.rectangle([M, DY, W - M, DY + 46], fill=RED)
d.text((M + 8, DY + 3), "DATE CHECK \u2014 19 NOVEMBER, NOT TODAY\u2019S STORY LIST:",
       font=SANS_B(9), fill=WHITE)
dc = ("Shenzhen trilateral summit + peace declaration \u00b7 ICJ Myanmar genocide ruling 9-6 \u00b7 "
      "Anthropic IPO debut (opened $111.50, +34% vs $83; closed $97.17, +17%) \u00b7 UK \u00a3260m drone "
      "package for Ukraine \u00b7 US sanctions on Comancheros + \u2019Ndrangheta \u00b7 US Senate rejects Iran "
      "war-powers 51-48 \u00b7 Houthi strike on Riyadh PIF Tower (Thu) \u00b7 Tanker mine incidents in "
      "Hormuz (Thu) \u00b7 Georgia gas explosion, 6 dead (Thu) \u00b7 UK+Norway \u00a3100m+ for two Ukrainian "
      "naval craft \u00b7 Serbia speaker elected \u00b7 Suneung exam \u00b7 COP31 first draft \u00b7 Voyager 1 one "
      "light-day \u00b7 Van Gogh $190.4m \u00b7 Pew Islam projection.")
para(M + 8, DY + 15, dc, SANS(8), CW - 16, WHITE, lh=10)

# ---------------------------------------------------------------- sources
d.text((M, 1004), "SOURCES: Reuters, AP, AFP, Bloomberg, PTI, IMD, Kyiv Post, Kyiv Independent, UN News, "
                  "EU Council, PBOC, ICC, USGS, ESA, Formula1.com, Al Jazeera, SBS, RNZ, Xinhua, ATP.",
       font=SANS(8), fill=INK)

img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
img.save(OUT, "PNG")
print("saved", OUT, img.size)
