"""Reconstruit le bloc « Par thème » de articles/index.html à partir de donnees.THEMES.
Usage : python3 _outils/themes.py"""
import re, html, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from donnees import THEMES
os.chdir(os.path.join(os.path.dirname(__file__), ".."))
def titre(slug):
    t = open(f"articles/{slug}/index.html").read()
    h = re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S).group(1)
    return html.unescape(re.sub("<[^>]+>", "", h)).replace("\xa0", " ").strip()
blocs = "".join(
    f'<div><h3>{html.escape(nom)}</h3><ul>' + "".join(f'<li><a href="/articles/{s}/">{html.escape(titre(s))}</a></li>' for s in slugs) + "</ul></div>"
    for nom, slugs in THEMES)
bloc = ('<!-- THEMES:debut (généré par _outils/themes.py) -->\n<section class="band"><div class="in stack">\n  <h2 class="sectitle">Par thème</h2>\n'
        f'  <div class="themes">{blocs}</div>\n</div></section>\n<!-- THEMES:fin -->')
s = open("articles/index.html").read()
if "<!-- THEMES:debut" in s:
    s = re.sub(r"<!-- THEMES:debut.*?<!-- THEMES:fin -->", lambda m: bloc, s, flags=re.S)
else:
    s = s.replace('</div></section>\n<section class="band"><div class="in">\n<!-- LISTE-ARTICLES', '</div></section>\n' + bloc + '\n<section class="band"><div class="in">\n  <h2 class="sectitle">Tous les articles, du plus récent au plus ancien</h2>\n<!-- LISTE-ARTICLES', 1)
open("articles/index.html", "w").write(s)
print("thèmes à jour")
