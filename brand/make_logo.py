"""Identité visuelle Peu le savent : photo de profil, filigrane, aperçus."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FONT_MED = "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf"

BG = (17, 17, 19)          # quasi noir
INK = (245, 242, 235)      # blanc cassé
ACCENT = (242, 179, 61)    # ambre, le "point de savoir"

S = 2160  # rendu x2 puis réduction, pour des bords nets
OUT = 1080


def mark(draw, cx, cy, size, ink, accent):
    """Monogramme 'pls' + point ambre, centré sur (cx, cy)."""
    font = ImageFont.truetype(FONT_BLACK, size)
    text = "p"
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    # hauteur de x approximée par le 's'
    sb = draw.textbbox((0, 0), "s", font=font)
    xh = sb[3] - sb[1]
    dot_r = int(xh * 0.20)
    gap = int(xh * 0.10)
    total = w + gap + dot_r * 2
    x0 = cx - total // 2 - bbox[0]
    # centre visuel sur la hauteur de x, pas sur les jambages
    y0 = cy - (sb[1] + sb[3]) // 2
    draw.text((x0, y0), text, font=font, fill=ink)
    # point posé sur la ligne de base
    base = y0 + sb[3]
    dx = x0 + bbox[0] + w + gap + dot_r
    draw.ellipse((dx - dot_r, base - 2 * dot_r, dx + dot_r, base), fill=accent)


def profile():
    img = Image.new("RGB", (S, S), BG)
    d = ImageDraw.Draw(img)
    mark(d, S // 2, S // 2 - int(S*0.065), int(S * 0.62), INK, ACCENT)
    return img.resize((OUT, OUT), Image.LANCZOS)


def watermark():
    """Filigrane transparent pour les coins des publications."""
    W, H = 1600, 360
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_BLACK, 200)
    text = "peulesavent"
    bb = d.textbbox((0, 0), text, font=font)
    sb = d.textbbox((0, 0), "s", font=font)
    xh = sb[3] - sb[1]
    dot_r = int(xh * 0.20)
    gap = int(xh * 0.10)
    tw = bb[2] - bb[0] + gap + 2 * dot_r
    x0 = (W - tw) // 2 - bb[0]
    y0 = H // 2 - (sb[1] + sb[3]) // 2
    # ombre douce pour rester lisible sur fond clair
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    ds.text((x0, y0 + 4), text, font=font, fill=(0, 0, 0, 140))
    sh = sh.filter(ImageFilter.GaussianBlur(10))
    img = Image.alpha_composite(img, sh)
    d = ImageDraw.Draw(img)
    d.text((x0, y0), text, font=font, fill=INK + (235,))
    base = y0 + sb[3]
    dx = x0 + bb[0] + (bb[2] - bb[0]) + gap + dot_r
    d.ellipse((dx - dot_r, base - 2 * dot_r, dx + dot_r, base), fill=ACCENT + (255,))
    cropped = img.crop(img.getbbox())
    return cropped.resize((cropped.width // 2, cropped.height // 2), Image.LANCZOS)


def circle(img, size):
    im = img.resize((size, size), Image.LANCZOS)
    m = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(m).ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255)
    m = m.resize((size, size), Image.LANCZOS)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(im, (0, 0), m)
    return out


def preview(pfp, wm):
    """Planche : tailles réelles d'affichage, fond clair et sombre, filigrane."""
    W, H = 1400, 1180
    sheet = Image.new("RGB", (W, H), (250, 250, 248))
    d = ImageDraw.Draw(sheet)
    d.rectangle((0, H // 2 - 60, W, H), fill=(12, 12, 14))
    lab = ImageFont.truetype(FONT_MED, 26)
    name = ImageFont.truetype(FONT_BLACK, 34)

    sizes = [320, 150, 77, 44, 32]
    for row, (y, fg, tag) in enumerate([(60, (30, 30, 30), "Mode clair"),
                                         (H // 2 - 20, (230, 230, 230), "Mode sombre")]):
        d.text((60, y), tag, font=lab, fill=fg)
        x = 60
        for s in sizes:
            c = circle(pfp, s)
            sheet.paste(c, (x, y + 50 + (320 - s) // 2), c)
            d.text((x, y + 390), f"{s}px", font=lab, fill=(140, 140, 140))
            x += s + 70
        # ligne de commentaire simulée
        cy = y + 60
        c = circle(pfp, 44)
        sheet.paste(c, (x + 10, cy), c)
        d.text((x + 70, cy - 2), "peulesavent", font=ImageFont.truetype(FONT_BLACK, 24), fill=fg)
        d.text((x + 70, cy + 26), "Source en commentaire", font=lab, fill=(150, 150, 150))

    # filigrane sur une vignette de publication factice
    post = Image.new("RGB", (300, 300), (88, 104, 120))
    pd_ = ImageDraw.Draw(post)
    for i in range(0, 300, 6):
        pd_.line((0, i, 300, i), fill=(80 + i // 10, 96 + i // 12, 112 + i // 15))
    w = wm.copy()
    w.thumbnail((130, 60), Image.LANCZOS)
    post.paste(w, (300 - w.width - 14, 300 - w.height - 14), w)
    sheet.paste(post, (W - 360, H - 360))
    d.text((W - 360, H - 400), "Filigrane", font=lab, fill=(200, 200, 200))
    return sheet


if __name__ == "__main__":
    import os
    out = "/home/claude/logo"
    p = profile()
    p.save(f"{out}/peulesavent_profil.png")
    wm = watermark()
    wm.save(f"{out}/peulesavent_filigrane.png")
    preview(p, wm).save(f"{out}/peulesavent_apercu.png")
    print("ok", wm.size)
