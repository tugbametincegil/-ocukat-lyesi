import math, random, sys, os
from PIL import Image, ImageDraw, ImageFont

S = 2
W, H = 1080, 1920
FPS = 30
DUR = 36.5
OL = (88, 58, 48)
SKIN = (255, 218, 185)
WHITE = (255, 255, 255)
FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts", "Poppins-Bold.ttf")
_fc = {}
def F(sz):
    sz = int(sz)
    if sz not in _fc:
        _fc[sz] = ImageFont.truetype(FONT_PATH, sz)
    return _fc[sz]

def cl(x): return max(0.0, min(1.0, x))
def so(x):
    x = cl(x); return x * x * (3 - 2 * x)
def back(x):
    x = cl(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def lerp(a, b, t): return a + (b - a) * t
def mix(c1, c2, t): return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))

class Pen:
    def __init__(self, img):
        self.d = ImageDraw.Draw(img)
    def E(self, cx, cy, rx, ry, fill, out=None, ow=0):
        self.d.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S],
                       fill=fill, outline=out, width=int(ow * S) if out else 0)
    def RR(self, x0, y0, x1, y1, r, fill, out=None, ow=0):
        self.d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S,
                                 fill=fill, outline=out, width=int(ow * S) if out else 0)
    def LN(self, pts, w, fill, caps=True):
        P = [(x * S, y * S) for x, y in pts]
        self.d.line(P, fill=fill, width=int(w * S), joint="curve")
        if caps:
            r = w / 2
            for x, y in (pts[0], pts[-1]):
                self.E(x, y, r, r, fill)
    def PG(self, pts, fill, out=None, ow=0):
        self.d.polygon([(x * S, y * S) for x, y in pts], fill=fill)
        if out:
            self.LN(pts + [pts[0]], ow, out, caps=False)
    def TX(self, x, y, s, size, fill, anchor="mm"):
        self.d.text((x * S, y * S), s, font=F(size * S), fill=fill, anchor=anchor)
    def TW(self, s, size):
        return self.d.textlength(s, font=F(size * S)) / S

def star(p, cx, cy, r, col):
    pts = []
    for i in range(8):
        a = math.pi / 4 * i - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.28
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    p.PG(pts, col)

# ---------- static layers ----------
def build_wall():
    img = Image.new("RGB", (W * S, H * S))
    p = Pen(img)
    for y in range(0, H):
        c = mix((255, 236, 200), (255, 207, 160), y / 1100) if y < 1100 else (255, 207, 160)
        p.d.rectangle([0, y * S, W * S, (y + 1) * S], fill=c)
    for x in range(0, W, 120):  # soft stripes
        p.d.rectangle([x * S, 0, (x + 60) * S, 1100 * S], fill=(255, 230, 190))
    # window
    p.RR(70, 400, 330, 700, 24, (170, 225, 245), OL, 8)
    p.LN([(200, 400), (200, 700)], 8, OL, False)
    p.LN([(70, 550), (330, 550)], 8, OL, False)
    p.E(120, 450, 26, 26, (255, 245, 170))
    # shelf with jars
    p.RR(700, 560, 1030, 580, 8, (176, 116, 70), OL, 5)
    for i, (c, h) in enumerate([((240, 120, 100), 90), ((120, 200, 120), 110), ((250, 200, 90), 80)]):
        x = 730 + i * 100
        p.RR(x, 560 - h, x + 70, 560, 14, c, OL, 5)
        p.RR(x + 8, 560 - h - 16, x + 62, 560 - h + 4, 6, (250, 250, 250), OL, 4)
    # lamp
    p.LN([(540, 0), (540, 150)], 6, OL, False)
    p.PG([(450, 260), (630, 260), (580, 150), (500, 150)], (255, 170, 80), OL, 6)
    p.E(540, 262, 40, 12, (255, 240, 170))
    return img

def build_counter():
    cy0 = 1100
    img = Image.new("RGB", (W * S, (H - cy0) * S))
    p = Pen(img)
    def Y(y): return y - cy0
    p.d.rectangle([0, 0, W * S, 280 * S], fill=(236, 184, 120))        # surface
    p.d.rectangle([0, 262 * S, W * S, 292 * S], fill=(190, 128, 76))   # edge
    for y in range(292, H):
        p.d.rectangle([0, Y(y) * S, W * S, Y(y + 1) * S],
                      fill=mix((205, 140, 84), (176, 112, 66), (y - 292) / 1628))
    for yy in (420, 560, 700, 840, 980):
        p.LN([(0, yy), (W, yy)], 5, (160, 100, 58), False)
    # sign plaque
    p.RR(250, 360, 830, 520, 30, (255, 244, 220), OL, 7)
    p.TX(540, 440, "ÇOCUK ATÖLYESİ", 52, (230, 100, 40))
    # plaque is placed in counter-local coords (cy0 offset)
    return img

WALL = build_wall()
COUNTER = build_counter()

# ---------- pizza data ----------
rnd = random.Random(7)
RX0, RY0 = 330, 118
SHREDS = []
for i in range(150):
    r = math.sqrt(rnd.random()) * 0.8
    a = rnd.random() * math.tau
    SHREDS.append((r * math.cos(a), r * math.sin(a), 14.2 + rnd.random() * 3.3,
                   rnd.random() * math.pi, rnd.randint(-12, 12)))
TOP = []
kinds = ["pep"] * 6 + ["oli"] * 6 + ["bas"] * 4
rnd.shuffle(kinds)
slots = []
for i in range(16):
    for _ in range(50):
        r = math.sqrt(rnd.random()) * 0.74
        a = rnd.random() * math.tau
        u, v = r * math.cos(a), r * math.sin(a)
        if all((u - a2) ** 2 + (v - b2) ** 2 > 0.07 for a2, b2 in slots):
            break
    slots.append((u, v))
    TOP.append((kinds[i], u, v, 19.3 + i * 0.275))
SPOTS = [(rnd.uniform(-.7, .7), rnd.uniform(-.7, .7), rnd.uniform(10, 20)) for _ in range(14)]
POP_TIMES = [x[3] for x in TOP]

def draw_toppings(p, cx, cy, s, t):
    for kind, u, v, t0 in TOP:
        if t < t0:
            continue
        q = cl((t - t0) / 0.35)
        x = cx + u * RX0 * s
        yt = cy + v * RY0 * s
        y = lerp(yt - 230 * s, yt, q * q)
        sc = s * (0.7 + 0.3 * back(q))
        if kind == "pep":
            p.E(x, y, 36 * sc, 18 * sc, (196, 48, 44), (120, 30, 30), 3)
            for dx, dy in ((-12, -3), (10, 4), (0, -7)):
                p.E(x + dx * sc, y + dy * sc, 5 * sc, 3 * sc, (150, 35, 35))
        elif kind == "oli":
            p.E(x, y, 22 * sc, 11 * sc, (50, 50, 60))
            p.E(x, y, 9 * sc, 4.5 * sc, (252, 226, 130))
        else:
            p.E(x, y, 28 * sc, 13 * sc, (70, 160, 70), (40, 110, 50), 3)
            p.LN([(x - 20 * sc, y), (x + 20 * sc, y)], 3, (40, 110, 50), False)

def draw_pizza(p, cx, cy, s, t, g, sp, cp, b, shreds=True, toppings=True):
    rx = lerp(85, RX0, g) * s
    ry = lerp(62, RY0, g) * s
    cyy = cy + lerp(-20, 0, g) * s
    p.E(cx, cyy + 20 * s, rx + 8, ry + 4, (196, 128, 76))  # shadow
    crust = mix((247, 226, 178), (224, 150, 72), b)
    p.E(cx, cyy, rx, ry, crust, OL, 5)
    if g < 1:
        p.E(cx - rx * .25, cyy - ry * .3, rx * .35, ry * .22, (255, 240, 205))
    if sp > 0:
        p.E(cx, cyy, rx * .88 * sp, ry * .86 * sp, (214, 64, 48))
    if cp > 0:
        p.E(cx, cyy, rx * .84 * cp, ry * .82 * cp, mix((252, 226, 130), (244, 188, 78), b))
    if b > 0:
        for u, v, r in SPOTS:
            p.E(cx + u * rx * .8, cyy + v * ry * .8, r * s * b, r * s * b * .5, (206, 120, 50))
    if shreds:
        for u, v, t0, ph, rot in SHREDS:
            if t < t0:
                continue
            q = cl((t - t0) / 0.5)
            x = cx + u * rx
            yt = cyy + v * ry
            y = lerp(cyy - 380 * s, yt, q * q)
            x += (1 - q) * 40 * math.sin(ph)
            a = math.radians(rot) + (1 - q) * 3
            L = 12 * s
            p.LN([(x - L * math.cos(a), y - L * math.sin(a) * .5), (x + L * math.cos(a), y + L * math.sin(a) * .5)],
                 7 * s, (255, 238, 170) if int(ph * 10) % 2 else (255, 224, 130))
    if toppings:
        draw_toppings(p, cx, cyy, s, t)

# ---------- character ----------
def draw_character(p, t, bob, open_mouth, worker=False):
    hy = 735 + bob
    # body
    p.RR(395, 880 + bob * .5, 685, 1250, 70, WHITE, OL, 6)
    p.PG([(470, 900 + bob * .5), (610, 900 + bob * .5), (640, 1250), (440, 1250)], (90, 150, 230) if worker else (255, 150, 90), OL, 5)  # apron
    p.RR(500, 860 + bob * .5, 580, 910 + bob * .5, 20, SKIN, OL, 5)  # neck
    for k in range(3):  # buttons
        p.E(540, 960 + k * 70 + bob * .5, 10, 10, (255, 230, 200), OL, 3)
    # head
    p.E(396, hy + 10, 26, 36, (140, 90, 60), OL, 4)
    p.E(684, hy + 10, 26, 36, (140, 90, 60), OL, 4)
    p.E(540, hy, 150, 145, SKIN, OL, 6)
    # hat
    if worker:
        pts = [(540 + 150 * math.cos(math.pi * i / 24), 650 + bob - 135 * math.sin(math.pi * i / 24)) for i in range(25)]
        p.PG(pts, (255, 205, 60), OL, 6)
        p.RR(380, 632 + bob, 700, 672 + bob, 16, (255, 190, 40), OL, 6)
        p.RR(515, 520 + bob, 565, 640 + bob, 12, (255, 225, 110))
    else:
        p.RR(410, 560 + bob, 670, 625 + bob, 18, WHITE, OL, 6)
        for cx, cyy, r in ((455, 535, 72), (540, 495, 90), (625, 535, 72)):
            p.E(cx, cyy + bob, r, r, WHITE, OL, 6)
        p.RR(412, 590 + bob, 668, 626 + bob, 14, WHITE)
        p.RR(410, 600 + bob, 670, 640 + bob, 14, (255, 120, 80), OL, 5)
    # face
    blink = (t % 3.3) < 0.12
    ry = 3 if blink else 22
    for ex in (488, 592):
        p.E(ex, hy - 5, 16, ry, OL)
        if not blink:
            p.E(ex + 5, hy - 12, 6, 7, WHITE)
    p.E(450, hy + 42, 28, 17, (255, 150, 150))
    p.E(630, hy + 42, 28, 17, (255, 150, 150))
    if open_mouth > 0:
        m = open_mouth
        p.E(540, hy + 58, 38, 14 + 24 * m, (150, 40, 50), OL, 4)
        p.E(540, hy + 58 + 18 * m, 20, 8 * m + 2, (255, 120, 130))
    else:
        pts = [(500 + 80 * u / 12, hy + 52 + 20 * math.sin(math.pi * u / 12)) for u in range(13)]
        p.LN(pts, 7, OL)

SH_L, SH_R = (430, 975), (650, 975)
def arm_pts(sh, hand, side):
    mx, my = (sh[0] + hand[0]) / 2, (sh[1] + hand[1]) / 2
    return [sh, (mx + side * 70, my + 35), hand]

def draw_arm(p, sh, hand, side):
    pts = arm_pts(sh, hand, side)
    p.LN(pts, 62, OL)
    p.LN(pts, 50, WHITE)

def draw_hand(p, hand):
    p.E(hand[0], hand[1], 40, 38, SKIN, OL, 5)

# ---------- scene helpers ----------
CAPS = [(0, 3.0, "Dev pizza nasıl yapılır?"), (3.0, 9.2, "1. Hamuru aç"), (9.2, 14.0, "2. Sosu sür"),
        (14.0, 19.0, "3. Bol peynir!"), (19.0, 24.0, "4. Malzemeleri ekle"), (24.0, 29.0, "5. Fırına!"),
        (29.0, 33.0, "Hazır! Dilimleyelim"), (33.0, 36.6, "Afiyet olsun!")]
CAP_COL = [(255, 120, 60), (80, 160, 230), (230, 80, 70), (240, 180, 40), (90, 180, 90), (230, 110, 40), (160, 100, 220), (230, 80, 120)]

def draw_caption(p, t):
    for i, (a, b, s) in enumerate(CAPS):
        if a <= t < b:
            q = back((t - a) / 0.35)
            size = 62 if len(s) < 20 else 54
            size = size * (0.6 + 0.4 * q)
            w = p.TW(s, size) + 90
            p.RR(540 - w / 2, 190, 540 + w / 2, 330, 70, WHITE, CAP_COL[i], 10)
            p.TX(540, 262, s, size, (70, 50, 45))
            break
    prog = t / DUR
    p.RR(100, 100, 980, 120, 10, (255, 255, 255))
    p.RR(100, 100, 100 + 880 * prog, 120, 10, (255, 120, 60))

def draw_oven(p, ox, t, b):
    x0, x1 = 130 + ox, 950 + ox
    p.RR(x0, 1010, x1, 1650, 50, (120, 130, 150), OL, 8)
    p.RR(x0 + 40, 1040, x1 - 40, 1130, 24, (50, 55, 70), OL, 5)
    sec = max(1, 3 - int((t - 24.7)))
    txt = str(sec) if t < 27.7 else "OK"
    p.TX((x0 + x1) / 2, 1085, txt, 64, (120, 255, 150))
    p.RR(x0 + 50, 1160, x1 - 50, 1560, 36, (255, 170, 70), OL, 8)
    glow = 0.5 + 0.5 * math.sin(t * 8)
    p.RR(x0 + 70, 1180, x1 - 70, 1540, 28, mix((255, 120, 40), (255, 190, 80), glow), None)
    draw_pizza(p, (x0 + x1) / 2, 1390, 0.62, 99, 1, 1, 1, b)
    for k in range(4):
        p.E(x0 + 100 + k * 200, 1605, 24, 24, (230, 230, 240), OL, 5)

def frame(t):
    img = WALL.copy()
    p = Pen(img)
    bob = 5 * math.sin(2 * math.pi * 1.1 * t)
    om = 0
    if t > 31.3:
        om = 0.5 + 0.5 * math.sin(t * 5)
    elif t < 3:
        om = 0.3
    draw_character(p, t, bob, om)
    img.paste(COUNTER, (0, 1100 * S))
    p = Pen(img)
    # plaque / end card
    if t >= 33.4:
        p.d.rectangle([200 * S, 1430 * S, 880 * S, 1740 * S], fill=(190, 126, 74))
        p.RR(150, 1440, 930, 1560, 50, (255, 120, 60), OL, 7)
        p.TX(540, 1500, "Yarın: Bisiklet tamiri!", 52, WHITE)
        p.RR(300, 1600, 780, 1720, 50, (230, 50, 60), OL, 7)
        p.TX(540, 1660, "Takip et!", 56, WHITE)
        p.PG([(240, 1632), (270, 1660), (240, 1688)], WHITE)
    lh, rh = (400, 1135), (680, 1135)
    prop = None
    # --- scenes ---
    g = sp = cp = b = 0.0
    show_pizza = False
    if t < 3.0:
        g = 0
        show_pizza = t >= 0.3
        k = back((t - 0.3) / 0.4)
        # ball
        if show_pizza:
            p.E(540, 1195 + 20, 85 * k, 62 * k, (246, 224, 176), OL, 5)
            p.E(510, 1195, 28 * k, 16 * k, (255, 240, 205))
        show_pizza = False
        rh = (790 + 25 * math.sin(2 * math.pi * 2.3 * t), 760 + 40 * math.sin(2 * math.pi * 2.3 * t))
    elif t < 9.2:
        g = so((t - 3.5) / 5.0)
        show_pizza = True
        tt = t - 3.0
        piny = 1215 + 75 * math.sin(2 * math.pi * 1.1 * tt)
        if tt < 0.5:
            piny = lerp(1000, piny, so(tt / 0.5))
        lh, rh = (305, piny), (775, piny)
        prop = ("pin", piny)
    elif t < 14.0:
        g, show_pizza = 1, True
        sp = so((t - 9.5) / 3.8)
        tt = t - 9.3
        r = 0.2 + 0.8 * sp
        w = 2 * math.pi * 1.0 * tt
        rh = (540 + 230 * r * math.cos(w), 1100 + 50 * r * math.sin(w))
        prop = ("ladle", rh)
    elif t < 19.0:
        g, sp, show_pizza = 1, 1, True
        cp = so((t - 15.0) / 3.5)
        rh = (540 + 250 * math.sin(2 * math.pi * 0.9 * (t - 14.0)), 960 + 15 * math.sin(t * 9))
    elif t < 24.0:
        g, sp, cp, show_pizza = 1, 1, 1, True
        cur = None
        for kind, u, v, t0 in TOP:
            if t >= t0 - 0.05:
                cur = (u, v)
        if cur:
            rh = (540 + cur[0] * RX0 + 20, 1235 + cur[1] * RY0 - 250)
        else:
            rh = (700, 980)
    elif t < 29.0:
        g, sp, cp, show_pizza = 1, 1, 1, True
        b = so((t - 24.7) / 3.0) if t < 28.5 else 1
    else:
        g, sp, cp, b, show_pizza = 1, 1, 1, 1, True

    if show_pizza:
        s = 1.0
        if 28.4 <= t < 29.4:
            s = 1 + 0.08 * math.sin(math.pi * (t - 28.4))
        cx = 540
        draw_pizza(p, cx, 1235, s, t, g, sp, cp, b)
        if t >= 28.6 and t < 33.4:
            for k in range(4):  # steam
                pts = []
                for i in range(14):
                    yy = 1130 - i * 26
                    pts.append((cx - 180 + k * 120 + 14 * math.sin(i * .8 + t * 4 + k), yy))
                p.LN(pts, 8, (255, 255, 255))
        if t >= 28.9:
            # cuts
            for i, ang in enumerate((0, 60, 120)):
                q = so((t - 29.0 - i * 0.5) / 0.5)
                if q <= 0:
                    continue
                a = math.radians(ang)
                dx, dy = math.cos(a) * RX0 * q, math.sin(a) * RY0 * q
                p.LN([(540 - dx, 1235 - dy), (540 + dx, 1235 + dy)], 5, (140, 80, 40), False)
            if t >= 30.6:
                l = so((t - 30.6) / 1.6)
                th1, th2 = math.radians(60), math.radians(120)
                def pt(th, k=1.0): return (540 + RX0 * k * math.cos(th), 1235 + RY0 * k * math.sin(th))
                ths = [th1 + (th2 - th1) * i / 10 for i in range(11)]
                wedge = [(540, 1235)] + [pt(th) for th in ths]
                p.PG(wedge, (236, 184, 120))
                p.LN([pt(th1, 1.0), (540, 1235), pt(th2, 1.0)], 4, (190, 128, 76), False)
                off = (0, -330 * l)
                def mv(pts, k=1.0): return [(540 + (x - 540) * k + off[0], 1235 + (y - 1235) * k + off[1]) for x, y in pts]
                p.PG(mv(wedge), (224, 150, 72), OL, 5)
                p.PG(mv(wedge, 0.9), (244, 188, 78))
                for dx2, dy2, r in ((-22, 70, 18), (24, 90, 18), (0, 45, 14)):
                    p.E(540 + dx2 + off[0], 1235 + dy2 + off[1] , r, r * .5, (196, 48, 44))
                if l < 0.97 and l > 0.05:
                    for side, kk in ((th1, 0.9), (th2, 0.9), (math.radians(90), 0.7)):
                        sx, sy = pt(side, kk)
                        ex, ey = sx + off[0], sy + off[1]
                        mxx, myy = (sx + ex) / 2, (sy + ey) / 2 + 40 * l
                        p.LN([(sx, sy), (mxx, myy), (ex, ey)], 9 * (1 - 0.6 * l), (252, 226, 130))
                rh = (540, 1235 + off[1] + 70)
                lh = (320, 1020 + 20 * math.sin(t * 4))
        if t >= 24.0 and t < 28.7:
            pass

    # arms (drawn after counter items)
    draw_arm(p, SH_L, lh, -1)
    draw_arm(p, SH_R, rh, 1)
    if prop and prop[0] == "pin":
        py = prop[1]
        p.RR(310, py - 26, 770, py + 26, 26, (214, 164, 108), OL, 5)
        p.RR(250, py - 18, 330, py + 18, 16, (170, 110, 70), OL, 5)
        p.RR(750, py - 18, 830, py + 18, 16, (170, 110, 70), OL, 5)
        for k in range(5):  # flour
            fx = 540 + 220 * math.sin(t * 3 + k * 1.7)
            fy = 1160 - 20 * ((t * 2 + k * .37) % 1) * 3
            p.E(fx, fy, 7, 7, (255, 255, 255))
    if prop and prop[0] == "ladle":
        hx, hy2 = prop[1]
        p.LN([(hx, hy2), (hx + 12, hy2 + 95)], 16, (160, 165, 180))
        p.E(hx + 14, hy2 + 105, 40, 24, (170, 175, 190), OL, 4)
        p.E(hx + 14, hy2 + 105, 30, 15, (214, 64, 48))
    draw_hand(p, lh)
    draw_hand(p, rh)

    # oven overlay
    if 24.0 <= t < 28.8:
        if t < 24.7:
            ox = lerp(1000, 0, so((t - 24.0) / 0.7))
        elif t < 28.1:
            ox = 0
        else:
            ox = lerp(0, 1000, so((t - 28.1) / 0.7))
        draw_oven(p, ox, t, b)

    # sparkles
    if t >= 31.5:
        for i, (sx, sy, ph) in enumerate(((190, 900, 0), (880, 860, 1), (150, 1300, 2), (930, 1300, 3), (300, 560, 4), (790, 600, 5))):
            sc = max(0, math.sin((t - 31.5) * 5 + ph * 1.3))
            star(p, sx, sy, 38 * sc, (255, 220, 70))
    draw_caption(p, t)
    return img.resize((W, H), Image.LANCZOS)

