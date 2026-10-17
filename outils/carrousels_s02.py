"""Lot 2 : carrousels Ibn Battuta et vol de la Joconde."""
import math
from pls import layer, INK, ACCENT, BG, LINE, MUTED
from carrousels_s01 import build


def ill_globe(W, H):
    im, d = layer(W, H)
    cx, cy, r = W // 2, int(H * 0.50), int(H * 0.40)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(26, 26, 30), outline=LINE, width=8)
    for k in range(1, 4):
        ry = int(r * k / 4)
        d.arc((cx - r, cy - ry, cx + r, cy + ry), 0, 360, fill=LINE, width=5)
    for k in (-2, -1, 1, 2):
        rx = int(r * abs(k) / 3)
        d.ellipse((cx - rx, cy - r, cx + rx, cy + r), outline=LINE, width=5)
    d.line((cx, cy - r, cx, cy + r), fill=LINE, width=5)
    d.line((cx - r, cy, cx + r, cy), fill=LINE, width=5)
    # itinéraire en pointillés, de l'ouest vers l'est puis retour vers le sud
    pts = [(-0.78, -0.12), (-0.45, 0.02), (-0.15, -0.20), (0.15, -0.05), (0.45, 0.12),
           (0.70, -0.10), (0.40, 0.30), (-0.10, 0.25), (-0.55, 0.38)]
    pts = [(cx + x * r, cy + y * r) for x, y in pts]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        n = int(math.hypot(x2 - x1, y2 - y1) / 34)
        for i in range(n):
            if i % 2 == 0:
                a, b = i / n, (i + 1) / n
                d.line((x1 + (x2 - x1) * a, y1 + (y2 - y1) * a,
                        x1 + (x2 - x1) * b, y1 + (y2 - y1) * b), fill=ACCENT, width=10)
    for x, y in pts[1:-1]:
        d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=INK)
    x, y = pts[0]
    d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=ACCENT)
    return im


def ill_cadre_vide(W, H):
    im, d = layer(W, H)
    cx, cy = W // 2, int(H * 0.52)
    # mur
    d.rectangle((int(W * 0.08), int(H * 0.04), int(W * 0.92), int(H * 0.98)), fill=(28, 27, 31))
    w, h = int(H * 0.36), int(H * 0.52)
    # trace plus claire laissée par le tableau
    d.rectangle((cx - w, cy - h, cx + w, cy + h), fill=(40, 39, 44))
    # les quatre crochets
    for px, py in ((-0.75, -0.85), (0.75, -0.85), (-0.75, 0.85), (0.75, 0.85)):
        x, y = cx + px * w, cy + py * h
        d.rounded_rectangle((x - 16, y - 40, x + 16, y + 40), radius=10, fill=ACCENT)
    # cartel
    d.rectangle((cx - 120, cy + h + 40, cx + 120, cy + h + 90), fill=MUTED)
    return im


IBN = dict(slug="2026-10-18-ibn-battuta", label="Patrimoine marocain", slides=[
    dict(illus=ill_globe,
         title="En 1325, un Tangérois de 21 ans quitte sa ville. *Il ne reverra le Maroc que 24 ans plus tard.*"),
    dict(body="Il s'appelle *Ibn Battuta*. Il est né à Tanger en 1304.\n\n"
              "En juin 1325, il part vers l'est, seul, à 21 ans. "
              "Il deviendra l'un des plus grands voyageurs de l'histoire."),
    dict(big="120 000 km",
         body="C'est la distance qu'il aurait parcourue en une trentaine d'années. "
              "Environ trois fois le tour de la Terre, sans train ni moteur."),
    dict(body="L'Égypte, la Perse, l'Anatolie, l'Asie centrale.\n\n"
              "Puis il pousse jusqu'en *Inde*, passe par les *Maldives* et dit être allé jusqu'en *Chine*."),
    dict(body="À Delhi, le sultan le nomme juge. Aux Maldives, il exerce encore comme juge.\n\n"
              "Un jeune homme parti de Tanger se retrouve à rendre la justice à l'autre bout du monde."),
    dict(body="De retour au Maroc, il repart. D'abord en Andalousie, puis à travers le Sahara "
              "jusqu'à l'empire du *Mali* et Tombouctou."),
    dict(body="Dans les années 1350, le sultan du Maroc lui demande de tout raconter. "
              "Il dicte ses souvenirs au lettré Ibn Juzayy.\n\n"
              "Le récit, la *Rihla*, reste une source majeure sur le monde du XIVe siècle.",
         footer="Si tu as déjà atterri à Tanger, tu le connais : l'aéroport porte son nom."),
])

JOCONDE = dict(slug="2026-10-20-joconde", label="Histoire vraie", slides=[
    dict(illus=ill_cadre_vide,
         title="En 1911, des foules entières sont venues au Louvre *pour regarder un mur vide.*"),
    dict(body="*Lundi 21 août 1911*, vers 7 heures du matin. Le Louvre est fermé ce jour-là, "
              "les salles sont presque désertes."),
    dict(body="Un homme en blouse blanche, comme les employés, décroche un tableau de ses crochets. "
              "Il se débarrasse du cadre dans un escalier et ressort par une porte de service."),
    dict(body="Le vol n'est remarqué que le lendemain, par un peintre venu copier l'œuvre. "
              "Le tableau, c'est *la Joconde.*"),
    dict(body="L'enquête s'emballe. Le poète *Apollinaire* est arrêté, Picasso est interrogé.\n\n"
              "Le vrai voleur, Vincenzo Peruggia, un vitrier qui avait travaillé au musée, est questionné "
              "par la police. Elle le laisse repartir."),
    dict(body="Pendant plus de deux ans, la Joconde dort dans une malle, dans sa chambre à Paris.\n\n"
              "En décembre 1913, Peruggia tente de la vendre à un marchand d'art de Florence. "
              "Le marchand prévient la police."),
    dict(body="Le tableau était déjà célèbre. Mais plus de deux ans de mystère, racontés par les journaux du monde entier, "
              "en ont fait *l'une des œuvres les plus connues de la planète.*\n\n"
              "À Florence, des milliers de personnes se pressent pour la revoir.",
         footer="Ce vol a peut-être été la meilleure publicité de la Joconde."),
])

if __name__ == "__main__":
    build(IBN)
    build(JOCONDE)
