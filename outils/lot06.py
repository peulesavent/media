"""Lot 6 : 7 Reels photo pour les créneaux libres du 22 au 30/10."""
import sys
from reel_photo import render_photo
from lot05 import reel

LOT6 = {
    "wifi": ("2026-10-22-partager-wifi", reel(
        "whatsapp.jpg",
        "Ton téléphone connaît *le mot de passe Wi-Fi.*",
        "Android : réglages Wi-Fi, ton réseau, puis *Partager* ou *Code QR.*",
        "Un *code QR* s'affiche. Ton ami le scanne et se connecte.",
        "Sur iPhone : Réglages, Wi-Fi, touche *(i)* puis Mot de passe.",
        cta="Envoie ça à celui qui *demande toujours le code Wi-Fi.*")),
    "pneu": ("2026-10-23-date-pneu", reel(
        "pneu.jpg",
        "Ton pneu affiche *sa date de fabrication.*",
        "Cherche sur le flanc le mot *DOT* et une suite de caractères.",
        "Les *4 derniers chiffres* : la semaine puis l'année.",
        "*2423*, c'est la 24e semaine de 2023.",
        cta="Envoie ça à quelqu'un qui *achète une voiture d'occasion.*")),
    "jean": ("2026-10-26-poche-jean", reel(
        "jean.jpg",
        "Cette mini-poche de ton jean *a une histoire.*",
        "Dès 1873, Levi's la prévoit pour *les montres à gousset.*",
        "Les montres ont quitté les poches. *La petite poche est restée.*",
        "Aujourd'hui, on y glisse souvent *des pièces ou des clés.*",
        cta="Envoie ça à quelqu'un qui *n'a jamais su à quoi elle servait.*")),
    "gestionnaire": ("2026-10-27-ctrl-maj-echap", reel(
        "pcwin.jpg",
        "Appli bloquée ? *Ce raccourci* te débloque.",
        "Appuie sur *Ctrl + Maj + Échap.*",
        "Le *Gestionnaire des tâches* s'ouvre directement, sans menu intermédiaire.",
        "Sélectionne l'appli bloquée, puis *Fin de tâche.*",
        cta="Envoie ça au collègue *qui redémarre tout à chaque bug.*")),
    "oeuf": ("2026-10-28-oeuf-eau", reel(
        "oeufs.jpg",
        "Un verre d'eau révèle *l'âge de ton œuf.*",
        "Il coule et reste à plat : *il est très frais.*",
        "Il se redresse ou flotte ? *Sa poche d'air a grandi.*",
        "Pas forcément avarié. *Casse-le à part.* Odeur bizarre ? *Jette-le.*",
        cta="Envoie ça à quelqu'un qui *cuisine tous les jours.*")),
    "banque": ("2026-10-29-code-banque", reel(
        "carte.jpg",
        "Ta banque ne te demandera *jamais ce code.*",
        "Le code SMS qui valide un paiement : *garde-le pour toi.*",
        "Un faux conseiller peut appeler avec *le numéro de ta banque* affiché.",
        "Raccroche, puis appelle toi-même *le numéro habituel de ta banque.*",
        cta="Envoie ça à *tes parents.*")),
    "noor": ("2026-10-30-noor-ouarzazate", reel(
        "miroirs.jpg",
        "Ces miroirs suivent le soleil *toute la journée.*",
        "À Ouarzazate, le complexe Noor en aligne *des centaines de milliers.*",
        "La chaleur stockée fait tourner les turbines *après le coucher du soleil.*",
        "C'est l'un des plus grands complexes *solaires à concentration* du monde.",
        cta="Envoie ça à quelqu'un qui *passe par Ouarzazate.*")),
}

if __name__ == "__main__":
    for k in sys.argv[1:]:
        render_photo(*LOT6[k])
