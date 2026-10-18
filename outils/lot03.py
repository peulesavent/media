"""Lot 3 : 7 Reels et 3 carrousels."""
import math
import sys
from PIL import Image, ImageDraw
from pls import font, layer, FONT_BLACK, FONT_MED, INK, ACCENT, BG, LINE, MUTED
from reels_s01 import render, ease, _canvas, _done
from carrousels_s01 import build

RED = (214, 72, 72)
BLUE = (80, 140, 230)
GREEN = (98, 160, 92)
SAND = (214, 178, 112)
YEL = (238, 206, 92)


def mix(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def label(d, x, y, txt, size=64, col=INK, anchor="mm"):
    d.text((x, y), txt, font=font(FONT_BLACK, size), fill=col, anchor=anchor)


# ================= REELS =================

# --- Cléopâtre : frise chronologique ---
def timeline(t, show=3, hl=None):
    im, d, w, h = _canvas()
    y = h + 80
    x0, x1 = 300, 2 * w - 300
    d.line((x0, y, x1, y), fill=MUTED, width=10)
    # -2560 -> 2026, échelle linéaire
    def X(yr):
        return x0 + (yr + 2600) / (2026 + 2600) * (x1 - x0)
    pts = [(-2560, "Khéops", "v. 2560 av."), (-30, "Cléopâtre", "30 av."), (2007, "iPhone", "2007")]
    k = ease(t * 1.6)
    for i, (yr, name, dt) in enumerate(pts[:show]):
        x = X(yr)
        col = ACCENT if hl is None or i in hl else INK
        if i == 0:
            d.polygon([(x - 120, y - 30), (x + 120, y - 30), (x, y - 230)], fill=SAND)
        elif i == 1:
            d.ellipse((x - 46, y - 150, x + 46, y - 58), fill=col)
            d.polygon([(x - 70, y - 30), (x + 70, y - 30), (x, y - 120)], fill=col)
        else:
            d.rounded_rectangle((x - 50, y - 210, x + 50, y - 30), radius=22, outline=col, width=12)
        d.ellipse((x - 22, y - 22, x + 22, y + 22), fill=col)
        label(d, x, y + 110, name, 84, col)
        label(d, x, y + 200, dt, 62, MUTED)
    if hl is not None and len(hl) == 2:
        a, b = sorted(hl)
        xa, xb = X(pts[a][0]), X(pts[b][0])
        xe = xa + (xb - xa) * k
        d.line((xa, y - 300, xe, y - 300), fill=ACCENT, width=14)
        d.line((xa, y - 330, xa, y - 270), fill=ACCENT, width=10)
        if k > 0.98:
            d.line((xb, y - 330, xb, y - 270), fill=ACCENT, width=10)
    return _done(im)


CLEO = [
    dict(text="Cléopâtre a vécu plus près de l'iPhone *que de la grande pyramide.*", hook=True,
         illus=lambda t: timeline(t, 3), dur=3.4),
    dict(text="La pyramide de Khéops est construite vers *2560 av. J.-C.* "
              "À la naissance de Cléopâtre, elle a déjà près de 2 500 ans.",
         illus=lambda t: timeline(t, 2, hl=(0, 1)), dur=4.2),
    dict(text="Cléopâtre meurt en *30 av. J.-C.* Jusqu'au premier iPhone, en 2007, "
              "il s'écoule environ 2 036 ans.", illus=lambda t: timeline(t, 3, hl=(1, 2)), dur=4.2),
    dict(text="Pour elle, la grande pyramide était déjà *un monument très ancien.* "
              "Plus ancien encore qu'elle ne l'est pour nous.", illus=lambda t: timeline(t, 3, hl=(0,)), dur=3.8),
]


# --- Pieuvre ---
def octopus(t, hearts="all", pulse=True, blood=False):
    im, d, w, h = _canvas()
    cx, cy = w, h - 120
    body = (176, 92, 120)
    for k in range(8):
        a = math.radians(200 + k * 20)
        pts = []
        for i in range(30):
            s = i / 29
            r = 180 + s * 520
            wob = math.sin(s * 5 + t * 6 + k) * 40 * s
            pts.append((cx + math.cos(a) * r * 0.9 + wob, cy + 260 + s * 420 + math.sin(a) * 60))
        d.line(pts, fill=body, width=int(70), joint="curve")
    d.ellipse((cx - 300, cy - 360, cx + 300, cy + 300), fill=body)
    d.ellipse((cx - 150, cy - 40, cx - 70, cy + 40), fill=INK)
    d.ellipse((cx + 70, cy - 40, cx + 150, cy + 40), fill=INK)
    d.ellipse((cx - 120, cy - 10, cx - 90, cy + 20), fill=BG)
    d.ellipse((cx + 100, cy - 10, cx + 130, cy + 20), fill=BG)
    beat = 1 + (0.18 * max(0, math.sin(t * 2 * math.pi * 3)) if pulse else 0)

    def heart(x, y, s, col):
        s *= beat
        d.ellipse((x - s, y - s * 0.8, x, y + s * 0.2), fill=col)
        d.ellipse((x, y - s * 0.8, x + s, y + s * 0.2), fill=col)
        d.polygon([(x - s * 0.98, y - s * 0.2), (x + s * 0.98, y - s * 0.2), (x, y + s * 1.0)], fill=col)

    hy = cy - 210
    if hearts in ("all", "small"):
        heart(cx - 170, hy, 46, ACCENT if hearts == "small" else RED)
        heart(cx + 170, hy, 46, ACCENT if hearts == "small" else RED)
    if hearts in ("all", "big"):
        heart(cx, hy - 20, 74, ACCENT if hearts == "big" else RED)
    if blood:
        for k in range(10):
            ph = (t * 1.5 + k / 10) % 1
            x = cx - 600 + ph * 1200
            y = h * 2 - 120 + 30 * math.sin(ph * 12)
            d.ellipse((x - 20, y - 20, x + 20, y + 20), fill=BLUE)
    return _done(im)


PIEUVRE = [
    dict(text="La pieuvre a *trois cœurs.* Et le sang bleu.", hook=True,
         illus=lambda t: octopus(t, "all"), dur=3.0),
    dict(text="Deux petits cœurs, un par branchie, y poussent le sang "
              "pour qu'il se charge en *oxygène.*", illus=lambda t: octopus(t, "small"), dur=3.8),
    dict(text="Le troisième, le plus gros, l'envoie ensuite *dans tout le corps.*",
         illus=lambda t: octopus(t, "big"), dur=3.4),
    dict(text="Son sang transporte l'oxygène grâce au *cuivre*, pas au fer comme le nôtre. "
              "Oxygéné, il devient bleu.", illus=lambda t: octopus(t, "all", blood=True), dur=4.0),
    dict(text="Quand elle nage, son gros cœur *marque une pause.* "
              "Une des raisons pour lesquelles elle préfère souvent ramper.",
         illus=lambda t: octopus(t, "big", pulse=False), dur=4.0),
]


# --- Bananes ---
def banana(t, dots=True, n=14):
    im, d, w, h = _canvas()
    cx, cy = w, h - 40
    pts_o, pts_i = [], []
    for i in range(41):
        a = math.radians(200 + i * 3.5)
        pts_o.append((cx + math.cos(a) * 640, cy + 380 + math.sin(a) * 640))
        pts_i.append((cx + math.cos(a) * 470, cy + 380 + math.sin(a) * 420))
    d.polygon(pts_o + pts_i[::-1], fill=YEL)
    d.line(pts_o, fill=(200, 168, 60), width=10)
    x, y = pts_o[0]
    d.rounded_rectangle((x - 30, y - 20, x + 40, y + 50), radius=10, fill=(110, 84, 40))
    x, y = pts_o[-1]
    d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=(90, 70, 40))
    if dots:
        for k in range(n):
            ph = (t * 0.9 + k / n) % 1
            a = k * 2.4
            r = 300 + ph * 600
            px, py = cx + math.cos(a) * r, cy + math.sin(a) * r * 0.6
            col = mix(ACCENT, BG, ph)
            d.ellipse((px - 14, py - 14, px + 14, py + 14), fill=col)
    return _done(im)


def xray(t):
    im, d, w, h = _canvas()
    # 200 petites bananes en grille qui apparaissent
    cols, rows = 20, 10
    n = int(200 * ease(t * 1.3))
    for i in range(n):
        x = 200 + (i % cols) * 92
        y = 360 + (i // cols) * 92
        d.arc((x - 40, y - 60, x + 40, y + 20), 200, 340, fill=YEL, width=14)
    label(d, w, 180, f"{n}", 140, ACCENT)
    return _done(im)


BANANE = [
    dict(text="Les bananes sont *légèrement radioactives.*", hook=True, illus=lambda t: banana(t), dur=3.0),
    dict(text="Elles sont riches en potassium. Et une infime partie de ce potassium est radioactive : "
              "le *potassium 40.*", illus=lambda t: banana(t, n=20), dur=4.2),
    dict(text="Une banane, c'est environ *0,1 microsievert.* "
              "Une radio des poumons équivaut à peu près à 200 bananes.", illus=xray, dur=4.4),
    dict(text="Aucun danger : ton corps garde son potassium stable et élimine le surplus. "
              "*Ça ne s'accumule pas.*", illus=lambda t: banana(t, dots=False), dur=4.0),
]


# --- Fraises ---
def strawberry(d, cx, cy, s, achenes=True, glow=0.0):
    pts = []
    for i in range(61):
        a = i / 60 * 2 * math.pi
        x = math.sin(a) * 300 * (1 - 0.35 * (1 - math.cos(a)) / 2)
        y = -math.cos(a) * 340
        if y > 0:
            x *= 1 - (y / 340) * 0.55
        pts.append((cx + x * s, cy + y * s))
    d.polygon(pts, fill=RED)
    for k in range(5):
        a = math.radians(-160 + k * 35)
        d.polygon([(cx, cy - 300 * s), (cx + math.cos(a) * 200 * s, cy - 300 * s + math.sin(a) * 90 * s - 40 * s),
                   (cx + math.cos(a + 0.3) * 120 * s, cy - 300 * s - 20 * s)], fill=GREEN)
    if achenes:
        col = mix(YEL, ACCENT, glow)
        rr = 9 + 8 * glow
        for i in range(6):
            for j in range(-3 + (i % 2), 4, 2):
                x = cx + j * 70 * s * (1 - i * 0.1)
                y = cy - 200 * s + i * 80 * s
                d.ellipse((x - rr * s, y - rr * 1.4 * s, x + rr * s, y + rr * 1.4 * s), fill=col)


def ill_fraise(mode):
    def f(t):
        im, d, w, h = _canvas()
        if mode == "duo":
            strawberry(d, w - 420, h + 60, 1.0)
            pts_o, pts_i = [], []
            for i in range(31):
                a = math.radians(210 + i * 4)
                pts_o.append((w + 420 + math.cos(a) * 420, h + 360 + math.sin(a) * 420))
                pts_i.append((w + 420 + math.cos(a) * 320, h + 360 + math.sin(a) * 280))
            d.polygon(pts_o + pts_i[::-1], fill=YEL)
            label(d, w - 420, h + 520, "PAS UNE BAIE", 56, MUTED)
            label(d, w + 420, h + 520, "BAIE", 56, ACCENT)
        elif mode == "flesh":
            strawberry(d, w, h + 20, 1.2, achenes=False)
        else:
            strawberry(d, w, h + 20, 1.2, glow=0.5 + 0.5 * math.sin(t * 10))
        return _done(im)
    return f


FRAISE = [
    dict(text="Pour un botaniste, la fraise *n'est pas une baie.* La banane, si.", hook=True,
         illus=ill_fraise("duo"), dur=3.6),
    dict(text="Une baie, c'est un fruit charnu issu d'un seul ovaire de la fleur. "
              "Banane, raisin, tomate : *des baies.*", illus=ill_fraise("duo"), dur=4.2),
    dict(text="La partie rouge de la fraise ? C'est *le réceptacle de la fleur*, qui a gonflé.",
         illus=ill_fraise("flesh"), dur=3.6),
    dict(text="Les vrais fruits, ce sont *les petits points jaunes.* "
              "Chacun contient une graine. Il y en a environ 200 par fraise.",
         illus=ill_fraise("dots"), dur=4.2),
]


# --- Licorne ---
def shield(t, chain=False, lion=False):
    im, d, w, h = _canvas()
    cx, cy = w, h + 20
    pts = [(cx - 330, cy - 380), (cx + 330, cy - 380), (cx + 330, cy + 60),
           (cx, cy + 420), (cx - 330, cy + 60)]
    d.polygon(pts, fill=(36, 52, 110))
    d.line(pts + [pts[0]], fill=ACCENT, width=18)
    # corne torsadée
    hx, hy = cx + (240 if lion else 0), cy
    for i in range(7):
        y = hy + 220 - i * 70
        wdt = 70 - i * 9
        d.polygon([(hx - wdt, y), (hx + wdt, y), (hx + wdt - 9, y - 60), (hx - wdt + 9, y - 60)],
                  fill=INK if i % 2 == 0 else (210, 206, 198))
    d.polygon([(hx - 8, hy - 260), (hx + 8, hy - 260), (hx, hy - 330)], fill=INK)
    if lion:
        lx = cx - 240
        d.ellipse((lx - 110, cy - 120, lx + 110, cy + 100), fill=ACCENT)
        d.ellipse((lx - 60, cy - 60, lx + 60, cy + 50), fill=(200, 140, 40))
    if chain:
        for i in range(9):
            x = cx - 420 + i * 105
            y = cy + 520 + 20 * math.sin(t * 6 + i)
            d.ellipse((x - 46, y - 28, x + 46, y + 28), outline=MUTED, width=14)
    return _done(im)


LICORNE = [
    dict(text="L'animal national de l'Écosse, c'est *la licorne.*", hook=True,
         illus=lambda t: shield(t), dur=3.2),
    dict(text="Selon la tradition, elle orne les armoiries des rois d'Écosse dès le Moyen Âge. "
              "Au XVe siècle, on frappe même des pièces d'or appelées *unicorn.*",
         illus=lambda t: shield(t), dur=4.6),
    dict(text="En 1603, le roi d'Écosse devient aussi roi d'Angleterre. "
              "Sur les armoiries, la licorne doit partager la place avec *le lion anglais.*",
         illus=lambda t: shield(t, lion=True), dur=4.4),
    dict(text="Et elle y porte souvent *une chaîne.* "
              "Le signe d'un roi assez puissant pour dompter la plus sauvage des créatures.",
         illus=lambda t: shield(t, chain=True), dur=4.0),
]


# --- Robot ---
def robot(t, glow=0.0):
    im, d, w, h = _canvas()
    cx, cy = w, h + 40
    d.rounded_rectangle((cx - 300, cy - 280, cx + 300, cy + 240), radius=60, fill=(150, 156, 166))
    d.line((cx, cy - 280, cx, cy - 420), fill=MUTED, width=16)
    d.ellipse((cx - 40, cy - 470, cx + 40, cy - 390), fill=mix(ACCENT, RED, 0.5 + 0.5 * math.sin(t * 8)))
    for ex in (-130, 130):
        d.ellipse((cx + ex - 70, cy - 150, cx + ex + 70, cy - 10), fill=BG)
        r = 30 + 10 * glow
        d.ellipse((cx + ex - r, cy - 80 - r, cx + ex + r, cy - 80 + r), fill=ACCENT)
    for k in range(5):
        x = cx - 160 + k * 80
        d.rectangle((x - 26, cy + 90, x + 26, cy + 160), fill=BG)
    return _done(im)


def word_card(word, sub):
    def f(t):
        im, d, w, h = _canvas()
        k = ease(t * 1.5)
        n = int(len(word) * k + 0.999)
        label(d, w, h - 40, word[:n], 260, ACCENT)
        label(d, w, h + 200, sub, 70, MUTED)
        return _done(im)
    return f


ROBOT = [
    dict(text="Le mot robot a à peine plus de 100 ans. *Et il vient du tchèque.*", hook=True,
         illus=lambda t: robot(t), dur=3.4),
    dict(text="En 1920, l'écrivain *Karel Čapek* publie R.U.R., une pièce sur des ouvriers artificiels "
              "qui finissent par se révolter.", illus=lambda t: robot(t, 1.0), dur=4.4),
    dict(text="Il cherchait un nom pour eux. C'est son frère, le peintre Josef, "
              "qui lui souffle : *roboti.*", illus=word_card("roboti", "Josef Čapek"), dur=4.0),
    dict(text="En tchèque, *robota* désigne la corvée, le travail forcé "
              "que les serfs devaient au seigneur.", illus=word_card("robota", "corvée"), dur=4.0),
]


# --- Zéro ---
def zero_travel(stage):
    def f(t):
        im, d, w, h = _canvas()
        stops = [("Inde", 1700, 760), ("Bagdad", 1260, 600), ("Béjaïa", 720, 520), ("Pise", 820, 300)]
        k = ease(t * 1.4)
        for i, (name, x, y) in enumerate(stops):
            on = i <= stage
            d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=ACCENT if on else LINE)
            label(d, x, y + 100, name, 84, INK if on else MUTED)
        for i in range(stage):
            (_, x1, y1), (_, x2, y2) = stops[i], stops[i + 1]
            kk = k if i == stage - 1 else 1
            d.line((x1, y1, x1 + (x2 - x1) * kk, y1 + (y2 - y1) * kk), fill=ACCENT, width=12)
        x, y = stops[stage][1], stops[stage][2]
        if stage > 0:
            (_, xa, ya) = stops[stage - 1]
            x, y = xa + (x - xa) * k, ya + (y - ya) * k
        label(d, x, y - 150, "0", 200, ACCENT)
        return _done(im)
    return f


ZERO = [
    dict(text="Le zéro que tu utilises tous les jours a fait *un très long voyage.*", hook=True,
         illus=zero_travel(0), dur=3.2),
    dict(text="En 628, en Inde, le mathématicien *Brahmagupta* traite le zéro comme un vrai nombre, "
              "avec ses propres règles de calcul.", illus=zero_travel(0), dur=4.4),
    dict(text="À Bagdad, *al-Khwarizmi* écrit en arabe sur le calcul indien. "
              "Son nom, latinisé, a donné le mot *algorithme.*", illus=zero_travel(1), dur=4.4),
    dict(text="À la fin du XIIe siècle, un jeune Pisan apprend ces chiffres à *Béjaïa*, en Algérie : Fibonacci. "
              "Son livre de 1202 aide à les répandre en Europe.", illus=zero_travel(3), dur=4.8),
]


# ================= CARROUSELS =================

def ill_emeu(W, H):
    im, d = layer(W, H)
    cx, gy = W // 2, int(H * 0.95)
    body = (120, 104, 88)
    d.ellipse((cx - 380, gy - 640, cx + 220, gy - 300), fill=body)
    d.line((cx + 140, gy - 560, cx + 220, gy - 960), fill=body, width=70)
    d.ellipse((cx + 160, gy - 1060, cx + 300, gy - 930), fill=body)
    d.polygon([(cx + 290, gy - 1010), (cx + 380, gy - 990), (cx + 290, gy - 965)], fill=MUTED)
    d.ellipse((cx + 230, gy - 1015, cx + 260, gy - 985), fill=INK)
    for lx in (-120, 40):
        d.line((cx + lx, gy - 330, cx + lx - 30, gy - 20), fill=MUTED, width=30)
        d.line((cx + lx - 30, gy - 20, cx + lx + 60, gy - 10), fill=MUTED, width=22)
    d.line((60, gy, W - 60, gy), fill=LINE, width=8)
    # petits impacts manqués
    for x, y in ((420, 380), (1760, 520), (1600, 260), (300, 700)):
        d.line((x - 30, y, x + 30, y), fill=ACCENT, width=8)
        d.line((x, y - 30, x, y + 30), fill=ACCENT, width=8)
    return im


def ill_fes(W, H):
    im, d = layer(W, H)
    cx, gy = W // 2, int(H * 0.95)
    # toit de tuiles vertes et porte en arc
    d.rectangle((cx - 700, gy - 520, cx + 700, gy), fill=(232, 222, 200))
    d.polygon([(cx - 780, gy - 520), (cx + 780, gy - 520), (cx + 640, gy - 760), (cx - 640, gy - 760)],
              fill=(46, 120, 92))
    for i in range(14):
        x = cx - 700 + i * 108
        d.line((x, gy - 520, cx + (x - cx) * 640 / 780, gy - 760), fill=(36, 96, 74), width=8)
    r = 210
    d.pieslice((cx - r, gy - 360 - r, cx + r, gy - 360 + r), 180, 360, fill=(120, 74, 40))
    d.rectangle((cx - r, gy - 360, cx + r, gy), fill=(120, 74, 40))
    for k in range(-5, 6):
        x = cx + k * 120
        d.polygon([(x, gy - 470), (x + 30, gy - 440), (x, gy - 410), (x - 30, gy - 440)], fill=ACCENT)
    return im


def ill_sahara(W, H):
    im, d = layer(W, H)
    gy = int(H * 0.95)
    d.ellipse((W - 640, 80, W - 360, 360), fill=ACCENT)
    # dunes vertes
    for k, col in enumerate(((70, 128, 70), (88, 150, 80), (110, 170, 96))):
        pts = [(0, gy)]
        for i in range(41):
            x = W * i / 40
            pts.append((x, gy - 260 - 120 * k + 80 * math.sin(i / 40 * math.pi * 3 + k)))
        pts.append((W, gy))
        d.polygon(pts, fill=col)
    # lac
    d.ellipse((W * 0.18, gy - 140, W * 0.62, gy - 20), fill=(64, 120, 180))
    # girafe stylisée
    gx = int(W * 0.78)
    d.rectangle((gx - 120, gy - 420, gx + 80, gy - 300), fill=SAND)
    d.line((gx + 60, gy - 400, gx + 160, gy - 740), fill=SAND, width=44)
    d.ellipse((gx + 120, gy - 800, gx + 240, gy - 720), fill=SAND)
    for lx in (-100, -40, 30, 70):
        d.line((gx + lx, gy - 300, gx + lx, gy - 60), fill=SAND, width=20)
    return im


EMEUS = dict(slug="2026-10-18-guerre-emeus", label="Histoire vraie", slides=[
    dict(illus=ill_emeu,
         title="En 1932, l'Australie envoie des mitrailleuses contre des émeus. "
               "*Ça ne s'est pas passé comme prévu.*"),
    dict(body="Australie-Occidentale, fin 1932. Environ *20 000 émeus* "
              "envahissent les champs de blé des fermiers de la région de Campion."),
    dict(body="Le gouvernement envoie *trois militaires*, menés par le major Meredith, "
              "avec deux mitrailleuses Lewis et 10 000 cartouches."),
    dict(body="Sur le terrain, les émeus courent vite, se dispersent dès qu'on approche "
              "et se révèlent *difficiles à abattre.*"),
    dict(big="986",
         body="C'est le nombre d'émeus tués selon le rapport officiel. "
              "Pour 9 860 cartouches. *Dix balles par oiseau.*"),
    dict(body="En décembre, les militaires sont retirés. La presse se moque de l'opération, "
              "en Australie comme à l'étranger.\n\n"
              "Les fermiers redemanderont l'armée les années suivantes. *Refusé.*"),
    dict(body="Des années plus tard, Meredith aurait confié à la presse qu'avec des soldats "
              "aussi résistants que ces oiseaux, il pourrait affronter "
              "*n'importe quelle armée du monde.*",
         footer="Les émeus, eux, se portent très bien."),
])

FES = dict(slug="2026-10-19-quaraouiyine", label="Patrimoine marocain", slides=[
    dict(illus=ill_fes,
         title="Le plus ancien établissement d'enseignement supérieur encore ouvert *est à Fès.*"),
    dict(big="859",
         body="Selon la tradition, c'est l'année où *Fatima al-Fihriya*, une femme venue de Kairouan, "
              "fonde la Quaraouiyine au cœur de la médina de Fès."),
    dict(body="C'est d'abord une mosquée, et elle l'est toujours. Au fil des siècles, "
              "elle devient *un grand centre de savoir*, où l'on vient étudier de loin."),
    dict(body="Selon la même tradition, sa sœur *Mariam* aurait fondé l'autre grande mosquée "
              "de la ville, celle des Andalous."),
    dict(body="Le Guinness des records la classe comme *le plus ancien établissement "
              "d'enseignement supérieur* au monde. En 1963, elle devient une université d'État."),
    dict(body="Sa bibliothèque, l'une des plus anciennes du monde, a été restaurée "
              "par l'architecte marocaine *Aziza Chaouni.* Elle a rouvert en 2016."),
    dict(body="Les historiens débattent encore du mot université, né du modèle européen. "
              "Mais une chose est sûre : on y enseigne depuis *plus de 900 ans.*",
         footer="Fès, 859. Et toujours ouverte."),
])

SAHARA = dict(slug="2026-10-19-sahara-vert", label="Histoire de la Terre", slides=[
    dict(illus=ill_sahara, title="Il y a 10 000 ans, le Sahara *était vert.*"),
    dict(body="Une vraie *savane*, avec des lacs, des rivières et des prairies.\n\n"
              "Les scientifiques parlent de période humide africaine."),
    dict(body="Elle commence il y a environ *14 500 ans* et s'achève il y a 5 000 à 6 000 ans, "
              "par étapes."),
    dict(big="330 000 km²",
         body="C'était la surface du lac *Méga-Tchad.* Presque la taille de l'Allemagne."),
    dict(body="Hippopotames, girafes, éléphants, crocodiles y vivaient.\n\n"
              "On les retrouve gravés et peints sur les rochers du *Tassili n'Ajjer*, "
              "dans le sud de l'Algérie."),
    dict(body="La cause : une variation de *l'orbite de la Terre.* Plus de soleil en été dans l'hémisphère Nord, "
              "une mousson plus forte qui remonte vers le nord."),
    dict(body="Puis l'orbite a continué de bouger, la mousson a reculé, "
              "et *le désert est revenu.*",
         footer="Le Sahara a déjà reverdi plusieurs fois. Il recommencera."),
])

REELS = {
    "cleo": ("2026-10-18-cleopatre", CLEO),
    "pieuvre": ("2026-10-18-pieuvre", PIEUVRE),
    "banane": ("2026-10-19-bananes", BANANE),
    "fraise": ("2026-10-19-fraises", FRAISE),
    "licorne": ("2026-10-19-licorne", LICORNE),
    "robot": ("2026-10-19-robot", ROBOT),
    "zero": ("2026-10-19-zero", ZERO),
}

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or "carrousels" in args:
        for c in (EMEUS, FES, SAHARA):
            build(c)
    if "sahara" in args:
        build(SAHARA)
    for k in args:
        if k in REELS:
            render(*REELS[k])
