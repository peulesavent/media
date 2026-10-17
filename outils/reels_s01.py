"""Semaine 1 : les deux Reels (1080x1920, 30 i/s)."""
import math
import os
import subprocess
from PIL import Image, ImageDraw
from pls import (font, draw_rich, text_height, mark, watermark, layer,
                 FONT_BLACK, FONT_MED, BG, INK, ACCENT, LINE, MUTED, REPO)

W, H, FPS = 1080, 1920, 30
IW, IH = 1080, 760          # zone d'illustration
ILL_Y = 330
INTRO, OUTRO = 1.0, 2.6
POP = 0.35                  # instant où le point apparaît (et où sonne la signature)


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def with_alpha(im, k):
    if k >= 1:
        return im
    a = im.getchannel("A").point(lambda v: int(v * k))
    out = im.copy()
    out.putalpha(a)
    return out


def text_layer(text, hook=False, has_illus=True):
    im, d = layer(W, H)
    m = 90
    fnt = font(FONT_BLACK, 84) if hook else font(FONT_MED, 66)
    lead = 1.12 if hook else 1.3
    th = text_height(d, text, fnt, W - 2 * m, lead)
    y = ILL_Y + IH + 60 if has_illus else (H - th) // 2 - 80
    draw_rich(d, (m, y), text, fnt, W - 2 * m, leading=lead)
    return im


# ---------- illustrations animées (t de 0 à 1 sur la durée de la carte) ----------

def _canvas():
    im, d = layer(IW * 2, IH * 2)
    return im, d, IW, IH  # coordonnées x2 = IW, IH valent la moitié


def _done(im):
    return im.resize((IW, IH), Image.LANCZOS)


def planet(d, cx, cy, r, phase=0.0):
    # disque uni et voilé : dégradé concentrique du bord vers le centre
    steps = 24
    for k in range(steps):
        f = k / (steps - 1)
        rr = r * (1 - 0.55 * f)
        col = (int(200 + 40 * f), int(160 + 52 * f), int(92 + 60 * f))
        ox = -0.18 * r * f
        d.ellipse((cx + ox - rr, cy + ox - rr, cx + ox + rr, cy + ox + rr), fill=col)
    # repère qui tourne : un point qui glisse sur l'équateur
    x = cx + math.cos(math.pi * (1 - phase)) * r * 0.85
    d.ellipse((x - 22, cy - 22, x + 22, cy + 22), fill=INK)


def ill_venus_hook(t):
    im, d, w, h = _canvas()
    planet(d, w, h, 520, phase=t * 0.25)
    return _done(im)


def ill_venus_rotation(t):
    im, d, w, h = _canvas()
    planet(d, w, h, 420, phase=ease(t))
    r = 560
    end = -90 + 360 * ease(t * 1.15)
    d.arc((w - r, h - r, w + r, h + r), -90, end, fill=ACCENT, width=26)
    a = math.radians(end)
    x, y = w + r * math.cos(a), h + r * math.sin(a)
    d.ellipse((x - 30, y - 30, x + 30, y + 30), fill=ACCENT)
    return _done(im)


def ill_venus_orbit(t):
    im, d, w, h = _canvas()
    rx, ry = 820, 520
    d.ellipse((w - rx, h - ry, w + rx, h + ry), outline=LINE, width=10)
    d.ellipse((w - 130, h - 130, w + 130, h + 130), fill=ACCENT)
    a = math.radians(180 + 360 * ease(t * 1.1))
    end = math.degrees(a)
    d.arc((w - rx, h - ry, w + rx, h + ry), 180, end, fill=ACCENT, width=10)
    x, y = w + rx * math.cos(a), h + ry * math.sin(a)
    planet(d, x, y, 90, phase=0)
    return _done(im)


def ill_venus_west(t):
    im, d, w, h = _canvas()
    ground = int(h * 1.45)
    sx = w * 0.45
    sy = ground + 140 - 520 * ease(t * 1.3)
    d.ellipse((sx - 140, sy - 140, sx + 140, sy + 140), fill=ACCENT)
    d.rectangle((0, ground, 2 * w, 2 * h), fill=BG)
    d.line((60, ground, 2 * w - 60, ground), fill=MUTED, width=8)
    f = font(FONT_BLACK, 64)
    d.text((80, ground + 40), "OUEST", font=f, fill=INK)
    tw = d.textlength("EST", font=f)
    d.text((2 * w - 80 - tw, ground + 40), "EST", font=f, fill=MUTED)
    return _done(im)


def gauge(d, w, h, arrow="left", glow=1.0, needle=0.18):
    cx, cy, r = w, int(h * 1.25), 620
    d.arc((cx - r, cy - r, cx + r, cy + r), 200, 340, fill=INK, width=22)
    for k in range(5):
        a = math.radians(200 + k * 35)
        x1, y1 = cx + (r - 20) * math.cos(a), cy + (r - 20) * math.sin(a)
        x2, y2 = cx + (r - 90) * math.cos(a), cy + (r - 90) * math.sin(a)
        d.line((x1, y1, x2, y2), fill=INK, width=14)
    f = font(FONT_BLACK, 80)
    for lab, a in (("E", 200), ("F", 340)):
        ra = math.radians(a)
        x, y = cx + (r - 170) * math.cos(ra), cy + (r - 170) * math.sin(ra)
        tw = d.textlength(lab, font=f)
        d.text((x - tw / 2, y - 50), lab, font=f, fill=INK)
    a = math.radians(200 + 140 * needle)
    d.line((cx, cy, cx + (r - 60) * math.cos(a), cy + (r - 60) * math.sin(a)), fill=ACCENT, width=20)
    d.ellipse((cx - 44, cy - 44, cx + 44, cy + 44), fill=INK)
    # icône pompe
    px, py = cx - 110, cy - 330
    d.rounded_rectangle((px, py, px + 150, py + 210), radius=18, outline=INK, width=16)
    d.rectangle((px + 32, py + 34, px + 118, py + 90), fill=INK)
    d.line((px + 150, py + 70, px + 200, py + 110, px + 200, py + 190), fill=INK, width=14)
    # la petite flèche
    col = tuple(int(MUTED[i] + (ACCENT[i] - MUTED[i]) * glow) for i in range(3))
    ty = py + 105
    if arrow == "left":
        tx = px - 70
        d.polygon([(tx, ty), (tx + 60, ty - 42), (tx + 60, ty + 42)], fill=col)
    else:
        tx = px + 270
        d.polygon([(tx + 60, ty), (tx, ty - 42), (tx, ty + 42)], fill=col)


def ill_pump(t):
    im, d, w, h = _canvas()
    gauge(d, w, h, glow=0.0, needle=0.12 - 0.06 * ease(t))
    return _done(im)


def ill_arrow_pulse(t):
    im, d, w, h = _canvas()
    g = 0.5 + 0.5 * math.sin(t * 2 * math.pi * 2.2)
    gauge(d, w, h, glow=g, needle=0.06)
    return _done(im)


def ill_arrow_flip(t):
    im, d, w, h = _canvas()
    gauge(d, w, h, arrow="left" if t < 0.5 else "right", glow=1.0, needle=0.06)
    return _done(im)


# ---------- assemblage ----------

def intro_frame(t):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    k = ease(t / 0.3)
    size = int(520 * (0.86 + 0.14 * k))
    x = (t - POP) / 0.22
    dot = 0 if x <= 0 else (1 + 0.35 * math.sin(math.pi * min(x, 1))) if x < 1 else 1
    col = tuple(int(BG[i] + (INK[i] - BG[i]) * k) for i in range(3))
    mark(d, W // 2, H // 2 - 60, size, ink=col, dot_scale=dot)
    if t > INTRO - 0.12:
        img = Image.blend(img, Image.new("RGB", (W, H), BG), (t - (INTRO - 0.12)) / 0.12)
    return img


def outro_frame(t):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    k = ease(t / 0.4)
    mark(d, W // 2, 760, 300, dot_scale=k)
    lay, ld = layer(W, H)
    draw_rich(ld, (90, 1000), "Suis *@peulesavent*\npour la suite", font(FONT_BLACK, 76),
              W - 180, leading=1.15, align="center")
    lay = with_alpha(lay, k)
    img.paste(lay, (0, int(30 * (1 - k))), lay)
    return img


def card_frame(card, tl, txt):
    img = Image.new("RGB", (W, H), BG)
    dur = card["dur"]
    kin = ease(tl / 0.35)
    kout = 1 - ease((tl - (dur - 0.25)) / 0.25)
    k = min(kin, kout)
    if card.get("illus"):
        ill = with_alpha(card["illus"](tl / dur).convert("RGBA"), k)
        img.paste(ill, (0, ILL_Y), ill)
    t2 = with_alpha(txt, k)
    img.paste(t2, (0, int(50 * (1 - kin))), t2)
    watermark(img, 170, 60)
    return img


def render(slug, cards):
    folder = f"{REPO}/posts/{slug}"
    os.makedirs(folder, exist_ok=True)
    total = INTRO + sum(c["dur"] for c in cards) + OUTRO
    n = int(round(total * FPS))
    silent = f"{folder}/_video.mp4"
    snd = (f"aevalsrc='0.55*sin(2*PI*880*t)*exp(-16*t)+0.28*sin(2*PI*1320*t)*exp(-20*t)"
           f"+0.18*sin(2*PI*440*t)*exp(-10*t)':s=48000:d=0.8")
    ff = subprocess.Popen([
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-f", "lavfi", "-i", snd,
        "-filter_complex", f"[1:a]adelay={int(POP*1000)}|{int(POP*1000)},apad=whole_dur={total:.3f}[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "18",
        "-preset", "medium", "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "128k", "-ac", "2", "-t", f"{total:.3f}",
        f"{folder}/reel.mp4"], stdin=subprocess.PIPE)
    txts = [text_layer(c["text"], hook=c.get("hook", False), has_illus=bool(c.get("illus")))
            for c in cards]
    cover = None
    for i in range(n):
        t = i / FPS
        if t < INTRO:
            img = intro_frame(t)
        elif t < total - OUTRO:
            tl = t - INTRO
            for c, txt in zip(cards, txts):
                if tl < c["dur"]:
                    img = card_frame(c, tl, txt)
                    break
                tl -= c["dur"]
        else:
            img = outro_frame(t - (total - OUTRO))
        if cover is None and t >= INTRO + 1.2:
            cover = img
        ff.stdin.write(img.tobytes())
    ff.stdin.close()
    ff.wait()
    cover.save(f"{folder}/couverture.jpg", quality=92)
    print("ok", folder, f"{total:.1f}s")


VENUS = [
    dict(text="Sur Vénus, une journée dure *plus longtemps qu'une année.*", hook=True,
         illus=ill_venus_hook, dur=3.4),
    dict(text="Pour faire un tour complet sur elle-même, il lui faut *243 jours* terrestres.",
         illus=ill_venus_rotation, dur=3.4),
    dict(text="Pour faire le tour du Soleil, seulement *225 jours.*",
         illus=ill_venus_orbit, dur=3.0),
    dict(text="Et comme elle tourne à l'envers, là-bas le Soleil *se lève à l'ouest.*",
         illus=ill_venus_west, dur=3.6),
]

JAUGE = [
    dict(text="De quel côté est le réservoir ? *Ton tableau de bord le sait déjà.*", hook=True,
         illus=ill_pump, dur=3.4),
    dict(text="Regarde la petite flèche juste à côté de l'icône de la pompe.",
         illus=ill_arrow_pulse, dur=3.2),
    dict(text="Elle indique *le côté de la trappe à carburant.*",
         illus=ill_arrow_pulse, dur=2.8),
    dict(text="Flèche à gauche, trappe à gauche. *Flèche à droite, trappe à droite.*",
         illus=ill_arrow_flip, dur=3.6),
    dict(text="Inventée chez Ford à la fin des années 80, elle est aujourd'hui sur la plupart des voitures. "
              "Fini les demi-tours à la station.", dur=3.6),
]

if __name__ == "__main__":
    render("2026-10-20-venus", VENUS)
    render("2026-10-22-fleche-jauge", JAUGE)
