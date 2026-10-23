"""Moteur de dessin des icônes du mod (phase 8), style « C3 · Plan acier » choisi par Florian le 23/10.

Un sujet est dessiné une fois en formes et en lumière (niveaux de gris), suréchantillonné ×K, puis peint :
plan bleu assombri à la teinte de l'acier du jeu, aplat ombré, traits fins, grain, ombre portée. Les slots
vides sont peints en vert pâle en relief, comme ceux du vanilla. Le palier se marque comme dans le jeu :
chiffre romain orangé en bas à droite.

Export : .dds 32 bits A8R8G8B8 non compressé, sans mipmaps (format des images du designer vanilla,
skills/hoi4-interface/references/images-dds.md).
"""
import math
import struct
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

K = 8                                   # suréchantillonnage
FONTS = Path("C:/Windows/Fonts")
RNG = np.random.default_rng(7)
LIGHT = np.array([-0.55, -0.85]) / np.linalg.norm([-0.55, -0.85])


# ---------------------------------------------------------------- toile
class Canvas:
    def __init__(self, w=56, h=42):
        self.w, self.h = w, h
        self.lum = np.zeros((h * K, w * K), np.float32)
        self.alpha = np.zeros((h * K, w * K), np.float32)
        self.lines = np.zeros((h * K, w * K), np.float32)
        self.accent = np.zeros((h * K, w * K), np.float32)
        ys, xs = np.mgrid[0:h * K, 0:w * K]
        self.X = (xs + 0.5) / K
        self.Y = (ys + 0.5) / K
        self.badge = None                # (texte, sorte) : « II », « B », « S »…
        self.slot = False

    def _mask(self, fn):
        m = Image.new("L", (self.w * K, self.h * K), 0)
        fn(ImageDraw.Draw(m))
        return np.asarray(m, np.float32) / 255

    def fill(self, mask, shade, a=1.0, accent=0.0, outline=True):
        lum = shade(self.X, self.Y) if callable(shade) else np.full_like(self.lum, shade)
        self.lum = self.lum * (1 - mask) + lum * mask
        self.alpha = np.maximum(self.alpha, mask * a)
        self.accent = np.maximum(self.accent * (1 - mask), mask * accent)
        if outline:
            m = Image.fromarray((mask * 255).astype(np.uint8))
            inner = np.asarray(m.filter(ImageFilter.MinFilter(int(K * 0.9) | 1)), np.float32) / 255
            self.lines = self.lines * (1 - inner) + (mask - inner).clip(0, 1)

    def poly(self, pts, shade, **kw):
        p = [(x * K, y * K) for x, y in pts]
        self.fill(self._mask(lambda d: d.polygon(p, fill=255)), shade, **kw)

    def ellipse(self, box, shade, **kw):
        x0, y0, x1, y1 = (v * K for v in box)
        self.fill(self._mask(lambda d: d.ellipse((x0, y0, x1, y1), fill=255)), shade, **kw)

    def circle(self, cx, cy, r, shade, **kw):
        self.ellipse((cx - r, cy - r, cx + r, cy + r), shade, **kw)

    def rrect(self, box, r, shade, **kw):
        x0, y0, x1, y1 = (v * K for v in box)
        self.fill(self._mask(lambda d: d.rounded_rectangle((x0, y0, x1, y1), max(0, r * K), fill=255)), shade, **kw)

    def bar(self, p0, p1, r, shade=None, **kw):
        """Cylindre (tube, canon, fût) de p0 à p1, de rayon r."""
        (x0, y0), (x1, y1) = p0, p1
        L = math.hypot(x1 - x0, y1 - y0) or 1
        nx, ny = -(y1 - y0) / L * r, (x1 - x0) / L * r
        self.poly([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)],
                  shade or cyl(p0, p1, r), **kw)

    def line(self, pts, width=0.6, dark=0.55):
        p = [(x * K, y * K) for x, y in pts]
        m = self._mask(lambda d: d.line(p, fill=255, width=max(1, int(width * K)), joint="curve"))
        if dark == 0:                     # trait visible pour lui-même (réticule, ondes, jet) : il remplit l'image
            self.fill(m, 0.8, outline=False)
            self.lines = np.maximum(self.lines, m)
            return
        m = m * (self.alpha > 0.05)
        self.lum = self.lum * (1 - m * dark)
        self.lines = np.maximum(self.lines, m)

    def arc(self, box, start, end, width=0.6, dark=0.4):
        x0, y0, x1, y1 = (v * K for v in box)
        m = self._mask(lambda d: d.arc((x0, y0, x1, y1), start, end, fill=255, width=max(1, int(width * K))))
        self.lum = self.lum * (1 - m * dark * (self.alpha > 0.05))
        self.lines = np.maximum(self.lines, m)
        self.alpha = np.maximum(self.alpha, m * 0.9)


# ---------------------------------------------------------------- lumière
def cyl(p0, p1, r, base=0.42, amp=0.48):
    """Ombrage d'un cylindre d'axe p0→p1 et de rayon r, éclairé d'en haut à gauche."""
    (x0, y0), (x1, y1) = p0, p1
    ax = np.array([x1 - x0, y1 - y0], float)
    n = np.linalg.norm(ax)
    ax = ax / n if n else np.array([1.0, 0.0])
    nrm = np.array([-ax[1], ax[0]])
    if nrm @ LIGHT < 0:
        nrm = -nrm

    def f(X, Y):
        t = (((X - x0) * nrm[0] + (Y - y0) * nrm[1]) / max(r, 0.1)).clip(-1, 1)
        body = np.sqrt(np.clip(1 - t ** 2, 0, 1))
        spec = np.exp(-((t - 0.45) / 0.2) ** 2)
        return (base + amp * (0.55 * body + 0.45 * (t + 1) / 2) + 0.35 * spec).clip(0, 1)
    return f


def sphere(cx, cy, r, base=0.35, amp=0.6):
    def f(X, Y):
        dx, dy = (X - cx) / r, (Y - cy) / r
        z = np.sqrt(np.clip(1 - dx ** 2 - dy ** 2, 0, 1))
        lam = (z * 0.7 + (-(dx * LIGHT[0] + dy * LIGHT[1])) * 0.5).clip(0, 1)
        spec = np.exp(-(((dx + 0.35) ** 2 + (dy + 0.4) ** 2) / 0.05))
        return (base + amp * lam + 0.3 * spec).clip(0, 1)
    return f


def flat(v, grad=0.18):
    """Surface plane, un peu plus claire en haut."""
    def f(X, Y):
        return (v + grad * (0.5 - Y / Y.max())).clip(0, 1)
    return f


def plane_lit(v=0.62, depth=0.4, y0=0, y1=42):
    """Surface vue de dessus (aile, plan) : claire au bord d'attaque, plus sombre vers l'arrière."""
    def f(X, Y):
        t = ((Y - y0) / max(1, y1 - y0)).clip(0, 1)
        return (v + 0.15 - depth * t).clip(0, 1)
    return f


# ---------------------------------------------------------------- peinture
def gradient_map(lum, stops):
    ts = np.array([s[0] for s in stops])
    cols = np.array([s[1] for s in stops], np.float32)
    out = np.zeros(lum.shape + (3,), np.float32)
    for ch in range(3):
        out[..., ch] = np.interp(lum, ts, cols[:, ch])
    return out


def edge(alpha, px=1.0):
    m = Image.fromarray((alpha * 255).astype(np.uint8))
    er = np.asarray(m.filter(ImageFilter.MinFilter(int(K * px) | 1)), np.float32) / 255
    return (alpha - er).clip(0, 1)


def rim(alpha, px=1.0):
    m = Image.fromarray((alpha * 255).astype(np.uint8))
    sh = Image.new("L", m.size, 0)
    d = int(K * px)
    sh.paste(m, (d, d))
    return (alpha - np.asarray(sh, np.float32) / 255).clip(0, 1)


def grain(c, amt):
    n = RNG.normal(0, 1, (c.h * 2, c.w * 2)).astype(np.float32)
    n = np.asarray(Image.fromarray(((n * 40) + 128).clip(0, 255).astype(np.uint8))
                   .resize((c.w * K, c.h * K), Image.BILINEAR), np.float32)
    return (c.lum + (n / 255 - 0.5) * amt).clip(0, 1)


def downscale(rgba, w, h):
    return Image.fromarray(np.clip(rgba, 0, 255).astype(np.uint8), "RGBA").resize((w, h), Image.LANCZOS)


def with_shadow(img, strength=0.75, dx=1, dy=1, blur=1.1):
    a = img.split()[3]
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    m = Image.new("L", img.size, 0)
    m.paste(a, (dx, dy))
    out.putalpha(m.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * strength)))
    out.alpha_composite(img)
    return out


def paint(c, scale=1.0):
    """Style C3 · Plan acier ; slots vides en vert pâle en relief (convention du vanilla)."""
    if c.slot:
        col = gradient_map(c.lum, [(0, (20, 34, 22)), (0.5, (86, 120, 84)), (1, (190, 220, 180))])
        col = col * (1 - c.accent[..., None] * 0.55) + np.array([226, 250, 204]) * c.accent[..., None] * 0.55
        r = rim(c.alpha, 0.9)
        col = col * (1 - r[..., None] * 0.7) + np.array([200, 245, 255]) * r[..., None] * 0.7
        img = with_shadow(downscale(np.dstack([col, c.alpha * 255]), round(c.w * scale), round(c.h * scale)), 0.9)
    else:
        lum = grain(c, 0.12)
        ln = np.maximum(c.lines, edge(c.alpha, 0.7)) * 0.85
        base = gradient_map(lum, [(0, (10, 22, 36)), (0.5, (34, 70, 104)), (1, (96, 150, 192))])
        base = base * (1 - c.accent[..., None] * 0.6) + np.array([110, 200, 240]) * c.accent[..., None] * 0.6
        col = base * (1 - ln[..., None]) + np.array([206, 228, 244]) * ln[..., None]
        a = np.maximum(c.alpha * (0.78 + 0.22 * c.accent), ln) * 255
        img = with_shadow(downscale(np.dstack([col, a]), round(c.w * scale), round(c.h * scale)))
    return add_badges(img, c.badge)


def add_badges(img, badge):
    """Marques : palier ou classe en orangé du jeu (bas à droite), taille S/M/L en petit clair (haut à droite)."""
    if not badge:
        return img
    marks = badge if isinstance(badge, list) else [badge]
    S = 4
    w, h = img.size
    layer = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for text, kind in marks:
        if kind in ("tier", "class"):
            f = ImageFont.truetype(str(FONTS / "georgiab.ttf"), int(15 * S * (h / 42) ** 0.3))
            tw, th = d.textbbox((0, 0), text, font=f)[2:]
            x, y = w * S - tw - 2 * S, h * S - th - 3 * S
            d.text((x, y), text, font=f, fill=(0, 0, 0, 255), stroke_width=int(1.4 * S), stroke_fill=(20, 10, 0, 230))
            m = Image.new("L", layer.size, 0)
            ImageDraw.Draw(m).text((x, y), text, font=f, fill=255)
            t = np.linspace(0, 1, h * S)[:, None]
            k = ((t - y / (h * S)) / (th / (h * S))).clip(0, 1)[..., None]
            grad = np.zeros((h * S, w * S, 4), np.float32)
            grad[..., :3] = np.array([255, 226, 120]) * (1 - k) + np.array([226, 92, 24]) * k
            grad[..., 3] = np.asarray(m, np.float32)
            layer.alpha_composite(Image.fromarray(grad.astype(np.uint8), "RGBA"))
        elif kind == "size":
            f = ImageFont.truetype(str(FONTS / "bahnschrift.ttf"), int(10 * S))
            tw, th = d.textbbox((0, 0), text, font=f)[2:]
            d.text((w * S - tw - 2 * S, 0.5 * S), text, font=f, fill=(214, 236, 250, 255),
                   stroke_width=int(1.1 * S), stroke_fill=(6, 16, 28, 235))
        elif kind == "count":
            f = ImageFont.truetype(str(FONTS / "bahnschrift.ttf"), int(9.5 * S))
            d.text((1.5 * S, h * S - 11.5 * S), text, font=f, fill=(214, 236, 250, 255),
                   stroke_width=int(1.1 * S), stroke_fill=(6, 16, 28, 235))
    out = img.copy()
    out.alpha_composite(layer.resize((w, h), Image.LANCZOS))
    return out


ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}


# ---------------------------------------------------------------- export
def save_dds(img, path):
    """DDS 32 bits A8R8G8B8 non compressé, sans mipmaps (comme les images du designer vanilla)."""
    img = img.convert("RGBA")
    w, h = img.size
    px = np.asarray(img, np.uint8)[..., [2, 1, 0, 3]].tobytes()          # B G R A
    head = struct.pack("<4s7I44x", b"DDS ", 124, 0x100F, h, w, w * 4, 0, 0)
    pf = struct.pack("<8I", 32, 0x41, 0, 32, 0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000)
    caps = struct.pack("<5I", 0x1000, 0, 0, 0, 0)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(head + pf + caps + px)


def sheet(items, path, title, Z=4, cols=8):
    """Planche de revue : chaque icône agrandie ×Z sur le fond du designer, avec son nom."""
    bg = Image.open("F:/Github Local/HOI4-ref/gfx/interface/equipementdesigner/planes/plane_designer_popup_bg.dds").convert("RGBA")
    tex = bg.crop((40, 200, 400, 420))
    lab = ImageFont.truetype(str(FONTS / "segoeui.ttf"), 13)
    tf = ImageFont.truetype(str(FONTS / "segoeuib.ttf"), 22)
    cw = max(i.width for _, i in items) * Z + 24
    ch = max(i.height for _, i in items) * Z + 54
    rows = math.ceil(len(items) / cols)
    out = Image.new("RGBA", (cols * cw + 20, rows * ch + 60), (24, 27, 30, 255))
    d = ImageDraw.Draw(out)
    d.text((14, 14), title, font=tf, fill=(235, 235, 235))
    for k, (name, img) in enumerate(items):
        x, y = 10 + (k % cols) * cw, 52 + (k // cols) * ch
        fw, fh = img.width * Z + 12, img.height * Z + 12
        out.alpha_composite(tex.resize((fw, fh)), (x, y))
        out.alpha_composite(img.resize((img.width * Z, img.height * Z), Image.NEAREST), (x + 6, y + 6))
        txt = name if d.textlength(name, font=lab) < cw - 8 else name[:int(len(name) * (cw - 8) / d.textlength(name, font=lab)) - 1] + "…"
        d.text((x, y + fh + 4), txt, font=lab, fill=(190, 196, 202))
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    out.save(path)
    return path
