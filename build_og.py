"""Build a 1200x630 Open Graph image for the landing page.

Composition: dark background, five published-game icons in a row at the
bottom-third, ZenIRL wordmark + tagline above. Output to /assets/og.png.
Re-run whenever the published lineup changes.
"""
from __future__ import annotations
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 630
BG_TOP = (26, 26, 26)
BG_BOTTOM = (44, 44, 44)
TEXT = (245, 242, 232)
MUTED = (168, 168, 168)

ICONS = [
    "assets/games/asteroid-field/icon.png",
    "assets/games/haptic-beat/icon.png",
    "assets/games/sphere-defense/icon.png",
    "assets/games/crown-snake/icon.png",
    "assets/games/spell-caster/icon.png",
]

def gradient_bg(size, top, bottom):
    img = Image.new("RGB", size, top)
    px = img.load()
    for y in range(size[1]):
        t = y / max(size[1] - 1, 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        for x in range(size[0]):
            px[x, y] = (r, g, b)
    return img

def load_font(size):
    # Try a few common font paths; fall back to default.
    for candidate in [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]:
        if os.path.exists(candidate):
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()

def main() -> None:
    img = gradient_bg((W, H), BG_TOP, BG_BOTTOM)
    draw = ImageDraw.Draw(img)

    title_font = load_font(96)
    tagline_font = load_font(34)

    title = "ZenIRL"
    tagline = "Games designed for your wrist."

    tb = draw.textbbox((0, 0), title, font=title_font)
    tw = tb[2] - tb[0]
    draw.text(((W - tw) // 2, 110), title, font=title_font, fill=TEXT, spacing=12)

    tb = draw.textbbox((0, 0), tagline, font=tagline_font)
    tw = tb[2] - tb[0]
    draw.text(((W - tw) // 2, 230), tagline, font=tagline_font, fill=MUTED)

    # Icon row
    icon_size = 144
    gap = 28
    total_w = icon_size * len(ICONS) + gap * (len(ICONS) - 1)
    start_x = (W - total_w) // 2
    y = 360
    for i, rel in enumerate(ICONS):
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        ic = Image.open(path).convert("RGBA").resize(
            (icon_size, icon_size), Image.LANCZOS
        )
        # Slight drop-shadow under each icon for depth.
        shadow = Image.new("RGBA", (icon_size + 20, icon_size + 20), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.rounded_rectangle(
            (10, 14, 10 + icon_size, 14 + icon_size),
            radius=32, fill=(0, 0, 0, 110),
        )
        img.paste(shadow, (start_x + (icon_size + gap) * i - 10, y), shadow)
        img.paste(ic, (start_x + (icon_size + gap) * i, y), ic)

    out = os.path.join(ROOT, "assets", "og.png")
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({W}x{H})")


if __name__ == "__main__":
    main()
