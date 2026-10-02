import numpy as np, wave, random
SR = 44100

def make_audio(day, events, dur, path):
    N = int(SR * dur)
    out = np.zeros(N)
    rng = np.random.default_rng(day)
    def add(t0, sig, gain=1.0):
        i = int(t0 * SR)
        if i >= N or i < 0: return
        j = min(N, i + len(sig))
        out[i:j] += sig[:j - i] * gain
    def tone(freq, d, kind="tri", decay=6.0):
        t = np.arange(int(d * SR)) / SR
        ph = 2 * np.pi * freq * t
        w = np.sin(ph) if kind == "sine" else 2 / np.pi * np.arcsin(np.sin(ph))
        return w * np.exp(-decay * t) * np.minimum(1, t / 0.005)
    bpm = 108 + (day * 7) % 24
    beat = 60 / bpm
    shift = [0, 2, 3, 5, 7][day % 5]
    C = 261.63 * 2 ** (shift / 12)
    hz = lambda semi: C * 2 ** (semi / 12)
    pent = [0, 2, 4, 7, 9, 12, 14, 16]
    prog = [[0, -3, -7, -5], [0, -5, -3, -7], [-3, -7, 0, -5]][day % 3]
    r = random.Random(day * 13)
    phrase = [r.choice(pent) for _ in range(8)]; phrase[0] = 12; phrase[-1] = 7
    for b in range(int(dur / beat)):
        t0 = b * beat; chord = prog[(b // 4) % 4]
        add(t0, tone(hz(chord - 12), beat * .9, "sine", 4), 0.30)
        kt = np.arange(int(.18 * SR)) / SR
        add(t0, np.sin(2 * np.pi * 100 * (1 - np.exp(-kt * 20)) / 20 + 2 * np.pi * 50 * kt) * np.exp(-kt * 18), 0.33)
        h = rng.standard_normal(int(.05 * SR)); h = np.diff(h, prepend=0) * np.exp(-np.arange(len(h)) / SR * 70)
        add(t0 + beat / 2, h, 0.09)
        for k in range(2):
            idx = (b * 2 + k) % 8
            add(t0 + k * beat / 2, tone(hz(phrase[idx] + (chord if idx % 4 == 0 else 0) + 12), beat * .55, "tri", 7), 0.16)
        if b % 2 == 1:
            for iv in (0, 4, 7): add(t0, tone(hz(chord + iv), beat * .35, "tri", 12), 0.07)
    def pop(t0, f0=500, f1=1000, d=.12, g=.3):
        t = np.arange(int(d * SR)) / SR
        add(t0, np.sin(2 * np.pi * np.cumsum(f0 + (f1 - f0) * t / d) / SR) * np.exp(-t * 25), g)
    def thump(t0, f=90, d=.25, g=.45):
        t = np.arange(int(d * SR)) / SR
        add(t0, np.sin(2 * np.pi * f * t * np.exp(-t * 4)) * np.exp(-t * 14), g)
    def whoosh(t0, d=.7, g=.25):
        n = int(d * SR)
        k = np.convolve(rng.standard_normal(n), np.ones(40) / 40, mode='same')
        add(t0, k * np.sin(np.pi * np.arange(n) / n) ** 2, g * 3)
    def ding(t0, g=.3):
        for f in (1318, 1976): add(t0, tone(f, 1.2, "sine", 3.5), g * (1 if f < 1500 else .5))
    def sparkle(t0, g=.2):
        for i, n in enumerate([12, 16, 19, 24, 28]): add(t0 + i * .07, tone(hz(n + 12), .35, "sine", 8), g)
    for t0, k in events:
        if k == "pop": pop(t0)
        elif k == "tick": pop(t0, 1500, 1700, .03, .05)
        elif k == "thump": thump(t0)
        elif k == "tool": thump(t0, 140, .1, .22); pop(t0 + .05, 700, 400, .08, .12)
        elif k == "whoosh": whoosh(t0)
        elif k == "ding": ding(t0)
        elif k == "sparkle": sparkle(t0)
    out *= np.clip(np.minimum(1, (dur - np.arange(N) / SR) / 1.2), 0, 1)
    out = out / np.max(np.abs(out)) * 0.85
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes())
