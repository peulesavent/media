"""Lot 4 : 5 Reels courts et 4 carrousels de 8 visuels."""
import math
import sys
import reels_s01
from PIL import Image
from pls import font, layer, FONT_BLACK, INK, ACCENT, BG, LINE, MUTED
from reels_s01 import render, ease, _canvas, _done
from carrousels_s01 import build

# Reels plus nerveux : carte de fin plus courte
reels_s01.OUTRO = 2.0

RED = (214, 72, 72)
BLUE = (60, 120, 210)
SKY = (110, 170, 230)
GREEN = (98, 160, 92)
SAND = (214, 178, 112)
BROWN = (130, 96, 64)
WHITE = (240, 238, 232)


def mix(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def label(d, x, y, txt, size=64, col=INK):
    d.text((x, y), txt, font=font(FONT_BLACK, size), fill=col, anchor="mm")


def cta(text):
    return dict(body=text, footer="Suis *@peulesavent* pour la suite.")


# ================= REELS =================

# --- Loutres ---
def otter(d, x, y, s, col=(120, 88, 62)):
    d.ellipse((x - 260 * s, y - 70 * s, x + 260 * s, y + 70 * s), fill=col)
    d.ellipse((x + 190 * s, y - 95 * s, x + 330 * s, y + 45 * s), fill=mix(col, WHITE, 0.45))
    d.ellipse((x + 255 * s, y - 50 * s, x + 275 * s, y - 30 * s), fill=BG)
    d.ellipse((x + 300 * s, y - 25 * s, x + 322 * s, y - 5 * s), fill=BG)


def ill_otters(mode):
    def f(t):
        im, d, w, h = _canvas()
        wy = h + 120
        d.rectangle((0, wy, 2 * w, 2 * h), fill=(24, 44, 66))
        bob = 14 * math.sin(t * 8)
        if mode in ("pair", "hands"):
            otter(d, w - 360, wy - 20 + bob, 1.0)
            otter(d, w + 360, wy - 20 - bob, 1.0)
            if mode == "hands":
                d.line((w - 120, wy - 40, w + 120, wy - 40), fill=ACCENT, width=26)
        elif mode == "kelp":
            for k in range(7):
                x = 220 + k * 270
                pts = [(x + 40 * math.sin(i / 4 + t * 3 + k), wy - 40 + i * 30) for i in range(26)]
                d.line(pts, fill=GREEN, width=26, joint="curve")
            otter(d, w, wy - 20 + bob, 1.1)
            d.arc((w - 300, wy - 120, w + 300, wy + 80), 200, 340, fill=GREEN, width=30)
        elif mode == "aquarium":
            d.rectangle((140, 140, 2 * w - 140, 2 * h - 60), outline=SKY, width=18)
            otter(d, w - 360, wy - 20 + bob, 1.0)
            otter(d, w + 360, wy - 20 - bob, 1.0)
            d.line((w - 120, wy - 40, w + 120, wy - 40), fill=ACCENT, width=26)
        return _done(im)
    return f


LOUTRES = [
    dict(text="Les loutres ne dorment pas *main dans la main.*", hook=True,
         illus=ill_otters("hands"), dur=2.8),
    dict(text="Dans la nature, elles s'enroulent dans *les algues géantes* pour ne pas dériver.",
         illus=ill_otters("kelp"), dur=3.2),
    dict(text="Les célèbres vidéos de loutres main dans la main ont été filmées *en aquarium.*",
         illus=ill_otters("aquarium"), dur=3.2),
    dict(text="Ce qui est vrai : elles se reposent souvent *en groupe*, qu'on appelle un radeau.",
         illus=ill_otters("pair"), dur=3.0),
]


# --- Éclair ---
def ill_bolt(mode):
    def f(t):
        im, d, w, h = _canvas()
        if mode in ("bolt", "both"):
            x0 = w - (380 if mode == "both" else 0)
            flash = 1 if (t * 6) % 1 < 0.6 else 0.4
            k = 0.72 if mode == "both" else 1.0
            pts = [(x0, 120), (x0 - 120, 640), (x0 + 40, 640), (x0 - 140, 1300), (x0 + 220, 520),
                   (x0 + 40, 520), (x0 + 160, 120)]
            pts = [(x, 120 + (y - 120) * k) for x, y in pts]
            d.polygon(pts, fill=mix(BG, (250, 236, 150), flash))
        if mode in ("sun", "both"):
            cx = w + (380 if mode == "both" else 0)
            d.ellipse((cx - 300, h - 300, cx + 300, h + 300), fill=ACCENT)
        if mode == "both":
            label(d, w - 380, h + 560, "≈ 27 700 °C", 96, (250, 236, 150))
            label(d, w + 380, h + 560, "≈ 5 500 °C", 96, ACCENT)
        return _done(im)
    return f


ECLAIR = [
    dict(text="Un éclair : *5 fois plus chaud* que la surface du Soleil.", hook=True,
         illus=ill_bolt("both"), dur=3.0),
    dict(text="L'air qu'il traverse peut atteindre *environ 27 700 °C.*", illus=ill_bolt("bolt"), dur=2.8),
    dict(text="La surface du Soleil, elle, tourne autour de *5 500 °C.*", illus=ill_bolt("sun"), dur=2.8),
    dict(text="Cette chaleur brutale dilate l'air d'un coup. *Le tonnerre*, c'est ce bruit-là.",
         illus=ill_bolt("bolt"), dur=3.2),
]


# --- Crevette ---
def shrimp(d, w, h, glow=0.0):
    col = (236, 128, 96)
    dark = (200, 100, 74)
    cx, cy, R = w + 60, h - 20, 380
    # abdomen en C : segments de plus en plus petits jusqu'à la queue
    segs = []
    for i in range(7):
        a = math.radians(170 - i * 30)
        r = 150 - i * 15
        segs.append((cx + math.cos(a) * R, cy + math.sin(a) * R * 0.85, r))
    for x, y, r in reversed(segs[1:]):
        d.ellipse((x - r, y - r, x + r, y + r), fill=col, outline=dark, width=6)
    # éventail de la queue
    x, y, r = segs[-1]
    d.polygon([(x, y), (x + 220, y - 150), (x + 260, y - 20)], fill=dark)
    d.polygon([(x, y), (x + 260, y - 20), (x + 200, y + 120)], fill=col)
    # céphalothorax (la "tête")
    hx, hy, _ = segs[0]
    d.ellipse((hx - 300, hy - 200, hx + 150, hy + 150), fill=col, outline=dark, width=6)
    d.polygon([(hx - 280, hy - 60), (hx - 470, hy - 130), (hx - 290, hy - 10)], fill=dark)
    for k in range(3):
        d.line((hx - 260, hy - 80 + k * 26, hx - 860, hy - 520 + k * 80), fill=col, width=9)
    for k in range(5):
        x0 = hx - 180 + k * 60
        d.line((x0, hy + 130, x0 - 20, hy + 300), fill=dark, width=10)
    d.ellipse((hx - 220, hy - 140, hx - 160, hy - 80), fill=BG)
    if glow:
        r = 58 + 14 * math.sin(glow * 12)
        gx, gy = hx - 30, hy - 40
        d.ellipse((gx - r, gy - r, gx + r, gy + r), fill=RED, outline=ACCENT, width=10)


CREVETTE = [
    dict(text="Tu jettes le cœur de la crevette *sans le savoir.*", hook=True,
         illus=lambda t: _shrimp_frame(t, True), dur=2.8),
    dict(text="Il est dans ce qu'on appelle sa tête : *le céphalothorax*, la tête et le thorax soudés.",
         illus=lambda t: _shrimp_frame(t, False), dur=3.6),
    dict(text="Sous la carapace, on y trouve le cœur, mais aussi *l'estomac.*",
         illus=lambda t: _shrimp_frame(t, True), dur=3.0),
    dict(text="Alors la prochaine fois que tu décortiques une crevette, *pense à ce que tu jettes.*",
         illus=lambda t: _shrimp_frame(t, False), dur=3.2),
]


def _shrimp_frame(t, glow):
    im, d, w, h = _canvas()
    shrimp(d, w, h, t if glow else 0.0)
    return _done(im)


# --- Chèvres dans l'arganier ---
def argan(d, w, h, goats=3, rope=False):
    gy = int(h * 1.7)
    d.rectangle((w - 50, gy - 520, w + 50, gy), fill=BROWN)
    d.line((w, gy - 420, w - 360, gy - 700), fill=BROWN, width=50)
    d.line((w, gy - 420, w + 380, gy - 720), fill=BROWN, width=50)
    d.ellipse((w - 760, gy - 1180, w + 760, gy - 560), fill=(70, 120, 60))
    spots = [(-380, -760), (260, -820), (-40, -980), (480, -660)][:goats]
    for x, y in spots:
        gx, gy2 = w + x, gy + y
        d.ellipse((gx - 110, gy2 - 60, gx + 110, gy2 + 60), fill=WHITE)
        d.ellipse((gx + 80, gy2 - 110, gx + 170, gy2 - 20), fill=WHITE)
        d.line((gx + 120, gy2 - 110, gx + 150, gy2 - 170), fill=MUTED, width=12)
        for lx in (-70, -20, 40, 80):
            d.line((gx + lx, gy2 + 50, gx + lx, gy2 + 120), fill=MUTED, width=12)
    if rope:
        x, y = w - 380, gy - 760
        d.line((x, y + 60, w, gy - 300), fill=ACCENT, width=12)
    d.line((0, gy, 2 * w, gy), fill=SAND, width=10)


def ill_argan(goats=3, rope=False):
    def f(t):
        im, d, w, h = _canvas()
        argan(d, w, h - 120, goats, rope)
        return _done(im)
    return f


CHEVRES = [
    dict(text="Au Maroc, les chèvres grimpent dans les arbres. *Vraiment.*", hook=True,
         illus=ill_argan(3), dur=2.8),
    dict(text="Elles montent dans les *arganiers* pour manger les feuilles et les fruits.",
         illus=ill_argan(2), dur=3.0),
    dict(text="En ruminant, elles recrachent les noyaux. Elles aident à *disperser les graines.*",
         illus=ill_argan(2), dur=3.6),
    dict(text="Mais au bord des routes touristiques, certaines sont *installées et attachées* "
              "pour les photos.",
         illus=ill_argan(3, rope=True), dur=4.2),
]


# --- Étoile à neutrons ---
def ill_neutron(mode):
    def f(t):
        im, d, w, h = _canvas()
        if mode == "star":
            for k in range(3):
                r = 160 + k * 120 + 30 * math.sin(t * 6 + k)
                d.ellipse((w - r, h - r, w + r, h + r), outline=mix(SKY, BG, k / 3), width=10)
            d.ellipse((w - 140, h - 140, w + 140, h + 140), fill=WHITE)
            a = t * 8
            for s in (1, -1):
                d.line((w, h, w + s * math.cos(a) * 700, h + s * math.sin(a) * 700), fill=SKY, width=16)
        elif mode == "sugar":
            d.rectangle((w - 140, h - 140, w + 140, h + 140), fill=WHITE)
            label(d, w, h + 330, "≈ 1 milliard de tonnes", 96, ACCENT)
        elif mode == "city":
            for k in range(12):
                x = 200 + k * 150
                hh = 180 + (k * 97) % 320
                d.rectangle((x, h + 300 - hh, x + 110, h + 300), fill=LINE)
            d.ellipse((w - 520, h - 500, w + 520, h + 540), outline=ACCENT, width=14)
            label(d, w, h + 440, "≈ 20 km", 96, ACCENT)
        return _done(im)
    return f


NEUTRON = [
    dict(text="Ce morceau de sucre pèserait *un milliard de tonnes.*", hook=True,
         illus=ill_neutron("sugar"), dur=3.2),
    dict(text="C'est une *étoile à neutrons* : le cœur écrasé d'une étoile géante après son explosion.",
         illus=ill_neutron("star"), dur=3.4),
    dict(text="Plus lourde que le Soleil, mais compressée dans une boule *d'environ 20 km.*",
         illus=ill_neutron("city"), dur=3.2),
    dict(text="Sur Terre, selon la NASA, un morceau de sucre de sa matière pèserait *autant qu'une montagne.*",
         illus=ill_neutron("sugar"), dur=3.4),
]


# ================= CARROUSELS =================

def ill_cities(W, H):
    im, d = layer(W, H)
    gy = int(H * 0.9)
    for cx, name in ((W * 0.28, "HIROSHIMA"), (W * 0.72, "NAGASAKI")):
        d.ellipse((cx - 22, gy - 22, cx + 22, gy + 22), fill=ACCENT)
        d.text((cx, gy + 90), name, font=font(FONT_BLACK, 64), fill=INK, anchor="mm")
    pts = [(W * 0.28, gy), (W * 0.5, gy - 520), (W * 0.72, gy)]
    d.line([(W * 0.28 + (W * 0.44) * i / 40, gy - 520 * math.sin(math.pi * i / 40)) for i in range(41)],
           fill=MUTED, width=10)
    d.text((W * 0.5, gy - 610), "6 AOÛT   >   9 AOÛT 1945", font=font(FONT_BLACK, 60), fill=MUTED, anchor="mm")
    return im


def ill_jungle(W, H):
    im, d = layer(W, H)
    gy = int(H * 0.95)
    for k in range(9):
        x = 80 + k * 250
        d.line((x, gy, x + 20, gy - 600 - (k % 3) * 120), fill=(60, 90, 50), width=30)
        for j in range(4):
            yy = gy - 300 - j * 120 - (k % 3) * 60
            d.ellipse((x - 160, yy - 50, x + 200, yy + 50), fill=(56, 110, 60))
    d.text((W // 2, int(H * 0.2)), "1944   >   1974", font=font(FONT_BLACK, 110), fill=ACCENT, anchor="mm")
    return im


def ill_dance(W, H):
    im, d = layer(W, H)
    gy = int(H * 0.92)
    for k in range(7):
        x = 220 + k * 290
        y = gy - 60
        a = math.sin(k * 1.7)
        d.ellipse((x - 46, y - 520, x + 46, y - 428), fill=INK)
        d.line((x, y - 430, x + 40 * a, y - 220), fill=INK, width=26)
        d.line((x + 40 * a, y - 220, x - 90, y), fill=INK, width=24)
        d.line((x + 40 * a, y - 220, x + 100, y - 20), fill=INK, width=24)
        d.line((x, y - 380, x - 120, y - 520 + 80 * a), fill=INK, width=20)
        d.line((x, y - 380, x + 130, y - 470 - 60 * a), fill=INK, width=20)
    d.line((60, gy, W - 60, gy), fill=LINE, width=8)
    d.text((W // 2, int(H * 0.12)), "STRASBOURG, 1518", font=font(FONT_BLACK, 90), fill=ACCENT, anchor="mm")
    return im


def ill_blue(W, H):
    im, d = layer(W, H)
    gy = int(H * 0.95)
    blues = [(70, 120, 200), (100, 150, 220), (50, 100, 180), (130, 175, 230)]
    for k in range(10):
        x = 60 + k * 215
        hh = 280 + (k * 131) % 360
        col = blues[k % 4]
        d.rectangle((x, gy - hh, x + 200, gy), fill=col)
        d.rectangle((x + 70, gy - 150, x + 130, gy), fill=mix(col, BG, 0.4))
        d.pieslice((x + 70, gy - 180, x + 130, gy - 120), 180, 360, fill=mix(col, BG, 0.4))
    d.ellipse((W - 420, 60, W - 220, 260), fill=ACCENT)
    return im


YAMAGUCHI = dict(slug="2026-10-27-yamaguchi", label="Histoire vraie", slides=[
    dict(illus=ill_cities, title="Il a survécu à Hiroshima. *Trois jours plus tard, il était à Nagasaki.*"),
    dict(body="Il s'appelle *Tsutomu Yamaguchi.* Ingénieur chez Mitsubishi, il vit et travaille à Nagasaki."),
    dict(body="*6 août 1945.* Il est à Hiroshima pour le travail, à moins de 3 km du point d'explosion. "
              "Gravement brûlé au haut du corps, les tympans percés."),
    dict(body="Il passe la nuit dans un abri, puis prend le train. *Direction : chez lui, à Nagasaki.*"),
    dict(body="*9 août.* Couvert de bandages, il retourne au travail. Il raconte Hiroshima à son chef, "
              "qui ne le croit pas. À cet instant, la deuxième bombe explose."),
    dict(body="Encore à environ 3 km. Le souffle l'épargne, mais il *tombe gravement malade* les jours suivants."),
    dict(body="D'autres personnes ont vécu les deux bombardements. Mais en 2009, il devient "
              "*le seul reconnu officiellement* par le Japon comme survivant des deux. "
              "Il meurt en 2010, à 93 ans."),
    cta("Envoie ce post à quelqu'un qui aime les histoires vraies qu'on n'apprend pas à l'école."),
])

ONODA = dict(slug="2026-10-29-onoda", label="Histoire vraie", slides=[
    dict(illus=ill_jungle, title="La guerre s'est terminée en 1945. *Lui s'est rendu en 1974.*"),
    dict(body="*Hiroo Onoda*, officier japonais, débarque en 1944 sur l'île de Lubang, aux Philippines. "
              "Ses ordres : tenir, ne jamais se rendre."),
    dict(body="En 1945, des tracts annoncent la fin de la guerre. Il les voit. "
              "Il croit à *une ruse de l'ennemi.*"),
    dict(body="Les années passent. Ses compagnons se rendent ou sont tués. "
              "À partir de 1972, *il est seul.*"),
    dict(body="Pendant ces années, son groupe vole les récoltes et attaque des habitants. "
              "Il est accusé d'avoir tué jusqu'à *une trentaine de civils.* Une part sombre souvent oubliée."),
    dict(body="En 1974, un jeune aventurier japonais le retrouve. Onoda refuse de partir "
              "sans l'ordre de *son supérieur.*"),
    dict(body="Son ancien commandant, devenu libraire, fait le voyage. *Le 9 mars 1974*, il lui ordonne "
              "de cesser le combat. Le lendemain, Onoda se rend, en uniforme."),
    cta("Envoie ça à quelqu'un qui pense tout savoir sur la Seconde Guerre mondiale."),
])

STRASBOURG = dict(slug="2026-10-30-strasbourg-1518", label="Histoire vraie", slides=[
    dict(illus=ill_dance, title="En 1518, des centaines de Strasbourgeois se sont mis à danser. *Sans pouvoir s'arrêter.*"),
    dict(body="*Strasbourg, juillet 1518.* Une femme, Frau Troffea selon les chroniques, "
              "se met à danser seule dans la rue. Sans musique."),
    dict(body="Elle danse *pendant plusieurs jours.* En une semaine, plus de trente personnes l'ont rejointe."),
    dict(body="La réponse des autorités surprend : faire danser les malades jusqu'à la guérison. "
              "On monte *des estrades*, on paie *des musiciens.*"),
    dict(body="Ça ne marche pas. Les danseurs se multiplient. "
              "*Des dizaines*, jusqu'à 400 selon une chronique de l'époque."),
    dict(body="La ville interdit alors la musique et la danse en public. Les malades sont conduits "
              "à un sanctuaire près de Saverne. *Début septembre, tout s'arrête.*"),
    dict(body="Pourquoi ? On pense aujourd'hui à une *hystérie collective*, dans une ville épuisée "
              "par la famine et les maladies. Le nombre de morts, lui, reste inconnu."),
    cta("Envoie ça à la personne qui ne s'arrête jamais de danser."),
])

CHEFCHAOUEN = dict(slug="2026-10-28-chefchaouen", label="Patrimoine marocain", slides=[
    dict(illus=ill_blue, title="Chefchaouen est bleue. *Et personne ne sait vraiment pourquoi.*"),
    dict(big="1471",
         body="La ville est fondée dans les montagnes du Rif, comme petite forteresse face aux incursions portugaises."),
    dict(body="Elle accueille ensuite des familles *andalouses*, musulmanes et juives, chassées de la péninsule Ibérique."),
    dict(body="Explication la plus répandue : des familles juives auraient peint en bleu, "
              "*couleur du ciel*, dans les années 1930."),
    dict(body="D'autres disent que le bleu *éloigne les moustiques*, ou qu'il garde les maisons *plus fraîches.* "
              "Aucune preuve dans un cas comme dans l'autre."),
    dict(body="Des habitants racontent aussi que le bleu s'est généralisé plus tard, *pour attirer les visiteurs.* "
              "Plausible, mais pas documenté."),
    dict(body="Chaque printemps, les habitants *repeignent* leurs murs. "
              "Et le mystère reste entier."),
    cta("Envoie ce post à quelqu'un qui rêve d'aller à Chefchaouen."),
])

REELS = {
    "loutres": ("2026-10-26-loutres", LOUTRES),
    "eclair": ("2026-10-27-eclair", ECLAIR),
    "crevette": ("2026-10-28-crevette", CREVETTE),
    "chevres": ("2026-10-29-chevres-argan", CHEVRES),
    "neutron": ("2026-10-30-etoile-neutrons", NEUTRON),
}
CARROUSELS = {"yamaguchi": YAMAGUCHI, "onoda": ONODA, "strasbourg": STRASBOURG, "chefchaouen": CHEFCHAOUEN}

if __name__ == "__main__":
    for k in sys.argv[1:]:
        if k in REELS:
            render(*REELS[k])
        elif k in CARROUSELS:
            build(CARROUSELS[k])
