"""Gabarits graphiques Peu le savent : carrousels 4:5 et Reels 9:16."""
from PIL import Image, ImageDraw, ImageFont

FONT_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FONT_MED = "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf"

BG = (17, 17, 19)
INK = (245, 242, 235)
ACCENT = (242, 179, 61)
MUTED = (120, 118, 112)
LINE = (44, 44, 48)

REPO = "/home/claude/media"
WM = Image.open(f"{REPO}/brand/filigrane.png").convert("RGBA")


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------- texte riche : *mot* = ambre ----------

def tokens(text):
    """(mot, ambre, collé) : collé = pas d'espace avant (ponctuation après un *bloc*)."""
    out, amber, prev = [], False, " "
    for part in text.split("*"):
        words = part.split(" ")
        for i, w in enumerate(words):
            if w:
                glue = (i == 0 and bool(out) and not part.startswith(" ")
                        and not prev.endswith(" "))
                out.append((w, amber, glue))
        amber = not amber
        if part:
            prev = part
    return out


def wrap(draw, text, fnt, width):
    """Retourne une liste de lignes, chaque ligne = liste de (mot, ambre)."""
    lines, cur, space = [], [], draw.textlength(" ", font=fnt)
    curw = 0
    for para in text.split("\n"):
        for w, a, g in tokens(para):
            ww = draw.textlength(w, font=fnt)
            if g and cur:
                cur.append((w, a, True))
                curw += ww
                continue
            if cur and curw + space + ww > width:
                lines.append(cur)
                cur, curw = [], 0
            curw += (space if cur else 0) + ww
            cur.append((w, a, False))
        lines.append(cur)
        cur, curw = [], 0
    return lines


def nbsp(text):
    """Espaces insécables automatiques : milliers, av. J.-C., unités."""
    import re
    text = re.sub(r"(\d) (\d{3})", "\\1\u00a0\\2", text)
    text = re.sub(r"(\d) (\d{3})", "\\1\u00a0\\2", text)
    text = text.replace(" av. J.-C.", "\u00a0av.\u00a0J.-C.").replace("av. J.-C.", "av.\u00a0J.-C.")
    text = re.sub(r"(\d) (ans|km|m|jours|%)\b", "\\1\u00a0\\2", text)
    return text


def draw_rich(draw, xy, text, fnt, width, color=INK, accent=ACCENT, leading=1.28, align="left"):
    text = nbsp(text)
    x0, y = xy
    space = draw.textlength(" ", font=fnt)
    lh = int(fnt.size * leading)
    for line in wrap(draw, text, fnt, width):
        if not line:
            y += lh // 2
            continue
        lw = sum(draw.textlength(w, font=fnt) + (0 if g else space) for w, _, g in line) - space
        x = x0 + (width - lw) / 2 if align == "center" else x0
        first = True
        for w, a, g in line:
            if not first and not g:
                x += space
            draw.text((x, y), w, font=fnt, fill=accent if a else color)
            x += draw.textlength(w, font=fnt)
            first = False
        y += lh
    return y


def text_height(draw, text, fnt, width, leading=1.28):
    text = nbsp(text)
    lh = int(fnt.size * leading)
    return sum(lh if l else lh // 2 for l in wrap(draw, text, fnt, width))


# ---------- marque ----------

def mark(draw, cx, cy, size, ink=INK, accent=ACCENT, dot_scale=1.0):
    fnt = font(FONT_BLACK, size)
    bbox = draw.textbbox((0, 0), "p", font=fnt)
    w = bbox[2] - bbox[0]
    sb = draw.textbbox((0, 0), "s", font=fnt)
    xh = sb[3] - sb[1]
    dot_r = int(xh * 0.20)
    gap = int(xh * 0.10)
    total = w + gap + dot_r * 2
    x0 = cx - total // 2 - bbox[0]
    y0 = cy - (sb[1] + sb[3]) // 2
    draw.text((x0, y0), "p", font=fnt, fill=ink)
    base = y0 + sb[3]
    dx = x0 + bbox[0] + w + gap + dot_r
    r = dot_r * dot_scale
    cyd = base - dot_r
    if r > 0:
        draw.ellipse((dx - r, cyd - r, dx + r, cyd + r), fill=accent)


def watermark(img, width, margin):
    wm = WM.copy()
    wm = wm.resize((width, int(WM.height * width / WM.width)), Image.LANCZOS)
    img.paste(wm, (img.width - wm.width - margin, img.height - wm.height - margin), wm)


# ---------- carrousel ----------

CW, CH = 1080, 1350
SS = 2  # suréchantillonnage


def slide(n, total, label, body, big=None, illus=None, title=None, footer=None):
    """Une slide de carrousel. Tout est dessiné à x2 puis réduit."""
    W, H = CW * SS, CH * SS
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    m = 90 * SS
    tw = W - 2 * m

    # en-tête
    d.text((m, 78 * SS), label.upper(), font=font(FONT_MED, 26 * SS), fill=ACCENT)
    cnt = f"{n}/{total}"
    cf = font(FONT_MED, 26 * SS)
    d.text((W - m - d.textlength(cnt, font=cf), 78 * SS), cnt, font=cf, fill=MUTED)

    y = 190 * SS
    bottom = H - (330 if footer else 150) * SS
    bsize = 60
    while body and bsize > 44:
        bf_ = font(FONT_MED, bsize * SS)
        need = (200 * SS if big else 0) + text_height(d, body, bf_, tw, 1.32)
        if 190 * SS + need <= bottom:
            break
        bsize -= 2
    bf_ = font(FONT_MED, bsize * SS)
    if illus is None and not title:
        hgt = (200 * SS if big else 0) + (text_height(d, body, bf_, tw, 1.32) if body else 0)
        y = max(y, 190 * SS + (bottom - 190 * SS - hgt) // 2)
    if illus is not None:
        ill = illus(W, int(H * 0.42))
        img.paste(ill, (0, y - 40 * SS), ill)
        y += int(H * 0.42) - 10 * SS
    if title:
        ts = 86
        while ts > 60 and y + text_height(d, title, font(FONT_BLACK, ts * SS), tw, 1.1) > H - 140 * SS:
            ts -= 2
        tf = font(FONT_BLACK, ts * SS)
        y = draw_rich(d, (m, y), title, tf, tw, leading=1.1) + 30 * SS
    if big:
        bs = 190
        while bs > 90 and d.textlength(big, font=font(FONT_BLACK, bs * SS)) > tw:
            bs -= 6
        bf = font(FONT_BLACK, bs * SS)
        d.text((m - 8 * SS, y - 30 * SS), big, font=bf, fill=ACCENT)
        y += 200 * SS
    if body:
        y = draw_rich(d, (m, y), body, bf_, tw, leading=1.32)
    if footer:
        ff = font(FONT_BLACK, 40 * SS)
        fy = H - 250 * SS
        d.line((m, fy - 36 * SS, m + 80 * SS, fy - 36 * SS), fill=ACCENT, width=5 * SS)
        draw_rich(d, (m, fy), footer, ff, tw)

    # barre de progression
    seg, gap, by = 34 * SS, 10 * SS, H - 88 * SS
    for i in range(total):
        x = m + i * (seg + gap)
        d.rounded_rectangle((x, by, x + seg, by + 6 * SS), radius=3 * SS,
                            fill=ACCENT if i < n else LINE)

    img = img.resize((CW, CH), Image.LANCZOS)
    watermark(img, 190, 52)
    return img


# ---------- outils de dessin ----------

def layer(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)
