import math
from engine import *
import foods, repairs
from topics import TOPICS

BOUNDS = [0, 3.0, 8.5, 14.0, 19.5, 25.0, 29.0, 33.0, 36.0]
CAP_COL = [(255,120,60),(80,160,230),(230,80,70),(240,180,40),(90,180,90),(230,110,40),(160,100,220),(230,80,120)]
DUR = 36.0

def caption(p, t, caps):
    for i in range(8):
        if BOUNDS[i] <= t < BOUNDS[i + 1]:
            s = caps[i]
            q = back((t - BOUNDS[i]) / 0.35)
            size = (62 if len(s) < 20 else 52 if len(s) < 27 else 44) * (0.6 + 0.4 * q)
            w = p.TW(s, size) + 90
            p.RR(540 - w / 2, 190, 540 + w / 2, 330, 70, WHITE, CAP_COL[i], 10)
            p.TX(540, 262, s, size, (70, 50, 45))
            break
    p.RR(100, 100, 980, 120, 10, WHITE)
    p.RR(100, 100, 100 + 880 * (t / DUR), 120, 10, (255, 120, 60))

def frame(day, t):
    topic = TOPICS[day]
    food = topic["kind"] == "food"
    img = WALL.copy()
    p = Pen(img)
    bob = 5 * math.sin(2 * math.pi * 1.1 * t)
    om = 0.3 if t < 3 else (0.5 + 0.5 * math.sin(t * 5) if t > 31.3 else 0)
    draw_character(p, t, bob, om, worker=not food)
    img.paste(COUNTER, (0, 1100 * S))
    p = Pen(img)
    if t >= 33.0:
        p.d.rectangle([200 * S, 1430 * S, 880 * S, 1740 * S], fill=(190, 126, 74))
        p.RR(110, 1440, 970, 1560, 50, (255, 120, 60), OL, 7)
        p.TX(540, 1500, "Yarın: " + topic["next"], 46, WHITE)
        p.RR(300, 1600, 780, 1720, 50, (230, 50, 60), OL, 7)
        p.TX(540, 1660, "Takip et!", 56, WHITE)
        p.PG([(240, 1632), (270, 1660), (240, 1688)], WHITE)
    mod = foods if food else repairs
    lh, rh, prop, over = mod.scene(p, t, topic)
    draw_arm(p, SH_L, lh, -1)
    draw_arm(p, SH_R, rh, 1)
    if prop:
        k = prop[0]
        if k == "pin":
            py = prop[1]
            p.RR(310, py - 26, 770, py + 26, 26, (214, 164, 108), OL, 5)
            p.RR(250, py - 18, 330, py + 18, 16, (170, 110, 70), OL, 5); p.RR(750, py - 18, 830, py + 18, 16, (170, 110, 70), OL, 5)
        elif k == "ladle":
            hx, hy = rh
            p.LN([(hx, hy), (hx + 12, hy + 95)], 16, (160, 165, 180))
            p.E(hx + 14, hy + 105, 40, 24, (170, 175, 190), OL, 4)
        elif k == "mag":
            wx, wy = prop[1]
            p.LN([(wx + 50, wy - 50), (rh[0], rh[1])], 16, (120, 90, 60))
            p.E(wx, wy, 70, 70, (210, 240, 255), (120, 90, 60), 12)
        elif k == "tool":
            repairs.tool(p, prop[1], prop[2][0], prop[2][1], prop[3][0], prop[3][1], t)
            if prop[1] in ("wrench", "screwdriver"): repairs.sparks(p, prop[3][0], prop[3][1], t)
    draw_hand(p, lh); draw_hand(p, rh)
    if over: over()
    foods.fx(p, topic["fx"], t)
    caption(p, t, topic["caps"])
    return img.resize((W, H), Image.LANCZOS)

def events(day):
    topic = TOPICS[day]
    return (foods if topic["kind"] == "food" else repairs).events(topic)
