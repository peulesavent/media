"""Lot 2 : Reels flamants roses, trou du capuchon, Violet Jessop."""
import math
from pls import font, FONT_BLACK, INK, ACCENT, BG, LINE, MUTED
from reels_s01 import render, ease, _canvas, _done

GREY = (150, 148, 144)
PINK = (238, 120, 150)


def mix(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


# ---------- flamant ----------

def flamingo(d, w, h, col, s=1.0):
    u = 80 * s
    cx, cy = w, h + 0.6 * u
    leg = mix(col, (90, 90, 90), 0.3)
    # pattes
    d.line((cx - 0.3 * u, cy + 1.0 * u, cx - 0.3 * u, cy + 6.2 * u), fill=leg, width=int(14 * s))
    d.line((cx + 0.4 * u, cy + 1.0 * u, cx + 0.4 * u, cy + 3.6 * u), fill=leg, width=int(14 * s))
    d.line((cx + 0.4 * u, cy + 3.6 * u, cx - 0.3 * u, cy + 4.2 * u), fill=leg, width=int(14 * s))
    # corps
    d.ellipse((cx - 2.6 * u, cy - 1.2 * u, cx + 1.4 * u, cy + 1.3 * u), fill=col)
    d.polygon([(cx - 2.4 * u, cy - 0.3 * u), (cx - 3.6 * u, cy + 0.2 * u),
               (cx - 2.2 * u, cy + 0.7 * u)], fill=col)
    # cou en S
    pts = []
    for i in range(41):
        t = i / 40
        x = cx + 1.0 * u + 1.1 * u * math.sin(t * math.pi * 1.6)
        y = cy - 0.6 * u - 5.4 * u * t
        pts.append((x, y))
    d.line(pts, fill=col, width=int(36 * s), joint="curve")
    hx, hy = pts[-1]
    d.ellipse((hx - 0.55 * u, hy - 0.5 * u, hx + 0.55 * u, hy + 0.5 * u), fill=col)
    # bec courbé
    d.polygon([(hx + 0.35 * u, hy - 0.25 * u), (hx + 1.5 * u, hy + 0.3 * u),
               (hx + 1.2 * u, hy + 1.0 * u), (hx + 0.3 * u, hy + 0.35 * u)], fill=INK)
    d.polygon([(hx + 1.25 * u, hy + 0.45 * u), (hx + 1.5 * u, hy + 0.3 * u),
               (hx + 1.2 * u, hy + 1.0 * u)], fill=BG)
    d.ellipse((hx - 0.05 * u, hy - 0.2 * u, hx + 0.15 * u, hy), fill=BG)


def ill_fl_hook(t):
    im, d, w, h = _canvas()
    flamingo(d, w, h - 260, mix(GREY, PINK, 0.15 + 0.15 * t), 1.2)
    return _done(im)


def ill_fl_grey(t):
    im, d, w, h = _canvas()
    # poussin : boule de duvet gris
    cx, cy = w, h + 200
    d.ellipse((cx - 260, cy - 200, cx + 260, cy + 220), fill=GREY)
    d.ellipse((cx + 120, cy - 380, cx + 380, cy - 120), fill=GREY)
    d.polygon([(cx + 360, cy - 270), (cx + 470, cy - 230), (cx + 350, cy - 190)], fill=INK)
    d.ellipse((cx + 270, cy - 290, cx + 300, cy - 260), fill=BG)
    d.line((cx - 60, cy + 210, cx - 60, cy + 400), fill=MUTED, width=16)
    d.line((cx + 80, cy + 210, cx + 80, cy + 400), fill=MUTED, width=16)
    return _done(im)


def ill_fl_food(t):
    im, d, w, h = _canvas()
    flamingo(d, w - 200, h - 260, mix(GREY, PINK, ease(t)), 1.1)
    # eau et petites crevettes
    wy = h * 2 - 140
    d.rectangle((0, wy, w * 2, h * 2), fill=(30, 40, 52))
    for k in range(7):
        x = 260 + k * 230 + 40 * math.sin(t * 6 + k)
        y = wy + 60 + 20 * math.cos(t * 5 + k)
        d.arc((x - 40, y - 24, x + 40, y + 24), 200, 340, fill=PINK, width=12)
    return _done(im)


def ill_fl_pale(t):
    im, d, w, h = _canvas()
    flamingo(d, w, h - 260, mix(PINK, (232, 226, 222), ease(t * 1.2)), 1.1)
    return _done(im)


# ---------- capuchon ----------

def cap(d, w, h, flow=0.0, zoom=1.0):
    cx, cy = w, h
    L, R = 560 * zoom, 120 * zoom
    top = cy - L
    d.rounded_rectangle((cx - R, top, cx + R, cy + L * 0.6), radius=int(R * 0.9), fill=(56, 108, 196))
    # clip
    d.rounded_rectangle((cx + R - 10, top + 80 * zoom, cx + R + 40 * zoom, cy + L * 0.3),
                        radius=20, fill=(46, 92, 170))
    # trou au sommet
    hr = 34 * zoom
    d.ellipse((cx - hr, top + 70 * zoom - hr, cx + hr, top + 70 * zoom + hr), fill=BG)
    # flux d'air
    if flow > 0:
        for k in range(3):
            ph = (flow * 2.5 + k / 3) % 1
            y = top + 70 * zoom - 60 - ph * 420
            a = 1 - ph
            col = mix(BG, ACCENT, a)
            d.arc((cx - 90 + k * 10, y - 40, cx + 90 - k * 10, y + 40), 200, 340, fill=col, width=14)


def ill_cap_hook(t):
    im, d, w, h = _canvas()
    cap(d, w, h + 120, 0.0, 1.0)
    # cercle de mise en évidence sur le trou
    r = 120 + 12 * math.sin(t * 10)
    cy = h + 120 - 560 + 70
    d.ellipse((w - r, cy - r, w + r, cy + r), outline=ACCENT, width=12)
    return _done(im)


def ill_cap_air(t):
    im, d, w, h = _canvas()
    cap(d, w, h + 260, flow=t, zoom=1.0)
    return _done(im)


def ill_cap_static(t):
    im, d, w, h = _canvas()
    cap(d, w, h + 120, 0.0, 1.0)
    return _done(im)


# ---------- paquebots ----------

def liner(d, x, y, s, tilt=0.0, col=INK):
    """Paquebot à quatre cheminées, x,y = point bas au centre de la coque."""
    def rot(px, py):
        a = math.radians(tilt)
        return (x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a))
    hull = [(-520, 0), (560, 0), (640, -150), (-600, -150)]
    d.polygon([rot(*p) for p in hull], fill=col)
    deck = [(-460, -150), (480, -150), (480, -230), (-460, -230)]
    d.polygon([rot(*p) for p in deck], fill=mix(col, BG, 0.25))
    for k in range(4):
        fx = -300 + k * 190
        f = [(fx - 40, -230), (fx + 40, -230), (fx + 54, -440), (fx - 26, -440)]
        d.polygon([rot(*p) for p in f], fill=mix(col, BG, 0.1))
        tp = [(fx - 26, -440), (fx + 54, -440), (fx + 50, -390), (fx - 30, -390)]
        d.polygon([rot(*p) for p in tp], fill=ACCENT)
    for k in range(14):
        px = -440 + k * 66
        c = rot(px, -80)
        d.ellipse((c[0] - 12 * s, c[1] - 12 * s, c[0] + 12 * s, c[1] + 12 * s), fill=BG)


def year_label(d, w, txt):
    f = font(FONT_BLACK, 150)
    tw = d.textlength(txt, font=f)
    d.text((w - tw / 2, 60), txt, font=f, fill=ACCENT)


def sea(d, w, h, y):
    d.rectangle((0, y, w * 2, h * 2), fill=(24, 30, 40))
    d.line((0, y, w * 2, y), fill=MUTED, width=6)


def ill_ships_hook(t):
    im, d, w, h = _canvas()
    sy = int(h * 1.55)
    # trois silhouettes réduites
    from PIL import Image, ImageDraw
    small = Image.new("RGBA", (1400, 560), (0, 0, 0, 0))
    sd = ImageDraw.Draw(small)
    liner(sd, 700, 520, 1.0)
    small = small.resize((620, 248), Image.LANCZOS)
    for k, dx in enumerate((-640, 0, 640)):
        im.paste(small, (int(w + dx - 310), int(sy - 248 + 10 * math.sin(t * 6 + k))), small)
    sea(d, w, h, sy)
    return _done(im)


def ill_olympic(t):
    im, d, w, h = _canvas()
    year_label(d, w, "1911")
    sy = int(h * 1.6)
    liner(d, w - 120, sy, 1.0)
    # le croiseur qui arrive par le côté
    bx = w * 2 + 200 - 700 * ease(t * 1.4)
    d.polygon([(bx, sy), (bx + 600, sy), (bx + 600, sy - 110), (bx - 60, sy - 110)], fill=MUTED)
    d.rectangle((bx + 160, sy - 210, bx + 300, sy - 110), fill=MUTED)
    sea(d, w, h, sy)
    return _done(im)


def ill_titanic(t):
    im, d, w, h = _canvas()
    year_label(d, w, "1912")
    sy = int(h * 1.6)
    liner(d, w, sy + 60 * ease(t), 1.0, tilt=-6 * ease(t))
    # iceberg
    d.polygon([(w + 520, sy), (w + 640, sy - 260), (w + 760, sy - 180), (w + 860, sy)], fill=(210, 222, 230))
    sea(d, w, h, sy)
    return _done(im)


def ill_britannic(t):
    im, d, w, h = _canvas()
    year_label(d, w, "1916")
    sy = int(h * 1.6)
    liner(d, w, sy + 80 * ease(t), 1.0, tilt=8 * ease(t), col=(232, 230, 224))
    sea(d, w, h, sy)
    return _done(im)


FLAMANT = [
    dict(text="Les flamants roses *naissent gris.*", hook=True, illus=ill_fl_hook, dur=3.0),
    dict(text="Les poussins sortent de l'œuf couverts d'un duvet *gris ou blanc.* "
              "Le rose arrive petit à petit, sur plusieurs années.", illus=ill_fl_grey, dur=3.8),
    dict(text="La couleur vient de leur nourriture : des pigments, les *caroténoïdes*, "
              "présents dans les algues et les petites crevettes qu'ils filtrent.", illus=ill_fl_food, dur=4.2),
    dict(text="Privé de cette nourriture, un flamant pâlit, parfois presque jusqu'au blanc. "
              "C'est pour ça que les zoos *enrichissent leur alimentation.*", illus=ill_fl_pale, dur=4.2),
]

CAPUCHON = [
    dict(text="Le petit trou au bout du capuchon de ton stylo *n'est pas là pour faire joli.*",
         hook=True, illus=ill_cap_hook, dur=3.4),
    dict(text="Si quelqu'un avale le capuchon de travers, le trou *laisse passer un peu d'air.*",
         illus=ill_cap_air, dur=3.6),
    dict(text="BIC l'explique : c'est pour *limiter le risque d'étouffement* "
              "si un enfant inhale un capuchon.", illus=ill_cap_air, dur=3.8),
    dict(text="Ses capuchons respectent une norme de sécurité internationale, "
              "*l'ISO 11540*, conçue exactement pour ça.", illus=ill_cap_static, dur=3.8),
]

JESSOP = [
    dict(text="Le Titanic avait deux navires jumeaux. *Elle a survécu aux accidents des trois.*", hook=True, illus=ill_ships_hook, dur=3.6),
    dict(text="*Violet Jessop*, hôtesse à bord de l'Olympic. En 1911, un croiseur de la Royal Navy "
              "l'éperonne. Aucun mort, le navire rentre au port.", illus=ill_olympic, dur=4.2),
    dict(text="Elle passe sur son jumeau, *le Titanic.* Le 14 avril 1912, iceberg. "
              "Elle s'en sort dans le canot numéro 16.", illus=ill_titanic, dur=4.0),
    dict(text="Pendant la guerre, elle est infirmière sur le troisième, *le Britannic.* "
              "Il heurte une mine en 1916. Elle saute à l'eau et survit, blessée à la tête.",
         illus=ill_britannic, dur=4.6),
    dict(text="Elle a continué à travailler en mer jusqu'en 1950. "
              "Elle est morte en 1971, à 83 ans, *sur la terre ferme.*", dur=3.6),
]

if __name__ == "__main__":
    import sys
    todo = sys.argv[1:] or ["flamant", "capuchon", "jessop"]
    if "flamant" in todo:
        render("2026-10-19-flamants", FLAMANT)
    if "capuchon" in todo:
        render("2026-10-21-capuchon", CAPUCHON)
    if "jessop" in todo:
        render("2026-10-22-violet-jessop", JESSOP)
