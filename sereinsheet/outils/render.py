import json, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

W, H = 1080, 1920
IVORY = (237, 233, 223)
GOLD = (201, 169, 106)
CHAR = (30, 30, 30)
SERIF = "fonts/package/files/cormorant-garamond-latin-600-normal.woff"
SANS = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
SANS_B = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
OUT = "out"

def cover(path):
    im = Image.open(path).convert("RGB")
    r = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - H) // 2
    im = im.crop((x, y, x + W, y + H))
    im = ImageEnhance.Brightness(im).enhance(0.55)
    ov = Image.new("RGB", (W, H), CHAR)
    im = Image.blend(im, ov, 0.35)
    from PIL import ImageStat
    m = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(m)
    lum = ImageStat.Stat(im.convert("L").crop((0, 450, W, 1300))).mean[0]
    peak = 150 if lum > 70 else 90
    for y in range(350, 1400):
        a = peak * (1 - abs(y - 875) / 525) ** 0.6
        md.line((0, y, W, y), fill=int(a))
    return Image.composite(Image.new("RGB", (W, H), (12, 12, 12)), im, m)

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines

def text_card(bg, text, hook=False, step=None):
    im = bg.copy()
    d = ImageDraw.Draw(im)
    maxw = 860
    if hook:
        size = 112
        while True:
            f = ImageFont.truetype(SERIF, size)
            lines = wrap(d, text, f, maxw)
            if len(lines) <= 4 or size < 70: break
            size -= 6
        lh = int(size * 1.08)
    else:
        size = 64
        f = ImageFont.truetype(SANS, size)
        lines = wrap(d, text, f, maxw)
        lh = int(size * 1.3)
    total = lh * len(lines)
    y = 860 - total // 2
    d.rectangle((110, y - 70, 190, y - 64), fill=GOLD)
    for ln in lines:
        d.text((110, y), ln, font=f, fill=IVORY)
        y += lh
    wm = ImageFont.truetype(SANS_B, 34)
    d.text((110, 1560), "SereinSheet", font=wm, fill=GOLD)
    return im

def end_card():
    im = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype(SERIF, 130)
    f2 = ImageFont.truetype(SANS, 46)
    f3 = ImageFont.truetype(SANS_B, 50)
    t = "SereinSheet"
    d.text(((W - d.textlength(t, font=f1)) / 2, 640), t, font=f1, fill=CHAR)
    d.rectangle((W/2 - 60, 820, W/2 + 60, 826), fill=GOLD)
    y = 880
    for ln in ["Budget, wedding and travel", "spreadsheets for Excel", "and Google Sheets"]:
        d.text(((W - d.textlength(ln, font=f2)) / 2, y), ln, font=f2, fill=(70, 70, 70)); y += 64
    t = "Link in bio"
    d.text(((W - d.textlength(t, font=f3)) / 2, 1130), t, font=f3, fill=GOLD)
    return im

def render(slug, photo, screens, blur=0):
    os.makedirs(f"{OUT}/{slug}", exist_ok=True)
    bg = cover(photo)
    if blur: bg = bg.filter(ImageFilter.GaussianBlur(blur))
    frames = []
    for i, s in enumerate(screens):
        p = f"{OUT}/{slug}/s{i}.png"
        text_card(bg, s, hook=(i == 0)).save(p); frames.append(p)
    p = f"{OUT}/{slug}/end.png"; end_card().save(p); frames.append(p)
    durs = [2.6] + [2.4] * (len(screens) - 1) + [2.2]
    durs[-2] = 2.2
    inputs, filt = [], []
    for i, (fr, du) in enumerate(zip(frames, durs)):
        inputs += ["-loop", "1", "-t", str(du + 0.3), "-i", fr]
        filt.append(f"[{i}:v]scale=1188:2112,zoompan=z='min(1+0.0009*on,1.1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps=30,format=yuv420p,setsar=1[v{i}]")
    cur, off = "v0", 0.0
    for i in range(1, len(frames)):
        off += durs[i - 1]
        filt.append(f"[{cur}][v{i}]xfade=transition=fade:duration=0.3:offset={off:.2f}[x{i}]")
        cur = f"x{i}"
    total = sum(durs) + 0.3
    n = len(frames)
    cmd = ["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-f", "lavfi", "-t", f"{total:.2f}", "-i", "anullsrc=r=44100:cl=stereo",
           "-filter_complex", ";".join(filt), "-map", f"[{cur}]", "-map", f"{n}:a", "-c:v", "libx264", "-preset", "veryfast",
           "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-shortest", "-movflags", "+faststart",
           f"{OUT}/{slug}.mp4"]
    subprocess.run(cmd, check=True)
    Image.open(frames[0]).save(f"{OUT}/{slug}-cover.jpg", quality=90)
    return total

if __name__ == "__main__":
    lot = json.load(open("lot.json"))
    only = sys.argv[1:]
    for r in lot:
        if only and r["slug"] not in only: continue
        for i, s in enumerate(r["screens"]):
            n = len(s.split()); lim = 8 if i == 0 else 12
            assert n <= lim, (r["slug"], i, n)
        t = render(r["slug"], f"photos/{r['photo']}.jpg", r["screens"], r.get("blur", 0))
        print(r["slug"], round(t, 1), "s")
