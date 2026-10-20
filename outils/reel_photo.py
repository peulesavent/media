"""Gabarit Reel photo (lot 5 et suivants).

Photo d'ambiance plein écran, assombrie à environ 55 %, zoom lent continu.
Texte centré, gros, blanc et ambre (*mot* = ambre), qui apparaît mot par mot.
Filigrane en bas, carte de fin "Suis @peulesavent" avec le p. et le son de marque.

Utilisation :
    from reel_photo import render_photo
    render_photo("2026-10-31-exemple", [
        dict(text="Accroche de *8 mots* au maximum.", photo="a.jpg", dur=2.6, hook=True),
        dict(text="Explication courte.", photo="b.jpg", dur=3.0),
        dict(text="Envoie ça à *ton frère.*", dur=2.6, cta=True),
    ])
Les photos sont cherchées dans posts/<slug>/src/ puis dans photos/.
"""
import math
import re
import os
import subprocess
from PIL import Image, ImageDraw, ImageFilter
from pls import font, mark, watermark, nbsp, tokens, FONT_BLACK, FONT_MED, BG, INK, ACCENT, REPO

W, H, FPS = 1080, 1920, 30
DARK = 0.60          # opacité du voile noir sur la photo
ZOOM = 0.10          # zoom total sur la durée d'une carte
WORD_STEP = 0.05    # décalage entre deux mots (s)
WORD_FADE = 0.12     # durée d'apparition d'un mot (s)
HOOK_STEP = 0.035    # l'accroche se lit dès la première image
OUTRO = 1.7
POP = 0.30
M = 84               # marge latérale


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


# ---------- photo ----------

def load_photo(path):
    im = Image.open(path).convert("RGB")
    # recadrage 9:16 centré, à 120 % pour garder de la marge au zoom
    tw, th = int(W * 1.2), int(H * 1.2)
    r = max(tw / im.width, th / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x0, y0 = (im.width - tw) // 2, (im.height - th) // 2
    im = im.crop((x0, y0, x0 + tw, y0 + th))
    # voile : noir à DARK plus un dégradé plus sombre au centre vertical pour le texte
    veil = Image.new("L", (tw, th))
    vd = ImageDraw.Draw(veil)
    for y in range(th):
        c = abs(y / th - 0.5) * 2          # 0 au centre, 1 aux bords
        a = DARK + 0.12 * (1 - c)          # 0.67 au centre, 0.55 aux bords
        vd.line((0, y, tw, y), fill=int(255 * a))
    black = Image.new("RGB", (tw, th), BG)
    return Image.composite(black, im, veil)


def photo_frame(src, k, drift=(0, 0)):
    """k de 0 à 1 : zoom lent de 1.0 à 1+ZOOM, léger glissement."""
    z = 1 + ZOOM * k
    sw, sh = W / z, H / z
    cx = src.width / 2 + drift[0] * k * 50
    cy = src.height / 2 + drift[1] * k * 50
    return src.resize((W, H), Image.BICUBIC, box=(cx - sw / 2, cy - sh / 2, cx + sw / 2, cy + sh / 2))


# ---------- texte mot par mot ----------

def layout(text, fnt, width, leading):
    """Mise en page centrée : liste de (mot, ambre, x, y) en coordonnées relatives."""
    d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    space = d.textlength(" ", font=fnt)
    lines, cur, curw = [], [], 0
    text = re.sub(r" ([?:!])", "\u00a0\\1", nbsp(text))
    text = re.sub(r"(\d) (\w)", "\\1\u00a0\\2", text)
    for para in text.split("\n"):
        for w, a, g in tokens(para):
            ww = d.textlength(w, font=fnt)
            if g and cur:
                cur.append((w, a, True, ww))
                curw += ww
                continue
            if cur and curw + space + ww > width:
                lines.append((cur, curw))
                cur, curw = [], 0
            curw += (space if cur else 0) + ww
            cur.append((w, a, False, ww))
        if cur:
            lines.append((cur, curw))
        cur, curw = [], 0
    lh = int(fnt.size * leading)
    out = []
    for i, (line, lw) in enumerate(lines):
        x = (W - lw) / 2
        first = True
        for w, a, g, ww in line:
            if not first and not g:
                x += space
            out.append((w, a, x, i * lh))
            x += ww
            first = False
    return out, len(lines) * lh


def text_sprites(text, hook=False, cta=False):
    size = 98 if hook else (80 if cta else 76)
    fnt = font(FONT_BLACK, size)
    words, th = layout(text, fnt, W - 2 * M, 1.14)
    while th > 900 and size > 58:
        size -= 4
        fnt = font(FONT_BLACK, size)
        words, th = layout(text, fnt, W - 2 * M, 1.14)
    y0 = (H - th) // 2 - (40 if cta else 70)
    sprites = []
    for w, a, x, y in words:
        d0 = ImageDraw.Draw(Image.new("RGB", (8, 8)))
        bb = d0.textbbox((0, 0), w, font=fnt)
        pad = 24
        im = Image.new("RGBA", (bb[2] + 2 * pad, bb[3] + 2 * pad), (0, 0, 0, 0))
        dd = ImageDraw.Draw(im)
        # ombre douce pour la lisibilité sur photo
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((pad, pad + 4), w, font=fnt, fill=(0, 0, 0, 170))
        sh = sh.filter(ImageFilter.GaussianBlur(9))
        im.alpha_composite(sh)
        dd.text((pad, pad), w, font=fnt, fill=(ACCENT if a else INK) + (255,))
        sprites.append((im, int(x) - pad, int(y0 + y) - pad))
    return sprites


def with_alpha(im, k):
    if k >= 0.999:
        return im
    out = im.copy()
    out.putalpha(im.getchannel("A").point(lambda v: int(v * k)))
    return out


# ---------- assemblage ----------

def find_photo(folder, name):
    for p in (f"{folder}/src/{name}", f"{REPO}/photos/{name}", name):
        if os.path.exists(p):
            return p
    raise FileNotFoundError(name)


def outro_frame(bg, t):
    img = bg.copy()
    d = ImageDraw.Draw(img)
    k = ease(t / 0.4)
    mark(d, W // 2, 760, 300, dot_scale=k)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    f = font(FONT_BLACK, 76)
    for i, txt in enumerate(((("Suis ", INK), ("@peulesavent", ACCENT)), (("pour la suite", INK),))):
        tw = sum(ld.textlength(s, font=f) for s, _ in txt)
        x = (W - tw) / 2
        for s, c in txt:
            ld.text((x, 1000 + i * 88), s, font=f, fill=c)
            x += ld.textlength(s, font=f)
    lay = with_alpha(lay, k)
    img.paste(lay, (0, int(30 * (1 - k))), lay)
    return img


def render_photo(slug, cards, outro=OUTRO):
    folder = f"{REPO}/posts/{slug}"
    os.makedirs(folder, exist_ok=True)
    photos, last = [], None
    for c in cards:
        if c.get("photo"):
            last = c["photo"]
        if last is None:
            raise ValueError("la première carte doit avoir une photo")
        photos.append(last)
    cache = {p: load_photo(find_photo(folder, p)) for p in set(photos)}
    drifts = [(1, 0), (0, -1), (-1, 0), (0, 1)]

    total = sum(c["dur"] for c in cards) + outro
    n = int(round(total * FPS))
    snd = ("aevalsrc='0.55*sin(2*PI*880*t)*exp(-16*t)+0.28*sin(2*PI*1320*t)*exp(-20*t)"
           "+0.18*sin(2*PI*440*t)*exp(-10*t)':s=48000:d=0.8")
    at = int((total - outro + POP) * 1000)
    ff = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-f", "lavfi", "-i", snd,
        "-filter_complex", f"[1:a]adelay={at}|{at},apad=whole_dur={total:.3f}[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "19",
        "-preset", "medium", "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "128k", "-ac", "2", "-t", f"{total:.3f}",
        f"{folder}/reel.mp4"], stdin=subprocess.PIPE)

    sprites = [text_sprites(c["text"], c.get("hook", False), c.get("cta", False)) for c in cards]
    # la photo zoome en continu tant qu'elle reste la même d'une carte à l'autre
    spans, start = {}, 0.0
    for i, c in enumerate(cards):
        p = photos[i]
        if i == 0 or photos[i - 1] != p:
            run_start = start
            j, run = i, 0.0
            while j < len(cards) and photos[j] == p:
                run += cards[j]["dur"]
                j += 1
            spans[i] = (run_start, run)
        else:
            spans[i] = spans[i - 1]
        start += c["dur"]

    cover, last_bg = None, None
    for f in range(n):
        t = f / FPS
        if t < total - outro:
            tl, i = t, 0
            while tl >= cards[i]["dur"]:
                tl -= cards[i]["dur"]
                i += 1
            c = cards[i]
            s0, run = spans[i]
            k = (t - s0) / run
            bg = photo_frame(cache[photos[i]], k, drifts[i % 4])
            # fondu de photo à photo
            if i > 0 and photos[i - 1] != photos[i] and tl < 0.25:
                ps0, prun = spans[i - 1]
                prev = photo_frame(cache[photos[i - 1]], min(1, (t - ps0) / prun), drifts[(i - 1) % 4])
                bg = Image.blend(prev, bg, ease(tl / 0.25))
            img = bg.convert("RGBA")
            step = HOOK_STEP if (c.get("hook") and i == 0) else WORD_STEP
            kout = 1 - ease((tl - (c["dur"] - 0.2)) / 0.2)
            for w, (sp, x, y) in enumerate(sprites[i]):
                if i == 0 and c.get("hook") and w == 0:
                    kw = 1.0
                else:
                    kw = ease((tl - w * step) / WORD_FADE) if not (i == 0 and c.get("hook")) else \
                        ease((tl - w * step + 0.08) / 0.10)
                kw = min(kw, kout)
                if kw <= 0:
                    continue
                img.alpha_composite(with_alpha(sp, kw), (x, y + int(18 * (1 - kw))))
            img = img.convert("RGB")
            watermark(img, 170, 60)
            last_bg = bg
        else:
            if last_bg is not None and not isinstance(last_bg, tuple):
                end_bg = Image.blend(last_bg, Image.new("RGB", (W, H), BG), 0.35)
                last_bg = (end_bg,)
            img = outro_frame(last_bg[0], t - (total - outro))
        if cover is None and t >= 0.6:
            cover = img
        ff.stdin.write(img.tobytes())
    ff.stdin.close()
    ff.wait()
    cover.save(f"{folder}/couverture.jpg", quality=92)
    print("ok", folder, f"{total:.1f}s")
    return folder
