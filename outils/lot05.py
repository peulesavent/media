"""Lot 5 : gabarit Reel photo.

- Les 6 carrousels encore programmés (22 au 30/10) passent en Reels courts.
  Les carrousels restent en archive dans le même dossier (01.jpg...).
- Lot 5 à partir du 31/10 : 10 Reels et 1 carrousel à enregistrer.
"""
import sys
from reel_photo import render_photo
from carrousels_s01 import build


def dur(text, hook=False, cta=False):
    if hook:
        return 2.4
    n = len(text.replace("*", "").split())
    d = 0.9 + 0.17 * n
    return round(max(2.6 if cta else 2.2, min(2.8 if cta else 2.9, d)), 2)


def reel(photo, hook, *screens, cta):
    cards = [dict(text=hook, photo=photo, hook=True, dur=dur(hook, hook=True))]
    cards += [dict(text=s, dur=dur(s)) for s in screens]
    cards.append(dict(text=cta, cta=True, dur=dur(cta, cta=True)))
    return cards


# ================= CARROUSELS TRANSFORMÉS EN REELS =================

CONV = {
    "quaraouiyine": ("2026-10-19-quaraouiyine", reel(
        "fes.jpg",
        "À Fès, une école *ouverte depuis 11 siècles.*",
        "La Quaraouiyine. Selon la tradition, *une femme* l'a fondée : Fatima al-Fihri.",
        "Pour le Guinness, c'est le plus ancien établissement d'enseignement *encore en activité.*",
        "Sa date exacte reste *débattue par les historiens.*",
        cta="Envoie ça à quelqu'un *de Fès.*")),
    "sahara": ("2026-10-19-sahara-vert", reel(
        "sahara.jpg",
        "Le Sahara était vert. *Avec des hippopotames.*",
        "Il y a environ *10 000 ans* : pluies, lacs et savane.",
        "Girafes, éléphants, hippopotames : on les retrouve *peints sur les rochers.*",
        "Un lent changement de l'orbite terrestre *l'a peu à peu asséché.*",
        cta="Envoie ça à quelqu'un qui *rêve du désert.*")),
    "yamaguchi": ("2026-10-27-yamaguchi", reel(
        "hiroshima.jpg",
        "Hiroshima, puis Nagasaki. *Il a survécu aux deux.*",
        "6 août 1945 : Tsutomu Yamaguchi est à Hiroshima *pour son travail.*",
        "Blessé, il rentre *à Nagasaki.* Le 9 août, la deuxième bombe.",
        "En 2009, le Japon le reconnaît *survivant des deux.* Mort en 2010.",
        cta="Tu connaissais *son nom ?*")),
    "chefchaouen": ("2026-10-28-chefchaouen", reel(
        "chefchaouen.jpg",
        "Chefchaouen est bleue. *Personne ne sait vraiment pourquoi.*",
        "Version la plus répandue : des familles juives, *dans les années 1930.*",
        "D'autres parlent des moustiques ou de la fraîcheur. *Aucune preuve.*",
        "Ce qui est sûr : chaque printemps, les habitants *repeignent leurs murs.*",
        cta="Tu connais une autre explication ? *Dis-la en commentaire.*")),
    "onoda": ("2026-10-29-onoda", reel(
        "jungle.jpg",
        "Il s'est rendu *29 ans après la guerre.*",
        "Onoda, officier japonais aux Philippines. Ordre : *ne jamais se rendre.*",
        "En 1945, des tracts annoncent la paix. *Il croit à une ruse.*",
        "Part sombre : son groupe aurait *tué une trentaine de civils.*",
        "1974 : son ancien commandant vient lui ordonner *de cesser le combat.*",
        cta="Tu en avais déjà *entendu parler ?*")),
    "strasbourg": ("2026-10-30-strasbourg-1518", reel(
        "strasbourg.jpg",
        "En 1518, ils dansaient *sans pouvoir s'arrêter.*",
        "Juillet, Strasbourg : une femme se met à danser. *Pendant des jours.*",
        "En une semaine, *plus de trente personnes* l'ont rejointe.",
        "La ville paie des musiciens pour les guérir. *Ça ne marche pas.*",
        "Aujourd'hui, on pense à une *hystérie collective*, sur fond de famine.",
        cta="Tu aurais tenu *combien de temps ?*")),
}

# ================= LOT 5 =================

LOT5 = {
    "iphone": ("2026-10-31-iphone-curseur", reel(
        "iphone.jpg",
        "Ton clavier iPhone cache *un pavé tactile.*",
        "Garde le doigt appuyé sur *la barre d'espace.*",
        "Le clavier devient gris : glisse pour *déplacer le curseur.*",
        "Sur Android avec Gboard : *glisse sur la barre d'espace.*",
        cta="Envoie ça à quelqu'un qui *rate toujours ses corrections.*")),
    "miel": ("2026-10-31-miel", reel(
        "miel.jpg",
        "Du miel vieux de milliers d'années, *retrouvé intact.*",
        "Peu d'eau, très sucré et acide : *peu de microbes y survivent.*",
        "Les abeilles y ajoutent une enzyme qui produit un peu *d'eau oxygénée.*",
        "Garde-le bien fermé : *l'humidité* est son vrai ennemi.",
        cta="Cristallisé, il n'est pas périmé. Envoie ça à *qui le jette.*")),
    "winv": ("2026-11-01-windows-v", reel(
        "bureau.jpg",
        "Ton PC peut garder *tes 25 derniers copiés.*",
        "Sur Windows, appuie sur *Windows + V.*",
        "Active l'historique, puis retrouve tes *25 derniers copiés-collés.*",
        "*Épingle* tes favoris : ils restent même après un redémarrage.",
        cta="Envoie ça à ton collègue *qui copie-colle toute la journée.*")),
    "ryal": ("2026-11-01-ryal", reel(
        "souk.jpg",
        "Au Maroc, *1 dirham = 20 ryals.*",
        "Au souk, *100 ryals*, c'est 5 dirhams.",
        "L'ancien rial disparaît vers 1921. Le dirham actuel date de *1960.*",
        "Mais au souk, on compte encore *en ryals.*",
        cta="Envoie ça à quelqu'un qui *ne comprend rien aux prix du souk.*")),
    "fj": ("2026-11-02-touches-f-j", reel(
        "clavier.jpg",
        "Regarde les touches F et J. *Touche-les.*",
        "Elles ont une petite bosse. Ce n'est *pas un défaut.*",
        "Elles guident tes index *sans regarder le clavier.*",
        "Doigts posés dessus, les autres tombent *pile sur les bonnes touches.*",
        cta="Envoie ça à quelqu'un qui *tape avec deux doigts.*")),
    "maps": ("2026-11-02-maps-hors-connexion", reel(
        "route.jpg",
        "Sans réseau, *Google Maps peut encore te guider.*",
        "Avant de partir, télécharge la zone : *Cartes hors connexion.*",
        "Itinéraire en voiture *sans données mobiles.* Pas à pied ni en bus.",
        "Mets à jour tes cartes avant le départ, *elles expirent.*",
        cta="Envoie ça à quelqu'un qui *part en road trip.*")),
    "gmail": ("2026-11-03-gmail-annuler", reel(
        "gmail.jpg",
        "Mail parti trop vite ? *Rattrape-le.*",
        "Juste après l'envoi, Gmail affiche *Annuler* en bas de l'écran.",
        "Par défaut, le délai est *très court.*",
        "Sur ordinateur, dans les paramètres, passe à *30 secondes.*",
        cta="Envoie ça à ton collègue *qui répond trop vite.*")),
    "whatsapp": ("2026-11-03-whatsapp-modifier", reel(
        "whatsapp.jpg",
        "Ton message WhatsApp a une faute ? *Modifie-le.*",
        "Appui long sur le message, puis *Modifier* dans le menu.",
        "Tu as *15 minutes* après l'envoi.",
        "La mention *Modifié* s'affiche, mais pas l'ancienne version.",
        cta="Envoie ça au roi *des fautes de frappe.*")),
    "hublot": ("2026-11-04-hublot", reel(
        "hublot.jpg",
        "Ce trou dans le hublot *a un rôle.*",
        "Un hublot a *trois vitres.* Le trou est dans celle du milieu.",
        "Il équilibre la pression : la vitre extérieure *encaisse l'effort.*",
        "Et il évite *la buée* sur ta fenêtre.",
        cta="Envoie ça à quelqu'un qui *prend l'avion bientôt.*")),
    "urgences": ("2026-11-05-urgences-maroc", reel(
        "urgence.jpg",
        "Au Maroc, ces numéros peuvent *sauver une vie.*",
        "*15 ou 150* : protection civile, pompiers et ambulances.",
        "*19 ou 190* : police. *177* : gendarmerie, hors des villes.",
        "Note-les dans ton téléphone *avant d'en avoir besoin.*",
        cta="Envoie ça à *ta famille.*")),
}


def cta(text):
    return dict(body=text, footer="Suis *@peulesavent* pour la suite.")


RACCOURCIS = dict(slug="2026-11-04-raccourcis-windows", label="À enregistrer", slides=[
    dict(title="6 raccourcis Windows qui font *gagner du temps.*",
         body="Enregistre ce post, tu vas t'en resservir."),
    dict(big="Win + Maj + S", body="Capture d'une partie de l'écran. *Tu choisis la zone.*"),
    dict(big="Win + L", body="Verrouille ton PC en une seconde quand tu *quittes ton bureau.*"),
    dict(big="Win + D", body="Affiche le bureau. *Un second appui* remet tes fenêtres."),
    dict(big="Ctrl + Maj + T", body="Rouvre *le dernier onglet fermé*, dans Chrome et Edge."),
    dict(big="Alt + Tab", body="Passe d'une fenêtre à l'autre *sans toucher la souris.*"),
    dict(big="Win + E", body="Ouvre *l'explorateur de fichiers* directement."),
    cta("Envoie ça au collègue qui fait *tout à la souris.*"),
])

ALL = {**CONV, **LOT5}

if __name__ == "__main__":
    for k in sys.argv[1:]:
        if k == "raccourcis":
            build(RACCOURCIS)
        else:
            render_photo(*ALL[k])
