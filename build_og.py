"""Build the 1200x630 Open Graph image (assets/og.png).

Renders an HTML composition with headless Chrome (no Pillow needed):
ZenIRL wordmark + tagline on the left, round watch-face screenshots on the
right, and a row of round game icons along the bottom.

    python3 build_og.py

Re-run whenever the lineup changes. Set CHROME to override the browser path.
"""
from __future__ import annotations
import os
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

# (slug, screenshot number, left %, top %, width %, z) inside the 560x560 cluster
WATCHES = [
    ("crown-darts", 1, 22, 20, 56, 3),
    ("helix-drop", 1, 0, 2, 36, 2),
    ("haptic-beat", 2, 66, 0, 32, 2),
    ("crown-pinball", 3, 2, 64, 33, 2),
    ("memory-buzz", 2, 62, 61, 38, 2),
]
ICONS = ["asteroid-field", "haptic-beat", "sphere-defense", "crown-snake", "spell-caster",
         "crown-lockpick", "crown-darts"]


def build_html() -> str:
    def u(rel: str) -> str:
        return "file://" + os.path.join(ROOT, rel)

    watches = "".join(
        f'<div class="w" style="left:{x}%;top:{y}%;width:{w}%;z-index:{z}"><div class="bz"><img src="{u(f"assets/games/{s}/screenshot-{n}.png")}"></div></div>'
        for s, n, x, y, w, z in WATCHES
    )
    icons = "".join(f'<img class="ic" src="{u(f"assets/games/{s}/icon.png")}">' for s in ICONS)
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1200px;height:630px;overflow:hidden}}
body{{font-family:-apple-system,'Helvetica Neue',Helvetica,Arial,sans-serif;color:#F5F2E8;position:relative;
 background:radial-gradient(520px 520px at 900px 300px,rgba(92,107,115,.55),rgba(92,107,115,0) 100%),linear-gradient(135deg,#1A1A1A,#2C2C2C)}}
.copy{{position:absolute;left:72px;top:96px;width:540px}}
.eyebrow{{font-size:20px;letter-spacing:7px;text-transform:uppercase;color:#B8B8B8;margin-bottom:22px}}
h1{{font-size:132px;font-weight:200;letter-spacing:10px;line-height:1;margin-bottom:26px}}
.tag{{font-size:35px;font-weight:300;line-height:1.25;color:#E4E0D4;white-space:nowrap}}
.facts{{position:absolute;left:72px;top:462px;font-size:22px;letter-spacing:1px;color:#B8B8B8}}
.icons{{position:absolute;left:72px;bottom:44px;display:flex;gap:14px}}
.ic{{width:58px;height:58px;border-radius:50%;box-shadow:0 0 0 2px #3a3a3a,0 6px 14px rgba(0,0,0,.5)}}
.cluster{{position:absolute;left:628px;top:36px;width:560px;height:560px}}
.w{{position:absolute}}
.bz{{position:relative;width:100%;aspect-ratio:1;border-radius:50%;padding:5.5%;
 background:conic-gradient(from 200deg,#8a9096,#34383b 18%,#6f757a 36%,#26292b 55%,#868c91 74%,#2d3033 90%,#8a9096);
 box-shadow:0 24px 44px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.08);isolation:isolate}}
.bz::before{{content:"";position:absolute;inset:3.6%;border-radius:50%;background:#050505}}
.bz::after{{content:"";position:absolute;right:-3.2%;top:41%;width:5.5%;height:18%;border-radius:4px;background:linear-gradient(90deg,#2c2f31,#8f959a 45%,#3a3e41);z-index:-1}}
.bz img{{position:relative;z-index:1;width:100%;height:100%;border-radius:50%;display:block;object-fit:cover}}
</style></head><body>
<div class="copy"><div class="eyebrow">Wear OS</div><h1>ZenIRL</h1><div class="tag">Games built for the round screen.</div></div>
<div class="facts">Offline &middot; No ads &middot; Crown and haptics</div>
<div class="icons">{icons}</div>
<div class="cluster">{watches}</div>
</body></html>"""


def main() -> None:
    out = os.path.join(ROOT, "assets", "og.png")
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "og.html")
        with open(page, "w", encoding="utf-8") as f:
            f.write(build_html())
        subprocess.run(
            [CHROME, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=1",
             f"--screenshot={out}", "--window-size=1200,630", "--virtual-time-budget=3000",
             "file://" + page],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
