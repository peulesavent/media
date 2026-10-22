"""Lot 7 : 14 Reels d'essai (Trial Reels), 16h00, du 24/10 au 06/11."""
import sys
from reel_photo import render_photo
from lot05 import reel

LOT7 = {
    "capture": ("2026-10-24-capture-page", reel(
        "capture.jpg",
        "Ta capture d'écran peut faire *toute la page.*",
        "Sur Android : capture, puis *Capturer plus* ou l'icône défilante.",
        "Sur iPhone, dans Safari : touche la vignette, puis *Pleine page.*",
        "Sur iPhone, enregistre-la en *image ou en PDF.*",
        cta="Envoie ça à celui qui t'envoie *15 captures d'affilée.*")),
    "dentifrice": ("2026-10-25-carre-dentifrice", reel(
        "dentifrice.jpg",
        "Ce carré sur ton dentifrice *cache un mythe.*",
        "Une rumeur dit que sa couleur révèle *les ingrédients.*",
        "C'est un *repère pour les machines* qui coupent le tube.",
        "Les ingrédients sont écrits *sur l'emballage.*",
        cta="Envoie ça à celui qui *croit encore à la rumeur.*")),
    "excel": ("2026-10-26-excel-date", reel(
        "gmail.jpg",
        "Excel tape *la date du jour* pour toi.",
        "Sur PC, tape *Ctrl + ;* dans une cellule.",
        "La date d'aujourd'hui s'affiche, *sans rien taper.*",
        "Elle reste *figée* : elle ne changera pas demain.",
        cta="Envoie ça au collègue *qui tape la date à la main.*")),
    "dromadaire": ("2026-10-27-bosse-dromadaire", reel(
        "dromadaire.jpg",
        "La bosse du dromadaire *n'est pas remplie d'eau.*",
        "C'est surtout *de la graisse*, une réserve d'énergie.",
        "Elle peut stocker *jusqu'à environ 35 kilos* de graisse.",
        "Son vrai secret contre la soif : *il perd très peu d'eau.*",
        cta="Envoie ça à quelqu'un qui *part bientôt dans le désert.*")),
    "colis": ("2026-10-28-faux-sms-colis", reel(
        "colis.jpg",
        "Un SMS te parle *d'un colis bloqué ?*",
        "Il te demande de payer *une petite somme.*",
        "C'est une arnaque : le site vole *les infos de ta carte.*",
        "Ne clique pas. Vérifie *sur le site officiel* du transporteur.",
        cta="Envoie ça à *tes parents.*")),
    "oignon": ("2026-10-29-oignon-larmes", reel(
        "oignon.jpg",
        "Pourquoi l'oignon *te fait pleurer ?*",
        "En le coupant, tu libères un gaz qui *irrite tes yeux.*",
        "Un *couteau bien aiguisé* écrase moins de cellules.",
        "Coupe *lentement* : tu projettes moins de gouttelettes.",
        cta="Envoie ça à celui qui *coupe toujours les oignons.*")),
    "metre": ("2026-10-30-metre-ruban", reel(
        "metre.jpg",
        "Le crochet de ton mètre *bouge. C'est voulu.*",
        "Le crochet glisse de *son épaisseur exacte.*",
        "Tiré, il compte la mesure *depuis le bord.*",
        "Poussé contre un mur, *il compte aussi le crochet.*",
        cta="Envoie ça à celui qui croit *que son mètre est cassé.*")),
    "imei": ("2026-10-31-imei", reel(
        "imei.jpg",
        "Tape \\*#06# : ton téléphone affiche *son identifiant.*",
        "C'est l'*IMEI*, la carte d'identité de ton téléphone.",
        "Note-le *quelque part* en dehors du téléphone.",
        "En cas de vol, il sert à *identifier ton téléphone.*",
        cta="Envoie ça à quelqu'un qui *n'a jamais noté son IMEI.*")),
    "the": ("2026-11-01-the-de-haut", reel(
        "the.jpg",
        "Pourquoi verser le thé *de si haut ?*",
        "En tombant, il *s'aère* et fait de *la mousse.*",
        "Une *belle mousse*, c'est le signe d'un thé réussi.",
        "Le geste aide aussi à *refroidir un peu* le thé.",
        cta="Envoie ça à quelqu'un qui *verse le thé trop bas.*")),
    "recherche": ("2026-11-02-rechercher-page", reel(
        "recherche.jpg",
        "Ton téléphone a aussi *un Ctrl + F.*",
        "Dans Chrome : menu à trois points, puis *Rechercher sur la page.*",
        "Sur iPhone, dans Safari : Partager, puis *Rechercher sur la page.*",
        "Tape le mot : il est *surligné partout.*",
        cta="Envoie ça à quelqu'un qui *lit tout pour trouver une info.*")),
    "plastique": ("2026-11-03-triangle-plastique", reel(
        "plastique.jpg",
        "Ce chiffre dans le triangle *a un sens.*",
        "Il indique *le type de plastique* de l'emballage.",
        "Le *1*, c'est du PET, celui des bouteilles d'eau.",
        "Ce symbole ne garantit pas qu'il est *recyclable chez toi.*",
        cta="Envoie ça à quelqu'un qui *trie ses déchets.*")),
    "clim": ("2026-11-04-recyclage-air", reel(
        "clim.jpg",
        "Ce bouton avec *une flèche en boucle.*",
        "Il recycle l'air de l'habitacle *au lieu de prendre l'air extérieur.*",
        "Utile dans un tunnel ou derrière *un camion qui fume.*",
        "Mais si tu le laisses trop longtemps, *les vitres s'embuent.*",
        cta="Envoie ça à quelqu'un qui *roule toujours fenêtres fermées.*")),
    "nuage": ("2026-11-05-poids-nuage", reel(
        "nuage.jpg",
        "Un nuage pèse *des centaines de tonnes.*",
        "Un cumulus d'un kilomètre de côté : environ *500 tonnes d'eau.*",
        "Il flotte : son eau est en *gouttelettes minuscules.*",
        "L'air qui monte *les garde en suspension.*",
        cta="Envoie ça à quelqu'un qui *regarde toujours le ciel.*")),
    "moi": ("2026-11-06-whatsapp-toi-meme", reel(
        "notes.jpg",
        "WhatsApp a une discussion *avec toi-même.*",
        "Ouvre une nouvelle discussion, puis choisis *ton propre nom.*",
        "Notes, listes, photos, liens : *tout reste au même endroit.*",
        "Avec WhatsApp Web, *passe un fichier* du téléphone au PC.",
        cta="Envoie ça à celui qui *s'envoie tout par mail.*")),
}

if __name__ == "__main__":
    for k in sys.argv[1:]:
        render_photo(*LOT7[k])
