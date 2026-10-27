import json, os, subprocess, sys, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from kokoro_onnx import Kokoro

W, H, FPS = 1080, 1920, 30
IVORY = (237, 233, 223); CHAR = (24, 24, 27); GOLD = (201, 169, 106)
SERIF = "/home/claude/ss-reels/fonts/package/files/cormorant-garamond-latin-600-normal.woff"
SANS_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
SANS = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
SR = 24000
K = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
VOICE, SPEED, GAP = "af_heart", 1.08, 0.18

def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def caption_layer(text, hook):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    size = 66 if hook else 54
    f = ImageFont.truetype(SANS_B, size)
    lines = wrap(d, text, f, 900)
    lh = int(size * 1.25); hgt = lh * len(lines) + 56
    y0 = 300
    d.rounded_rectangle((60, y0, W - 60, y0 + hgt), 28, fill=CHAR + (235,))
    y = y0 + 28
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f)
        d.text(((W - tw) / 2, y), ln, font=f, fill=(255, 255, 255) if not hook else GOLD if False else (255, 255, 255))
        y += lh
    return im

def base_frame(img_path):
    bg = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(bg)
    f = ImageFont.truetype(SERIF, 54)
    t = "SereinSheet"; d.text(((W - d.textlength(t, font=f)) / 2, 150), t, font=f, fill=CHAR)
    d.rectangle((W / 2 - 40, 225, W / 2 + 40, 229), fill=GOLD)
    im = Image.open(img_path).convert("RGB")
    im.thumbnail((1000, 1080), Image.LANCZOS)
    sh = Image.new("RGBA", (im.width + 60, im.height + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((30, 40, im.width + 30, im.height + 40), 24, fill=(0, 0, 0, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    x = (W - im.width) // 2; y = 640 + (1080 - im.height) // 2
    bg.paste(sh, (x - 30, y - 30), sh)
    mask = Image.new("L", im.size, 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.width, im.height), 22, fill=255)
    bg.paste(im, (x, y), mask)
    return bg

def end_frame():
    bg = Image.new("RGB", (W, H), CHAR); d = ImageDraw.Draw(bg)
    f1 = ImageFont.truetype(SERIF, 120); f2 = ImageFont.truetype(SANS, 46); f3 = ImageFont.truetype(SANS_B, 60)
    t = "SereinSheet"; d.text(((W - d.textlength(t, font=f1)) / 2, 700), t, font=f1, fill=IVORY)
    d.rectangle((W / 2 - 60, 870, W / 2 + 60, 875), fill=GOLD)
    y = 930
    for ln in ["Excel and Google Sheets", "Instant download"]:
        d.text(((W - d.textlength(ln, font=f2)) / 2, y), ln, font=f2, fill=(200, 196, 188)); y += 66
    t = "Link in bio"
    bw = d.textlength(t, font=f3) + 120
    d.rounded_rectangle(((W - bw) / 2, 1130, (W + bw) / 2, 1250), 60, fill=GOLD)
    d.text(((W - d.textlength(t, font=f3)) / 2, 1155), t, font=f3, fill=CHAR)
    return bg

def music(dur):
    t = np.arange(int(dur * SR)) / SR
    chords = [[220.0, 277.18, 329.63], [196.0, 246.94, 293.66], [174.61, 220.0, 261.63], [196.0, 246.94, 329.63]]
    out = np.zeros_like(t); seg = 3.2
    for i in range(int(dur / seg) + 1):
        a, b = int(i * seg * SR), int(min((i + 1) * seg, dur) * SR)
        if a >= len(t): break
        tt = t[a:b] - i * seg
        env = np.minimum(1, tt / 0.6) * np.minimum(1, (seg - tt) / 0.6)
        for fr in chords[i % 4]:
            out[a:b] += env * (np.sin(2 * np.pi * fr * tt) + 0.3 * np.sin(2 * np.pi * fr * 2 * tt)) / 3
        out[a:b] += env * 0.5 * np.sin(2 * np.pi * chords[i % 4][0] / 2 * tt)
    beat = (np.sin(2 * np.pi * t / 0.5) > 0.995).astype(float)
    out += np.convolve(beat, np.exp(-np.arange(int(0.05 * SR)) / 300) * np.sin(2 * np.pi * 60 * np.arange(int(0.05 * SR)) / SR), "same") * 0.6
    out /= np.max(np.abs(out)) + 1e-9
    fade = np.minimum(1, np.minimum(t / 1.0, (dur - t) / 1.0))
    return out * fade * 0.10

def build(lid, spec, outdir):
    work = f"work/{spec['slug']}"; os.makedirs(work, exist_ok=True)
    voice, segs, t = [], [], 0.3
    voice.append(np.zeros(int(0.3 * SR)))
    for i, (sub, say) in enumerate(spec["lines"]):
        a, sr = K.create(say or sub, voice=VOICE, speed=SPEED, lang="en-us")
        d = len(a) / sr + GAP
        voice += [a, np.zeros(int(GAP * SR))]
        segs.append((sub, t, d)); t += d
    voice.append(np.zeros(int(0.8 * SR)))
    v = np.concatenate(voice); total = len(v) / SR
    m = music(total)[:len(v)]; v = v[:len(m)]
    mix = v * 0.95 + m
    sf.write(f"{work}/audio.wav", np.clip(mix, -1, 1), SR)
    clips = []
    n = len(segs)
    for i, (sub, st, d) in enumerate(segs):
        last = i == n - 1
        if last:
            fr = end_frame(); d = d + 0.8 + (0.3 if i == 0 else 0)
        else:
            fr = base_frame(f"src/{lid}/{spec['imgs'][i % len(spec['imgs'])]:02d}.jpg")
            if i == 0: d += 0.3
        cap = caption_layer(sub, i == 0)
        fr = fr.convert("RGBA"); fr.alpha_composite(cap)
        p = f"{work}/f{i}.png"; fr.convert("RGB").save(p)
        clips.append((p, d))
    inp, flt = [], []
    for i, (p, d) in enumerate(clips):
        inp += ["-framerate", str(FPS), "-loop", "1", "-t", f"{d + 0.25:.3f}", "-i", p]
        flt.append(f"[{i}:v]scale=1134:2016,zoompan=z='min(1+0.0006*on,1.05)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},format=yuv420p,setsar=1[v{i}]")
    cur, off = "v0", 0.0
    for i in range(1, len(clips)):
        off += clips[i - 1][1]
        flt.append(f"[{cur}][v{i}]xfade=transition=fade:duration=0.25:offset={off:.3f}[x{i}]"); cur = f"x{i}"
    out = f"{outdir}/{spec['slug']}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + inp + ["-i", f"{work}/audio.wav", "-filter_complex", ";".join(flt),
                    "-map", f"[{cur}]", "-map", f"{len(clips)}:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", out], check=True)
    Image.open(clips[0][0]).save(f"{outdir}/{spec['slug']}-cover.jpg", quality=90)
    return out, round(total, 1)

if __name__ == "__main__":
    S = json.load(open("scripts.json")); os.makedirs("out", exist_ok=True)
    for lid in (sys.argv[1:] or list(S)):
        print(lid, build(lid, S[lid], "out"))
