"""Semaine 1 : les trois carrousels."""
import math
import os
from PIL import ImageDraw
from pls import slide, layer, INK, ACCENT, BG, LINE, MUTED, REPO

OUT = f"{REPO}/posts"


# ---------- illustrations (dessinées à x2) ----------

def ill_arche(W, H):
    im, d = layer(W, H)
    cx, R = W // 2, int(H * 0.30)
    cy = int(H * 0.42)
    ground = int(H * 0.96)
    # alfiz, le cadre rectangulaire autour de l'arc
    fw = int(R * 1.45)
    d.rectangle((cx - fw, cy - int(R * 1.3), cx + fw, ground), outline=LINE, width=10)

    def arch(r, fill, outline, width):
        pts = []
        for a in range(160, 381, 2):
            t = math.radians(a)
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
        x1, x2 = pts[0][0], pts[-1][0]
        poly = [(x1, ground)] + pts + [(x2, ground)]
        d.polygon(poly, fill=fill)
        d.line(pts, fill=outline, width=width, joint="curve")
        d.line((x1, pts[0][1], x1, ground), fill=outline, width=width)
        d.line((x2, pts[-1][1], x2, ground), fill=outline, width=width)

    # frise de losanges façon zellige au pied
    s = 26
    for i in range(-9, 10):
        x = cx + i * s * 2.2
        y = ground - 40
        d.polygon([(x, y - s), (x + s, y), (x, y + s), (x - s, y)],
                  fill=ACCENT if i % 3 == 0 else LINE)
    arch(R, (28, 27, 30), ACCENT, 16)
    arch(int(R * 0.80), BG, (110, 84, 40), 6)
    return im


def ill_vague(W, H):
    im, d = layer(W, H)
    ground = int(H * 0.96)
    # immeubles du port
    xs = [(0.04, 0.48), (0.17, 0.62), (0.30, 0.40), (0.42, 0.70), (0.58, 0.52),
          (0.71, 0.66), (0.84, 0.44)]
    for i, (x, h) in enumerate(xs):
        x0 = int(W * x)
        x1 = x0 + int(W * 0.12)
        y0 = ground - int(H * h)
        d.rectangle((x0, y0, x1, ground), fill=(34, 33, 37))
        for wy in range(y0 + 40, ground - 60, 70):
            for wx in range(x0 + 30, x1 - 30, 60):
                d.rectangle((wx, wy, wx + 24, wy + 34), fill=(52, 50, 56))
    # la vague
    pts = []
    for i in range(0, 101):
        x = W * 1.05 * i / 100
        crest = 0.62 * H * math.exp(-((x - W * 0.38) / (W * 0.20)) ** 2)
        slope = 0.20 * H * max(0, 1 - x / (W * 0.95))
        pts.append((x, ground - crest - slope))
    poly = [(0, ground)] + pts + [(W * 1.05, ground)]
    d.polygon(poly, fill=(86, 49, 17))
    d.line(pts, fill=ACCENT, width=12, joint="curve")
    # coulures
    for x, l in [(0.30, 0.18), (0.44, 0.26), (0.52, 0.12)]:
        px = int(W * x)
        py = ground - int(0.30 * H)
        d.rounded_rectangle((px - 10, py, px + 10, py + int(H * l)), radius=10, fill=(110, 66, 24))
    d.line((0, ground, W, ground), fill=LINE, width=6)
    return im


def ill_pigeon(W, H):
    im, d = layer(W, H)
    u = H / 10
    cx, cy = W * 0.50, H * 0.55
    wing = (196, 192, 184)
    tail = (150, 147, 141)
    # queue
    d.polygon([(cx - 2.2 * u, cy - 0.2 * u), (cx - 4.6 * u, cy + 0.6 * u),
               (cx - 4.4 * u, cy + 1.4 * u), (cx - 1.8 * u, cy + 1.0 * u)], fill=tail)
    # corps
    d.ellipse((cx - 2.8 * u, cy - 1.3 * u, cx + 1.8 * u, cy + 1.6 * u), fill=INK)
    # cou
    d.polygon([(cx + 0.4 * u, cy - 1.1 * u), (cx + 1.4 * u, cy - 2.6 * u),
               (cx + 2.6 * u, cy - 2.2 * u), (cx + 1.8 * u, cy + 0.2 * u)], fill=INK)
    # tête
    hx, hy, hr = cx + 2.0 * u, cy - 2.6 * u, 0.85 * u
    d.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=INK)
    d.polygon([(hx + 0.7 * u, hy - 0.15 * u), (hx + 1.5 * u, hy + 0.15 * u),
               (hx + 0.7 * u, hy + 0.35 * u)], fill=MUTED)
    d.ellipse((hx + 0.15 * u, hy - 0.35 * u, hx + 0.45 * u, hy - 0.05 * u), fill=BG)
    # aile
    d.polygon([(cx - 1.6 * u, cy - 0.9 * u), (cx + 1.0 * u, cy - 0.7 * u),
               (cx + 0.6 * u, cy + 0.6 * u), (cx - 3.4 * u, cy + 0.9 * u)], fill=wing)
    for k in range(3):
        y = cy - 0.2 * u + k * 0.35 * u
        d.line((cx - 2.6 * u + k * 0.3 * u, y + 0.5 * u, cx + 0.5 * u, y), fill=tail, width=8)
    # pattes et tube du message
    for dx in (-0.2, 0.5):
        x = cx + dx * u
        d.line((x, cy + 1.4 * u, x, cy + 2.7 * u), fill=MUTED, width=14)
    d.rounded_rectangle((cx + 0.30 * u, cy + 1.75 * u, cx + 0.72 * u, cy + 2.45 * u),
                        radius=12, fill=ACCENT)
    d.line((0.12 * W, cy + 2.75 * u, 0.88 * W, cy + 2.75 * u), fill=LINE, width=6)
    return im


# ---------- contenus ----------

TANGER = dict(slug="2026-10-19-legation-tanger", label="Patrimoine marocain", slides=[
    dict(illus=ill_arche,
         title="Le seul monument historique américain hors des États-Unis est *au Maroc.*"),
    dict(big="1777",
         body="Les États-Unis viennent tout juste de proclamer leur indépendance. "
              "Presque personne au monde ne les reconnaît encore."),
    dict(body="Le sultan *Mohammed ben Abdallah* ouvre pourtant les ports marocains aux navires américains.\n\n"
              "Le Maroc devient l'un des tout premiers pays à reconnaître la jeune nation."),
    dict(big="1786",
         body="Les deux pays signent un traité de paix et d'amitié. "
              "Il est *toujours en vigueur*, ce qui en fait l'un des plus durables de l'histoire américaine."),
    dict(big="1821",
         body="Le sultan *Moulay Slimane* offre aux Américains une maison dans la médina de Tanger. "
              "C'est le premier bâtiment que les États-Unis possèdent pour une mission diplomatique."),
    dict(body="Elle restera un poste diplomatique pendant *140 ans*.\n\n"
              "Pendant la Seconde Guerre mondiale, les services de renseignement américains "
              "y préparent leurs opérations en Afrique du Nord."),
    dict(body="En 1982, elle est classée *National Historic Landmark*. "
              "La seule au monde située hors du sol américain.\n\n"
              "C'est aujourd'hui un musée et une bibliothèque, en plein cœur de la médina.",
         footer="La prochaine fois que tu passes à Tanger, tu sais où aller."),
])

MELASSE = dict(slug="2026-10-21-melasse-boston", label="Histoire vraie", slides=[
    dict(illus=ill_vague,
         title="En 1919, une vague a tué 21 personnes à Boston. *Ce n'était pas de l'eau.*"),
    dict(body="*15 janvier 1919*, vers midi et demi, dans le quartier de North End.\n\n"
              "Après plusieurs jours de grand froid, le thermomètre remonte enfin au-dessus de 4 degrés."),
    dict(body="Près du port se dresse une cuve géante appartenant à une distillerie.\n\n"
              "À l'intérieur, *8,7 millions de litres de mélasse*, le sirop noir et épais tiré de la canne à sucre."),
    dict(big="8 m",
         body="D'un coup, la cuve cède. Une vague brune haute comme un immeuble de trois étages "
              "déferle dans les rues, jusqu'à *56 km/h* selon les estimations."),
    dict(body="Le vrai piège, c'est la texture. En refroidissant, la mélasse s'épaissit "
              "et colle comme du goudron.\n\n"
              "Bilan : *21 morts* et environ 150 blessés."),
    dict(body="Les secours fouillent pendant quatre jours. L'eau du port reste brune jusqu'à l'été.\n\n"
              "119 habitants attaquent l'entreprise en justice. Trois ans plus tard, "
              "elle est jugée responsable et doit payer *628 000 dollars*."),
    dict(body="Le détail le plus étrange vient après.\n\n"
              "Pendant des décennies, les habitants ont juré que par les chaudes journées d'été, "
              "le quartier *sentait encore la mélasse.*",
         footer="Boston, 15 janvier 1919. Une date que la ville n'a jamais vraiment digérée."),
])

CHERAMI = dict(slug="2026-10-23-cher-ami", label="Histoire vraie", slides=[
    dict(illus=ill_pigeon,
         title="Ce pigeon aurait sauvé 194 soldats. *Tout le problème est dans le « aurait ».*"),
    dict(body="*Octobre 1918*, forêt d'Argonne.\n\n"
              "Plus de 500 soldats américains se retrouvent encerclés. "
              "L'histoire les retiendra sous le nom de *bataillon perdu*."),
    dict(body="Pire encore, leur propre artillerie les pilonne par erreur.\n\n"
              "Pas de radio. Leur dernier moyen de prévenir l'arrière, ce sont les pigeons voyageurs."),
    dict(body="Selon la légende, le dernier oiseau, *Cher Ami*, s'envole sous les balles. "
              "Touché à la poitrine, une patte presque arrachée, il atteint quand même son pigeonnier."),
    dict(body="Le message, en substance : notre artillerie nous tire dessus, pour l'amour du ciel, arrêtez.\n\n"
              "Les tirs cessent. À l'arrivée des secours, seuls *194 hommes* repartent à pied."),
    dict(body="Cher Ami reçoit la *Croix de guerre* française. Il meurt de ses blessures en juin 1919.\n\n"
              "Depuis 1921, il est exposé, naturalisé, au musée national d'histoire américaine à Washington."),
    dict(body="Sauf que le conservateur du musée lui-même le reconnaît : *aucune preuve solide* "
              "ne relie Cher Ami au bataillon perdu. Les archives de l'armée placent sa blessure plus tard dans le mois.\n\n"
              "On a même attendu 2021 et un test ADN pour être sûr que c'était un mâle.",
         footer="Héros ou légende, il reste le pigeon le plus célèbre de l'histoire."),
])


def build(post):
    folder = f"{OUT}/{post['slug']}"
    os.makedirs(folder, exist_ok=True)
    total = len(post["slides"])
    for i, s in enumerate(post["slides"], 1):
        img = slide(i, total, post["label"], s.get("body"), big=s.get("big"),
                    illus=s.get("illus"), title=s.get("title"), footer=s.get("footer"))
        img.save(f"{folder}/{i:02d}.jpg", quality=92, optimize=True)
    print("ok", folder)


if __name__ == "__main__":
    for p in (TANGER, MELASSE, CHERAMI):
        build(p)
