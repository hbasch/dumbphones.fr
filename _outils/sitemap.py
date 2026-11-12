"""Régénère sitemap.xml : toutes les pages indexables (sans noindex), avec la date de dernière
modification (dernier commit du fichier, ou aujourd'hui s'il a des changements non commités) et l'image de partage.
Usage : python3 _outils/sitemap.py"""
import subprocess, re, os, datetime, pathlib
RAC = pathlib.Path(__file__).resolve().parent.parent
os.chdir(RAC)
auj = datetime.date.today().isoformat()
modif = set(subprocess.check_output(["git", "status", "--porcelain"]).decode().split("\n"))
modif = {l[3:].strip() for l in modif if l}
fichiers = sorted(set(subprocess.check_output(["git", "ls-files", "*.html"]).decode().split()) | {str(p.relative_to(RAC)) for p in RAC.glob("*/index.html")} | {str(p.relative_to(RAC)) for p in RAC.glob("*/*/index.html")})
lignes = []
for f in fichiers:
    if f.startswith("_"): continue
    s = open(f).read()
    if "noindex" in s: continue
    can = re.search(r'rel="canonical" href="([^"]+)"', s)
    if not can: continue
    if any(f == m or f.startswith(m) for m in modif):
        d = auj
    else:
        d = subprocess.check_output(["git", "log", "-1", "--format=%cs", "--", f]).decode().strip() or auj
    img = re.search(r'og:image" content="([^"]+)"', s)
    im = f"<image:image><image:loc>{img.group(1)}</image:loc></image:image>" if img else ""
    prio = 0 if can.group(1) == "https://dumbphones.fr/" else 1
    lignes.append((prio, can.group(1), f"  <url><loc>{can.group(1)}</loc><lastmod>{d}</lastmod>{im}</url>"))
lignes.sort(key=lambda x: (x[0], x[1]))
xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
       + "\n".join(l for _, _, l in lignes) + "\n</urlset>\n")
open("sitemap.xml", "w").write(xml)
print(len(lignes), "URL")
