import math
from engine import *
from foods import face, win, REST_L, REST_R, dp, SURF

TOOLS = {}

def tool(p, kind, hx, hy, wx, wy, t):
    """draw a tool held at hand (hx,hy) working on (wx,wy)"""
    if kind == "wrench":
        p.LN([(hx, hy), (wx + 18, wy - 18)], 20, (150, 155, 170))
        p.E(wx + 14, wy - 14, 30, 30, (150, 155, 170), OL, 4); p.E(wx + 8, wy - 8, 12, 12, (255, 220, 190))
    elif kind == "screwdriver":
        p.LN([(hx, hy), (hx - (hx - wx) * .55, hy - (hy - wy) * .55)], 26, (240, 140, 50))
        p.LN([(hx - (hx - wx) * .55, hy - (hy - wy) * .55), (wx + 6, wy - 6)], 9, (200, 205, 215))
    elif kind == "needle":
        p.LN([(hx, hy), (wx + 6, wy - 4)], 7, (225, 230, 240))
        p.LN([(hx, hy), (hx + 40, hy + 80), (wx + 110, wy + 60), (wx + 30, wy + 10)], 4, (230, 60, 90), False)
    elif kind == "pump":
        p.LN([(hx, hy - 60), (hx, hy + 70)], 36, (230, 70, 70))
        p.LN([(hx, hy - 90 + 25 * math.sin(t * 9)), (hx, hy - 50)], 10, (90, 90, 100))
        p.LN([(hx, hy + 70), (hx - 40, hy + 150), (wx, wy)], 9, (60, 60, 70), False)
    elif kind == "glue":
        p.RR(hx - 22, hy - 55, hx + 22, hy + 40, 12, WHITE, OL, 4)
        p.PG([(hx - 14, hy + 40), (hx + 14, hy + 40), (hx + 4, hy + 80)], (255, 160, 60), OL, 3)
        p.LN([(hx + 4, hy + 80), (wx, wy)], 6, (255, 250, 230))

def sparks(p, wx, wy, t, n=4):
    for i in range(n):
        a = t * 9 + i * 1.6
        star(p, wx + 40 * math.cos(a), wy - 30 + 30 * math.sin(a * 1.3), 14 + 8 * math.sin(a), (255, 220, 70))

# ---------- objects: (p, cx, by, f, t, a) -> work, face ----------
def d_bike(p, cx, by, f, t, a):
    R = 150; ry = R - 60 * (1 - f); cy = by - ry
    y0 = by - 2 * R - 40
    p.LN([(cx, cy), (cx - 40, y0)], 16, (210, 60, 70)); p.LN([(cx - 130, y0), (cx + 40, y0)], 16, (210, 60, 70))
    p.E(cx, cy, R, ry, (60, 60, 70), OL, 6)
    p.E(cx, cy, R - 30, max(ry - 30, 10), (235, 235, 240), OL, 4)
    for k in range(8):
        an = k * math.pi / 4
        p.LN([(cx, cy), (cx + (R - 34) * math.cos(an), cy + (ry - 34) * math.sin(an))], 3, (160, 160, 170), False)
    p.E(cx, cy, 24, 24, (255, 200, 60), OL, 4)
    if f < .45:
        nx, ny = cx - R * .62, cy - ry * .72
        p.LN([(nx, ny), (nx + 28, ny - 30)], 10, (150, 150, 160)); p.E(nx + 30, ny - 33, 14, 14, (120, 120, 130), OL, 3)
    return (cx + 120, cy + ry * .6), (cx, cy, 1.0, (235, 235, 240))

def d_robot(p, cx, by, f, t, a):
    for dx in (-60, 60): p.RR(cx + dx - 28, by - 120, cx + dx + 28, by, 10, (150, 160, 180), OL, 5)
    p.RR(cx - 110, by - 310, cx + 110, by - 110, 24, (120, 170, 230), OL, 6)
    p.RR(cx - 60, by - 260, cx + 60, by - 180, 14, (240, 245, 255), OL, 4)
    for k in range(3): p.E(cx - 30 + k * 30, by - 220, 8, 8, (255, 120, 100) if f < .7 else (110, 220, 130))
    hy = by - 420 + (1 - f) * 16
    p.RR(cx - 85, hy - 60, cx + 85, hy + 50, 22, (150, 190, 240), OL, 6)
    eye = (120, 120, 130) if f < .6 else (80, 230, 255)
    for dx in (-35, 35): p.E(cx + dx, hy - 5, 18, 18, eye, OL, 4)
    bend = (1 - f) * 60
    p.LN([(cx, hy - 60), (cx + bend * .3, hy - 95), (cx + bend, hy - 110)], 8, OL)
    p.E(cx + bend, hy - 118, 14, 14, (255, 90, 90), OL, 4)
    p.LN([(cx + 110, by - 280), (cx + 190, by - 200 + 20 * math.sin(t * 8) * a)], 26, (150, 190, 240))
    sx, sy = cx - 110, by - 280
    A = (lerp(cx - 420, sx, f), lerp(by - 40, sy, f)); B = (lerp(cx - 290, cx - 190, f), lerp(by - 32, by - 195, f))
    p.LN([A, B], 26, (150, 190, 240))
    if f < .8:
        pts = [(sx - 10, sy), (sx - 25, sy + 18), (sx - 8, sy + 30), (sx - 28, sy + 46)]
        p.LN(pts, 4, (255, 220, 70), False)
    return (sx - 25, sy + 25), None

def d_cup(p, cx, by, f, t, a):
    gap = (1 - f) * 70; tp = by - 230; wt, wb = 150, 105
    p.PG([(cx - wt - gap, tp), (cx - gap, tp), (cx - gap, by), (cx - wb - gap, by)], (245, 245, 252), OL, 5)
    p.PG([(cx + gap, tp), (cx + wt + gap, tp), (cx + wb + gap, by), (cx + gap, by)], (245, 245, 252), OL, 5)
    hx = cx + wt + gap + 22
    p.E(hx + 20, by - 125, 55, 62, (245, 245, 252), OL, 5); p.E(hx + 20, by - 125, 28, 34, SURF, OL, 4)
    p.E(cx - gap * .5 + gap * .5, tp, wt + gap * .9, 30, (225, 225, 238), OL, 4)
    if f > .25:
        p.LN([(cx, tp), (cx - 14, by - 150), (cx + 12, by - 95), (cx, by)], 12 * f, (255, 200, 40))
    if f < .75:
        k = 1 - f / .75
        sx, sy = lerp(cx, cx + 270, k), lerp(by - 100, by - 18, k)
        p.PG([(sx - 40 * k - 10, sy + 14), (sx + 34 * k + 10, sy + 14), (sx, sy - 34 * k - 8)], (245, 245, 252), OL, 4)
    if a > 0:
        for i in range(3):
            pts = [(cx - 60 + i * 60 + 12 * math.sin(j * .8 + t * 5 + i), tp - 40 - j * 26) for j in range(8)]
            p.LN(pts, 8, (255, 210, 70))
    return (cx + 8, by - 150), (cx, by - 110, 1.15, None)

def d_teddy(p, cx, by, f, t, a):
    br, br2 = (196, 140, 90), (230, 190, 150)
    for dx in (-80, 80): p.E(cx + dx, by - 30, 50, 38, br, OL, 5)
    p.E(cx, by - 170, 125, 150, br, OL, 6); p.E(cx, by - 150, 75, 90, br2)
    p.E(cx + 135, by - 205, 38, 70, br, OL, 5)
    for dx in (-90, 90):
        p.E(cx + dx, by - 445, 38, 38, br, OL, 5); p.E(cx + dx, by - 445, 20, 20, br2)
    p.E(cx, by - 370, 105, 95, br, OL, 6); p.E(cx, by - 345, 50, 36, br2)
    p.E(cx, by - 358, 14, 10, OL)
    for dx in (-40, 40): p.E(cx + dx, by - 395, 10, 12, OL)
    p.LN([(cx - 18, by - 328), (cx, by - 318), (cx + 18, by - 328)], 5, OL)
    ax, ay = lerp(cx - 255, cx - 135, f), lerp(by - 60, by - 205, f)
    if f < 1: p.LN([(cx - 105, by - 245), (ax, ay)], 4, (230, 60, 90), False)
    p.E(ax, ay, 38, 70, br, OL, 5)
    if f < .55:
        for dx, dy in ((-40, -215), (-20, -190), (-52, -180)):
            p.E(cx + dx, by + dy, 22, 20, WHITE, (210, 210, 210), 3)
    else:
        for k in range(int(8 * (f - .5) * 2)):
            x = cx - 70 + k * 15
            p.LN([(x - 6, by - 215), (x + 6, by - 185)], 4, (230, 60, 90), False); p.LN([(x + 6, by - 215), (x - 6, by - 185)], 4, (230, 60, 90), False)
    return (cx - 30, by - 200), None

OBJECTS = {"bike": d_bike, "robot": d_robot, "cup": d_cup, "teddy": d_teddy}

def scene(p, t, topic):
    spec = topic["spec"]
    f = so((t - 8.5) / 16.5) if t > 8.5 else 0.0
    if t >= 25: f = 1.0
    alive = so((t - 25.0) / 1.0) if t > 25 else 0.0
    hop = 0
    if t >= 29.4: hop = 36 * abs(math.sin((t - 29.4) * 4.5))
    elif t >= 25: hop = 8 * abs(math.sin((t - 25) * 5)) * alive
    cx, by = 540, 1300
    lh, rh, prop = REST_L, REST_R, None
    if t < 3.0:
        k = back((t - .3) / .5) if t > .3 else 0
        by_eff = by + (1 - k) * 700
        OBJECTS[spec["obj"]](p, cx, by_eff, 0.0, t, 0)
        rh = (790 + 25 * math.sin(2 * math.pi * 2.3 * t), 760 + 40 * math.sin(2 * math.pi * 2.3 * t))
        return lh, rh, None, None
    work, fc = OBJECTS[spec["obj"]](p, cx, by - hop, f, t, alive if t >= 25 else 0)
    if t >= 29.0 and fc:
        face(p, fc[0], fc[1] - hop, fc[2], t, fc[3])
    if 3.0 <= t < 8.5:
        wx, wy = work
        pulse = 1 + .12 * math.sin(t * 8)
        p.TX(wx, wy - 120, "!", int(120 * pulse), (230, 50, 50))
        rh = (wx + 120, wy - 120)
        prop = ("mag", (wx, wy))
    elif 8.5 <= t < 25:
        wx, wy = work
        hx, hy = wx + 90 + 10 * math.sin(t * 11), wy - 80 + 10 * math.cos(t * 11)
        rh = (hx, hy)
        k = spec["tools"][min(2, int((t - 8.5) / 5.5))]
        prop = ("tool", k, (hx, hy), (wx, wy))
    if 20.0 <= t < 25.0:
        for i in range(3):
            sc = max(0, math.sin(t * 5 + i * 2.1))
            star(p, cx - 230 + i * 230, by - 330 + 60 * math.sin(i), 36 * sc, (255, 240, 130))
    return lh, rh, prop, None

def events(topic):
    ev = [(0.5, "thump")]
    t = 8.7
    while t < 25: ev.append((t, "tool")); t += .55
    ev += [(25.2, "sparkle"), (29.3, "sparkle"), (33.4, "sparkle")]
    return ev
