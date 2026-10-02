import math, random
from engine import *

T0, STEP = 3.0, 5.5
REST_L, REST_R = (400, 1135), (680, 1135)
SURF = (236, 184, 120)

def win(i): return T0 + STEP * i, T0 + STEP * (i + 1)

# ---------- small drawing helpers ----------
def dp(p, kind, x, y, sc, col):
    if kind == "pep":
        p.E(x, y, 36 * sc, 18 * sc, (196, 48, 44), (120, 30, 30), 3)
        for dx, dy in ((-12, -3), (10, 4), (0, -7)):
            p.E(x + dx * sc, y + dy * sc, 5 * sc, 3 * sc, (150, 35, 35))
    elif kind == "olive":
        p.E(x, y, 22 * sc, 11 * sc, (50, 50, 60)); p.E(x, y, 9 * sc, 4.5 * sc, (252, 226, 130))
    elif kind == "leaf":
        p.E(x, y, 28 * sc, 13 * sc, (70, 160, 70), (40, 110, 50), 3)
        p.LN([(x - 20 * sc, y), (x + 20 * sc, y)], 3, (40, 110, 50), False)
    elif kind == "chip":
        p.E(x, y, 17 * sc, 9 * sc, col, mix(col, (0, 0, 0), .4), 2)
    elif kind == "berry":
        p.E(x, y, 26 * sc, 16 * sc, (225, 45, 70), (140, 20, 40), 3); p.E(x, y - 11 * sc, 13 * sc, 5 * sc, (70, 160, 70))
    elif kind == "heart":
        p.E(x - 10 * sc, y - 6 * sc, 12 * sc, 11 * sc, col); p.E(x + 10 * sc, y - 6 * sc, 12 * sc, 11 * sc, col)
        p.PG([(x - 21 * sc, y - 1 * sc), (x + 21 * sc, y - 1 * sc), (x, y + 22 * sc)], col)
    elif kind == "dot":
        p.E(x, y, 9 * sc, 6 * sc, col)
    elif kind == "slice":
        p.E(x, y, 32 * sc, 16 * sc, col, mix(col, (0, 0, 0), .35), 3); p.E(x, y, 20 * sc, 9 * sc, mix(col, (255, 255, 255), .4))
    elif kind == "sprinkle":
        p.LN([(x - 8 * sc, y - 3 * sc), (x + 8 * sc, y + 3 * sc)], 6 * sc, col)

def face(p, x, y, sc, t, back=None):
    if back:
        p.E(x, y, 100 * sc, 70 * sc, back)
    blink = (t % 2.7) < 0.12
    for dx in (-42, 42):
        p.E(x + dx * sc, y - 8 * sc, 13 * sc, (3 if blink else 19) * sc, OL)
        if not blink:
            p.E(x + (dx + 4) * sc, y - 15 * sc, 5 * sc, 6 * sc, WHITE)
    p.E(x - 70 * sc, y + 18 * sc, 20 * sc, 12 * sc, (255, 140, 150))
    p.E(x + 70 * sc, y + 18 * sc, 20 * sc, 12 * sc, (255, 140, 150))
    pts = [(x - 24 * sc + 48 * sc * u / 10, y + 14 * sc + 14 * sc * math.sin(math.pi * u / 10)) for u in range(11)]
    p.LN(pts, 6 * sc, OL)

def fx(p, kind, t, t0=29.4):
    if t < t0:
        return
    k = t - t0
    r = random.Random(5)
    if kind == "confetti":
        cols = [(255, 90, 90), (90, 170, 255), (255, 210, 60), (110, 210, 120), (200, 120, 230)]
        for i in range(70):
            x = r.randint(60, 1020); y0 = r.randint(-600, 0); sp = r.uniform(300, 520)
            y = (y0 + k * sp) % 2100 - 150
            if y > 1100: continue
            p.RR(x, y, x + 16, y + 26, 4, cols[i % 5])
    elif kind == "hearts":
        for i in range(9):
            x = 200 + (i * 97) % 700 + 25 * math.sin(k * 2 + i)
            y = 1150 - ((k * 140 + i * 130) % 900)
            dp(p, "heart", x, y, 1.1, (255, 110, 150))
    elif kind == "stars":
        for i in range(10):
            x = 120 + (i * 211) % 840; y = 520 + (i * 137) % 700
            sc = max(0, math.sin(k * 5 + i * 1.3))
            star(p, x, y, 40 * sc, (255, 220, 70))
    elif kind == "butterflies":
        for i in range(3):
            x = 540 + 330 * math.sin(k * 1.3 + i * 2.1); y = 800 + 140 * math.sin(k * 2 + i) + i * 60
            fl = abs(math.sin(k * 14 + i))
            col = [(255, 150, 200), (150, 200, 255), (255, 200, 90)][i]
            p.E(x - 22 * fl, y, 26 * fl + 4, 20, col, OL, 3); p.E(x + 22 * fl, y, 26 * fl + 4, 20, col, OL, 3)
            p.E(x, y, 5, 16, OL)
    elif kind == "bubbles":
        for i in range(14):
            x = 100 + (i * 173) % 880 + 20 * math.sin(k * 3 + i); y = 1250 - ((k * 180 + i * 150) % 1100)
            p.E(x, y, 22 + i % 3 * 8, 22 + i % 3 * 8, (225, 245, 255), (120, 190, 230), 3)

# ---------- ROUND (pizza, cookie, toast, waffle, donut, pie) ----------
def make_parts(spec, seed):
    rng = random.Random(seed)
    res = []
    for i, op in enumerate(spec["ops"]):
        a, b = win(i + 1)
        parts = []
        if op["op"] == "scatter":
            n = op["n"]
            for k in range(n):
                for _ in range(60):
                    r = math.sqrt(rng.random()) * 0.8
                    ang = rng.random() * math.tau
                    u, v = r * math.cos(ang), r * math.sin(ang)
                    if r >= op.get("rmin", 0) and all((u - a2) ** 2 + (v - b2) ** 2 > op.get("gap", 0.0) for a2, b2, *_ in parts):
                        break
                col = rng.choice(op["colors"])
                parts.append((u, v, a + 0.3 + (b - a - 1.6) * k / max(n - 1, 1), col))
        res.append(parts)
    return res

def region(spec, g, s, cx, cy):
    st = spec["style"]
    if st == "rect":
        hw, hh = lerp(70, 290, g) * s, lerp(60, 125, g) * s
        return ("rect", cx, cy, hw, hh)
    rx, ry = lerp(85, 330, g) * s, lerp(62, 118, g) * s
    return ("ell", cx, cy + lerp(-20, 0, g) * s, rx, ry)

def draw_round(p, spec, parts, t, cx, cy, s, b):
    g = so((t - 3.3) / 4.5)
    kind, cx, cy, rx, ry = region(spec, g, s, cx, cy)
    crust = mix(spec["base"], spec["baked"], b)
    if kind == "rect":
        p.RR(cx - rx - 8, cy - ry + 20, cx + rx + 8, cy + ry + 20, 40, (196, 128, 76))
        p.RR(cx - rx, cy - ry, cx + rx, cy + ry, 40 * s, crust, OL, 5)
        if spec.get("grid") and g > .9:
            for k in range(-3, 4):
                p.LN([(cx + k * rx / 3.6, cy - ry + 12), (cx + k * rx / 3.6, cy + ry - 12)], 4, mix(crust, (0, 0, 0), .25), False)
            for k in range(-1, 2):
                p.LN([(cx - rx + 12, cy + k * ry / 1.8), (cx + rx - 12, cy + k * ry / 1.8)], 4, mix(crust, (0, 0, 0), .25), False)
    else:
        p.E(cx, cy + 20 * s, rx + 8, ry + 4, (196, 128, 76))
        p.E(cx, cy, rx, ry, crust, OL, 5)
    for i, op in enumerate(spec["ops"]):
        a, bb = win(i + 1)
        col = mix(op.get("color", (255, 255, 255)), op.get("baked", op.get("color", (255, 255, 255))), b)
        if op["op"] == "spread":
            sp = so((t - (a + .3)) / 3.8)
            if sp > 0:
                if kind == "rect":
                    p.RR(cx - rx * .9 * sp, cy - ry * .85 * sp, cx + rx * .9 * sp, cy + ry * .85 * sp, 26, col)
                else:
                    p.E(cx, cy, rx * .9 * sp, ry * .88 * sp, col)
        elif op["op"] == "lattice":
            q = so((t - (a + .3)) / 4.0)
            for k in range(-3, 4):
                u = k / 3.6
                vv = math.sqrt(max(0, 1 - u * u)) * .8 * q
                p.LN([(cx + u * rx * .9, cy - vv * ry), (cx + u * rx * .9, cy + vv * ry)], 16 * s, mix(spec["base"], (255, 235, 190), .5))
            for k in range(-3, 4):
                v = k / 3.6 * .8
                uu = math.sqrt(max(0, 1 - v * v)) * .9 * q
                p.LN([(cx - uu * rx, cy + v * ry), (cx + uu * rx, cy + v * ry)], 12 * s, mix(spec["base"], (255, 220, 160), .4))
        if spec.get("hole") and i == spec["hole"] - 1 and g > .9:
            p.E(cx, cy, rx * .27, ry * .27, SURF, mix(spec["base"], (0, 0, 0), .4), 4)
        if op["op"] == "scatter":
            for u, v, t0, pc in parts[i]:
                if t < t0:
                    continue
                q = cl((t - t0) / 0.38)
                x = cx + u * rx * (1.05 if kind == "rect" else 1.0)
                yt = cy + v * ry
                y = lerp(yt - 280 * s, yt, q * q)
                dp(p, op["kind"], x, y, s * op.get("sc", 1.0) * (0.75 + 0.25 * back(q)), pc)
    if spec.get("hole") and spec.get("hole") == 0:
        pass
    return cx, cy, rx, ry

def round_hands(spec, parts, t):
    lh, rh, prop = REST_L, REST_R, None
    if t < 3.0:
        return lh, (790 + 25 * math.sin(2 * math.pi * 2.3 * t), 760 + 40 * math.sin(2 * math.pi * 2.3 * t)), None
    if t < 8.5:
        tt = t - 3.0
        py = 1215 + 75 * math.sin(2 * math.pi * 1.1 * tt)
        if tt < 0.5: py = lerp(1000, py, so(tt / 0.5))
        return (305, py), (775, py), ("pin", py)
    for i, op in enumerate(spec["ops"]):
        a, b = win(i + 1)
        if a <= t < b:
            if op["op"] == "spread" or op["op"] == "lattice":
                w = 2 * math.pi * (t - a)
                return lh, (540 + 230 * math.cos(w), 1100 + 50 * math.sin(w)), ("ladle", None)
            pr = parts[i]
            if len(pr) > 40:
                return lh, (540 + 250 * math.sin(2 * math.pi * .9 * (t - a)), 960 + 15 * math.sin(t * 9)), None
            cur = None
            for u, v, t0, pc in pr:
                if t >= t0 - .05: cur = (u, v)
            if cur: return lh, (540 + cur[0] * 330 + 20, 1235 + cur[1] * 118 - 250), None
            return lh, (700, 980), None
    return lh, rh, None

def draw_oven(p, ox, t, b, item):
    x0, x1 = 130 + ox, 950 + ox
    p.RR(x0, 1010, x1, 1650, 50, (120, 130, 150), OL, 8)
    p.RR(x0 + 40, 1040, x1 - 40, 1130, 24, (50, 55, 70), OL, 5)
    sec = max(1, 3 - int(max(0, t - 25.7)))
    p.TX((x0 + x1) / 2, 1085, str(sec) if t < 28.2 else "OK", 64, (120, 255, 150))
    p.RR(x0 + 50, 1160, x1 - 50, 1560, 36, (255, 170, 70), OL, 8)
    glow = 0.5 + 0.5 * math.sin(t * 8)
    p.RR(x0 + 70, 1180, x1 - 70, 1540, 28, mix((255, 120, 40), (255, 190, 80), glow))
    item((x0 + x1) / 2, 1390, 0.62)
    for k in range(4):
        p.E(x0 + 100 + k * 200, 1605, 24, 24, (230, 230, 240), OL, 5)

def round_scene(p, t, topic):
    spec = topic["spec"]
    parts = make_parts(spec, topic["day"])
    topic["_parts"] = parts
    b = so((t - 25.7) / 2.5) if t > 25.7 else 0
    if t >= 28.5: b = 1
    s = 1.0
    if 29.0 <= t < 29.8: s = 1 + 0.09 * math.sin(math.pi * (t - 29.0) / 0.8)
    show = t >= 0.3
    if t < 3.0:
        k = back((t - 0.3) / 0.4)
        if show:
            p.E(540, 1215, 85 * k, 62 * k, mix(spec["base"], (255, 255, 255), .15), OL, 5)
    else:
        if not (25.0 <= t < 28.5):
            cx, cy, rx, ry = draw_round(p, spec, parts, t, 540, 1235, s, b)
            if t >= 29.0:
                face(p, 540, 1228, 1.35, t)
        else:
            draw_round(p, spec, parts, t, 540, 1235, 1.0, 0)
    lh, rh, prop = round_hands(spec, parts, t)
    over = None
    if 25.0 <= t < 28.9:
        if t < 25.7: ox = lerp(1000, 0, so((t - 25.0) / .7))
        elif t < 28.2: ox = 0
        else: ox = lerp(0, 1000, so((t - 28.2) / .7))
        def item(cx, cy, s2):
            draw_round(p, spec, parts, 99, cx, cy, s2, b)
        over = lambda: draw_oven(p, ox, t, b, item)
    return lh, rh, prop, over

# ---------- STACK (burger, cake, ice cream, pancake, cupcake) ----------
def layer_draw(p, L, cx, yb, t):
    sh, col, w, h = L["shape"], L["color"], L.get("w", 200), L["h"]
    dark, light = mix(col, (0, 0, 0), .25), mix(col, (255, 255, 255), .3)
    ry = w * .2
    if sh == "slab":
        p.E(cx, yb, w, ry, dark, OL, 4); p.RR(cx - w, yb - h, cx + w, yb, 0, col)
        p.LN([(cx - w, yb - h), (cx - w, yb)], 4, OL, False); p.LN([(cx + w, yb - h), (cx + w, yb)], 4, OL, False)
        p.E(cx, yb - h, w, ry, light, OL, 4)
    elif sh == "dome":
        p.E(cx, yb, w, ry, dark, OL, 4)
        pts = [(cx + w * math.cos(a), yb - h * math.sin(a)) for a in [math.pi * i / 24 for i in range(25)]]
        p.PG(pts, col, OL, 5)
        for dx, dy in L.get("seeds", []):
            p.E(cx + dx, yb - h * .6 + dy, 9, 5, (255, 244, 210))
    elif sh == "wavy":
        pts = [(cx - w + k * (2 * w / 24), yb - h / 2 + 7 * math.sin(k * 1.3)) for k in range(25)]
        p.LN(pts, h, col)
    elif sh == "ball":
        r = h / 2
        p.E(cx, yb - r, r, r, col, OL, 4); p.E(cx - r * .35, yb - r * 1.35, r * .25, r * .18, light)
        if L.get("drip"):
            p.E(cx, yb - r * 1.45, r * .75, r * .32, L["drip"])
            for dx in (-.4, .1, .45):
                p.RR(cx + dx * r - 8, yb - r * 1.45, cx + dx * r + 8, yb - r * (1.0 - dx * .2), 8, L["drip"])
    elif sh == "cup":
        p.PG([(cx - w, yb - h), (cx + w, yb - h), (cx + w * .72, yb), (cx - w * .72, yb)], col, OL, 5)
        for k in range(-3, 4):
            p.LN([(cx + k * w / 3.6, yb - h + 6), (cx + k * w / 3.6 * .72, yb - 6)], 4, dark, False)
    elif sh == "swirl":
        for i in range(3):
            ww = w * (1 - .28 * i)
            p.E(cx, yb - h / 3 * (i + .5), ww, h / 3 * .75, col if i % 2 == 0 else light, OL, 4)
        p.E(cx, yb - h + 8, w * .1, w * .1, col, OL, 3)
    elif sh == "candles":
        for dx in (-80, 0, 80):
            p.RR(cx + dx - 9, yb - h, cx + dx + 9, yb, 4, (255, 120, 150) if dx else (120, 190, 255), OL, 3)
            fl = 1 + .2 * math.sin(t * 12 + dx)
            p.E(cx + dx, yb - h - 20, 10, 18 * fl, (255, 200, 60)); p.E(cx + dx, yb - h - 16, 5, 9 * fl, (255, 250, 220))
    elif sh == "heart":
        dp(p, "heart", cx, yb - h / 2, w / 25, col)
    elif sh == "sprinkles":
        rr = random.Random(3)
        for _ in range(26):
            u = rr.uniform(-.85, .85); v = rr.uniform(-.6, .6)
            dp(p, "sprinkle", cx + u * w, yb + v * w * .2, 1.2, rr.choice(L["cols"]))
    elif sh == "syrup":
        p.E(cx, yb - 4, w, w * .2, col)
        for dx in (-.8, -.35, .15, .55, .85):
            p.RR(cx + dx * w - 11, yb - 4, cx + dx * w + 11, yb + 40 + 30 * abs(math.sin(dx * 9)), 11, col)

def stack_layout(spec):
    ys, y = [], 1335
    for L in spec["layers"]:
        ys.append(y); y -= L["h"]
    return ys

def stack_scene(p, t, topic):
    spec = topic["spec"]
    ys = stack_layout(spec)
    lh, rh, prop = REST_L, REST_R, None
    if t < 3.0:
        rh = (790 + 25 * math.sin(2 * math.pi * 2.3 * t), 760 + 40 * math.sin(2 * math.pi * 2.3 * t))
        if t > .4:
            q = back((t - .4) / .4)
            p.E(540, 1325, 200 * q, 40 * q, (205, 160, 110), OL, 4)
    else:
        p.E(540, 1335, 230, 46, (205, 160, 110), OL, 4)
    steps = {}
    for i, L in enumerate(spec["layers"]):
        steps.setdefault(L["step"], []).append(i)
    wob = 0
    if t >= 29.4: wob = 8 * math.sin((t - 29.4) * 6)
    pop = 1.0
    if 29.0 <= t < 29.8: pop = 1 + 0.06 * math.sin(math.pi * (t - 29.0) / 0.8)
    cur = None
    for i, L in enumerate(spec["layers"]):
        a, b = win(L["step"])
        a += 0 if L["step"] > 0 else 0
        idxs = steps[L["step"]]
        m = idxs.index(i)
        t0 = a + 0.3 + m * (4.2 / max(len(idxs), 1))
        if t < t0:
            continue
        q = cl((t - t0) / 0.5)
        yoff = -(1 - q) ** 2 * 800
        sq = 1.0
        land = t - t0 - .5
        if 0 < land < .25:
            sq = 1 - .06 * math.sin(math.pi * land / .25)
        yy = ys[i] + yoff
        h2 = pop
        layer_draw(p, L, 540 + wob * (1 - i / len(spec["layers"])), yy + (ys[i] - 1335) * (pop - 1), t)
        if (t - t0) < 1.0:
            cur = (540, ys[i] - 340)
    if cur and 3 <= t < 25:
        rh = (cur[0] + 25, cur[1])
    if 25 <= t < 29:  # shine sweep
        for i2, (sx, sy) in enumerate(((320, 1000), (760, 1050), (430, 1250), (700, 1280))):
            star(p, sx, sy, 34 * max(0, math.sin((t - 25) * 6 + i2 * 1.7)), (255, 240, 130))
    if t >= 29.0:
        fl = spec.get("face", len(spec["layers"]) // 2)
        L = spec["layers"][fl]
        face(p, 540 + wob, ys[fl] - L["h"] / 2 + 6, spec.get("fs", 1.1), t)
    return lh, rh, prop, None

def scene(p, t, topic):
    if topic["spec"]["type"] == "round":
        return round_scene(p, t, topic)
    return stack_scene(p, t, topic)

def events(topic):
    ev = [(0.35, "thump")]
    spec = topic["spec"]
    if spec["type"] == "round":
        parts = make_parts(spec, topic["day"])
        for k in range(8): ev.append((3.4 + k * .55, "thump"))
        for i, op in enumerate(spec["ops"]):
            a, b = win(i + 1)
            if op["op"] == "scatter":
                for u, v, t0, c in parts[i]:
                    ev.append((t0 + .38, "pop" if len(parts[i]) < 40 else "tick"))
            else:
                for k in range(10): ev.append((a + .5 + k * .45, "pop"))
        ev += [(25.0, "whoosh"), (28.2, "whoosh"), (28.1, "ding")]
    else:
        steps = {}
        for i, L in enumerate(spec["layers"]):
            steps.setdefault(L["step"], []).append(i)
        for i, L in enumerate(spec["layers"]):
            a, b = win(L["step"]); m = steps[L["step"]].index(i)
            ev.append((a + .3 + m * (4.2 / len(steps[L["step"]])) + .5, "thump"))
        ev.append((25.2, "sparkle"))
    ev += [(29.3, "sparkle"), (33.4, "sparkle")]
    return ev
