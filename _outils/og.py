"""Génère les images de partage (img/og/<page>.png, 1200x630), le logo et les favicons.
Pour chaque page qui déclare og:image, reprend son h1, la couleur de son bandeau et son croquis d'en-tête.
Usage : python3 _outils/og.py [--tout]   (sans --tout, ne refait que les images manquantes)"""
import re, os, sys, html, subprocess, pathlib
from playwright.sync_api import sync_playwright
RAC = pathlib.Path(__file__).resolve().parent.parent
os.chdir(RAC)
COUL = {"bleu": ("#4A62A6", "#F3EDE2"), "jaune": ("#D9AE4B", "#1F1D1A"), "vert": ("#8FA47E", "#1F1D1A"),
        "rose": ("#DFA5A2", "#1F1D1A"), "rouge": ("#E6DCCB", "#1F1D1A")}
import base64
def _police(nom, fichier, poids):
    d = base64.b64encode((RAC / "_outils/polices" / fichier).read_bytes()).decode()
    return f"@font-face{{font-family:'{nom}';src:url(data:font/woff2;base64,{d}) format('woff2');font-weight:{poids}}}"
FONTS = "<style>" + _police("Bowlby One", "bowlby-one-latin-400-normal.woff2", 400) + _police("Courier Prime", "courier-prime-latin-700-normal.woff2", 700) + "</style>"
def gabarit(titre, croquis, fond, encre, label):
    svg = (RAC / "img/croquis" / f"{croquis}.svg").read_text()
    taille = 84 if len(titre) < 34 else 70 if len(titre) < 52 else 60
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
body{{margin:0;width:1200px;height:630px;background:{fond};color:{encre};font-family:'Courier Prime',monospace;position:relative;overflow:hidden}}
.cadre{{position:absolute;inset:28px;border:2px solid #1F1D1A}}
.lab{{position:absolute;left:64px;top:60px;font-weight:700;font-size:26px;letter-spacing:.2em;text-transform:uppercase}}
h1{{position:absolute;left:64px;top:130px;width:720px;margin:0;font-family:'Bowlby One',Impact,sans-serif;font-weight:400;font-size:{taille}px;line-height:1}}
.pied{{position:absolute;left:64px;bottom:60px;font-weight:700;font-size:28px;letter-spacing:.28em}}
.carte{{position:absolute;right:72px;top:120px;width:300px;height:360px;background:#F3EDE2;border:2px solid #1F1D1A;box-shadow:12px 12px 0 #1F1D1A;display:flex;align-items:center;justify-content:center}}
.carte svg{{width:230px;height:290px}}
</style></head><body><div class="cadre"></div><div class="lab">{html.escape(label)}</div><h1>{html.escape(titre).replace(' :', '&nbsp;:').replace(' ?', '&nbsp;?').replace(' !', '&nbsp;!')}</h1>
<div class="pied">DUMBPHONES.FR</div><div class="carte">{svg}</div></body></html>"""

def pages():
    for f in subprocess.check_output(["git", "ls-files", "*.html"]).decode().split() + [str(p.relative_to(RAC)) for p in RAC.glob("*/index.html")]:
        s = open(f).read()
        m = re.search(r'og:image" content="https://dumbphones.fr/(img/og/[^"]+)"', s)
        if not m: continue
        h1 = html.unescape(re.sub("<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S).group(1))).replace("\xa0", " ").strip()
        band = re.search(r'class="band ([a-z]+) pagehead', s)
        cro = re.search(r'class="croquis-tete" src="/img/croquis/([a-z-]+)\.svg', s)
        label = "Article" if f.startswith("articles/") and f != "articles/index.html" else "Passer au dumbphone"
        yield m.group(1), h1, (cro.group(1) if cro else "clapet"), COUL.get(band.group(1) if band else "jaune", COUL["jaune"]), label

def main():
    tout = "--tout" in sys.argv
    os.makedirs("img/og", exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        vus = set()
        for chemin, h1, cro, (fond, encre), label in pages():
            if chemin in vus or (os.path.exists(chemin) and not tout): continue
            vus.add(chemin)
            pg.set_content(gabarit(h1, cro, fond, encre, label), wait_until="load")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(150)
            pg.screenshot(path=chemin, type="png")
            print("image", chemin)
        if tout or not os.path.exists("img/logo.png"):
            logo = f"""<!doctype html><html><head>{FONTS}<style>body{{margin:0}}div{{width:512px;height:512px;background:#4A62A6;display:flex;align-items:center;justify-content:center;font-family:'Bowlby One';font-size:128px;color:#1F1D1A;letter-spacing:-.02em}}span{{text-shadow:6px 6px 0 #F3EDE2}}</style></head><body><div><span>DUMB</span></div></body></html>"""
            for taille, nom in [(512, "img/logo.png"), (180, "img/apple-touch-icon.png"), (96, "img/favicon-96.png")]:
                pg.set_viewport_size({"width": 512, "height": 512})
                pg.set_content(logo if taille == 512 else logo.replace("DUMB</span>", "D</span>").replace("150px", "330px"), wait_until="load")
                pg.evaluate("document.fonts.ready")
                pg.wait_for_timeout(150)
                pg.screenshot(path="/tmp/_logo.png")
                pg2 = b.new_page(viewport={"width": taille, "height": taille})
                pg2.set_content(f'<body style="margin:0"><img src="data:image/png;base64,{__import__("base64").b64encode(open("/tmp/_logo.png","rb").read()).decode()}" style="width:{taille}px;height:{taille}px;display:block">')
                pg2.screenshot(path=nom); pg2.close()
                print("logo", nom)
        b.close()
main()
