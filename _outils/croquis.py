"""Génère les croquis SVG du site (img/croquis/*.svg), dans le style de l'accueil.
Chaque croquis = une couche d'aplats (filtre riso) + une couche de traits (filtre main).
Usage : python3 _outils/croquis.py"""
import os, re
O, R, S, B, P, K, E, BL = "#d9ae4b", "#dfa5a2", "#8fa47e", "#4a62a6", "#f3ede2", "#e6dccb", "#1f1d1a", "#9fb0d9"
DEFS = ('<defs><filter id="riso" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="1" seed="3" result="n"/>'
        '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0.96  0 0 0 0 0.94  0 0 0 0 0.9  0 0 0 12 -7.6" result="dots"/><feComposite in="dots" in2="SourceAlpha" operator="in" result="d2"/>'
        '<feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="d2"/></feMerge></filter><filter id="main" x="-5%" y="-5%" width="110%" height="110%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="9"/><feDisplacementMap in="SourceGraphic" scale="2.6"/></filter></defs>')

def keypad(x0, y0, cols=3, rows=4, w=14, h=10, gx=20, gy=14, fill=None, sw=1.6):
    out = []
    for r in range(rows):
        for c in range(cols):
            a = f'x="{x0+c*gx}" y="{y0+r*gy}" width="{w}" height="{h}" rx="3"'
            out.append(f'<rect {a} fill="{fill}"/>' if fill else f'<rect {a} stroke-width="{sw}"/>')
    return "".join(out)

C = {}
# Téléphone à clapet (repris de l'accueil)
C["clapet"] = ("0 0 124 150", "Croquis d'un téléphone à clapet",
 f'<g transform="rotate(-6 62 75)"><path d="M28 10h66c5 0 8 3 8 8v46H20V18c0-5 3-8 8-8z" fill="{O}"/><rect x="31" y="20" width="60" height="36" rx="3" fill="{BL}"/><rect x="20" y="64" width="82" height="6" fill="{E}"/><path d="M20 70h82v62c0 6-4 10-10 10H30c-6 0-10-4-10-10z" fill="{R}"/><ellipse cx="60" cy="82" rx="12" ry="5" fill="{O}"/>{keypad(33,93,rows=3,fill=P)}</g>',
 f'<g transform="rotate(-6 62 75)"><path d="M86 10V2"/><path d="M28 10h66c5 0 8 3 8 8v46H20V18c0-5 3-8 8-8z"/><path d="M50 15h22"/><rect x="31" y="20" width="60" height="36" rx="3"/><path d="M36 28h14M36 34h9" stroke-width="1.6"/><path d="M64 46c3-3 7-3 10 0 3-3 7-3 10 0" stroke-width="1.6"/><path d="M20 70h82v62c0 6-4 10-10 10H30c-6 0-10-4-10-10z"/><path d="M48 82h24"/>{keypad(33,93,rows=3)}<path d="M30 82h6M84 82h6"/></g><path d="M110 92c4 3 5 8 3 12M114 86c7 5 9 13 6 20" stroke-width="1.8"/>')
# Téléphone à touches (barre)
C["touches"] = ("0 0 110 160", "Croquis d'un téléphone à touches",
 f'<g transform="rotate(5 55 80)"><rect x="22" y="8" width="66" height="144" rx="14" fill="{S}"/><rect x="31" y="22" width="48" height="40" rx="3" fill="{BL}"/><ellipse cx="55" cy="76" rx="13" ry="6" fill="{O}"/>{keypad(30,90,fill=P,h=9,gy=13)}</g>',
 f'<g transform="rotate(5 55 80)"><rect x="22" y="8" width="66" height="144" rx="14"/><path d="M46 14h18"/><rect x="31" y="22" width="48" height="40" rx="3"/><path d="M36 30h12M36 36h20" stroke-width="1.6"/><path d="M58 52h16" stroke-width="1.6"/><path d="M42 76h26"/><path d="M30 76h5M75 76h5"/>{keypad(30,90,h=9,gy=13)}</g><path d="M96 30c4 3 5 8 3 12M100 24c7 5 9 13 6 20" stroke-width="1.8"/>')
# Téléphone tactile minimaliste (encre électronique)
C["tactile"] = ("0 0 110 160", "Croquis d'un téléphone minimaliste à écran tactile",
 f'<g transform="rotate(-4 55 80)"><rect x="18" y="6" width="74" height="148" rx="12" fill="{K}"/><rect x="26" y="20" width="58" height="112" rx="3" fill="{P}"/><circle cx="55" cy="143" r="5" fill="{O}"/></g>',
 f'<g transform="rotate(-4 55 80)"><rect x="18" y="6" width="74" height="148" rx="12"/><path d="M47 12h16"/><rect x="26" y="20" width="58" height="112" rx="3"/><path d="M34 34h24" stroke-width="3"/><path d="M34 50h32M34 62h22M34 74h28M34 86h18M34 98h26" stroke-width="1.6"/><circle cx="55" cy="143" r="5"/></g>')
# Smartphone rendu ennuyeux
C["smartphone"] = ("0 0 120 160", "Croquis d'un smartphone en noir et blanc",
 f'<g transform="rotate(4 60 80)"><rect x="22" y="6" width="76" height="148" rx="14" fill="{E}"/><rect x="28" y="16" width="64" height="128" rx="6" fill="#d8d3c9"/><rect x="36" y="30" width="48" height="10" fill="{P}"/></g>',
 f'<g transform="rotate(4 60 80)"><rect x="22" y="6" width="76" height="148" rx="14"/><rect x="28" y="16" width="64" height="128" rx="6"/><path d="M52 11h16"/><path d="M40 35h28" stroke-width="2.6"/><path d="M40 58h30M40 72h22M40 86h26M40 100h18" stroke-width="1.8"/><path d="M48 130h24" stroke-width="1.4"/></g><path d="M6 60l10 4M4 76h11M6 92l10-4" stroke-width="1.6"/>')
# Réveil (repris de l'accueil)
ticks = "".join(f'<path d="M{a}"/>' for a in ["55.0 39.0l0.0 -3.0","70.5 43.2l1.5 -2.6","81.8 54.5l2.6 -1.5","86.0 70.0l3.0 0.0","81.8 85.5l2.6 1.5","70.5 96.8l1.5 2.6","55.0 101.0l-0.0 3.0","39.5 96.8l-1.5 2.6","28.2 85.5l-2.6 1.5","24.0 70.0l-3.0 -0.0","28.2 54.5l-2.6 -1.5","39.5 43.2l-1.5 -2.6"])
C["reveil"] = ("0 0 112 132", "Croquis d'un réveil à aiguilles",
 f'<path d="M14 34c-4-14 8-26 24-22z" fill="{O}"/><path d="M96 34c4-14-8-26-24-22z" fill="{O}"/><rect x="51" y="10" width="8" height="12" fill="{E}"/><circle cx="55" cy="70" r="44" fill="{R}"/><circle cx="55" cy="70" r="35" fill="{P}"/><path d="M24 108l-10 18h8l12-14zM86 108l10 18h-8l-12-14z" fill="{E}"/>',
 f'<path d="M14 34c-4-14 8-26 24-22z"/><path d="M96 34c4-14-8-26-24-22z"/><path d="M44 10h22"/><circle cx="55" cy="70" r="44"/><circle cx="55" cy="70" r="35"/>{ticks}<path d="M55 70V46" stroke-width="3"/><path d="M55 70l17 10" stroke-width="3"/><circle cx="55" cy="70" r="2.5" fill="{E}"/><path d="M78 100c-6 6-14 9-23 9" stroke-width="1.4"/>')
# Sablier (repris de l'accueil)
C["sablier"] = ("0 0 96 140", "Croquis d'un sablier",
 f'<rect x="6" y="4" width="84" height="12" rx="3" fill="{S}"/><rect x="6" y="124" width="84" height="12" rx="3" fill="{S}"/><rect x="13" y="16" width="7" height="108" fill="{O}"/><rect x="76" y="16" width="7" height="108" fill="{O}"/><path d="M26 18c0 28 8 40 22 52-14 12-22 24-22 52h44c0-28-8-40-22-52 14-12 22-24 22-52z" fill="{P}"/><path d="M34 34c8 6 20 6 28 0-2 12-8 22-14 28-6-6-12-16-14-28z" fill="{O}"/><path d="M30 120c2-16 32-16 36 0z" fill="{O}"/>',
 '<rect x="6" y="4" width="84" height="12" rx="3"/><rect x="6" y="124" width="84" height="12" rx="3"/><path d="M16 16v108M80 16v108"/><path d="M26 18c0 28 8 40 22 52-14 12-22 24-22 52h44c0-28-8-40-22-52 14-12 22-24 22-52z"/><path d="M48 70v42" stroke-dasharray="1 6" stroke-width="2.4"/><path d="M32 26c4 2 8 3 12 3" stroke-width="1.4"/>')
# Carte papier pliée
C["carte"] = ("0 0 160 130", "Croquis d'une carte papier dépliée",
 f'<path d="M10 22l44-12 52 12 44-12v98l-44 12-52-12-44 12z" fill="{K}"/><path d="M54 10v98l52 12V22z" fill="{S}"/><circle cx="122" cy="44" r="9" fill="{R}"/>',
 '<path d="M10 22l44-12 52 12 44-12v98l-44 12-52-12-44 12z"/><path d="M54 10v98M106 22v98"/><path d="M22 96c14-8 20-24 36-26s24 14 40 4 14-26 22-28" stroke-dasharray="3 6" stroke-width="2"/><path d="M117 39l10 10M127 39l-10 10" stroke-width="2.6"/><path d="M20 40c8 4 16 2 24 6M66 34c10-2 16 6 28 4" stroke-width="1.2"/>')
# Billet de train
C["billet"] = ("0 0 170 110", "Croquis d'un billet de train imprimé",
 f'<g transform="rotate(-5 85 55)"><path d="M10 18h150v26a10 10 0 0 0 0 20v26H10V64a10 10 0 0 0 0-20z" fill="{P}"/><rect x="10" y="18" width="150" height="18" fill="{B}"/><rect x="118" y="50" width="30" height="30" fill="{O}"/></g>',
 '<g transform="rotate(-5 85 55)"><path d="M10 18h150v26a10 10 0 0 0 0 20v26H10V64a10 10 0 0 0 0-20z"/><path d="M10 36h150"/><path d="M106 36v54" stroke-dasharray="3 5" stroke-width="1.4"/><path d="M22 50h26M22 58h40M22 72h18M50 72l6 0M60 72h20" stroke-width="1.8"/><path d="M28 50l8-6 8 6" stroke-width="1.4"/><rect x="118" y="50" width="30" height="30"/><path d="M124 56h6v6h-6zM136 56h6v6h-6zM124 68h6v6h-6zM138 70h4v4" stroke-width="1.4"/></g>')
# Carnet et crayon
C["carnet"] = ("0 0 150 140", "Croquis d'un carnet et d'un crayon",
 f'<rect x="20" y="12" width="88" height="116" rx="4" fill="{O}"/><rect x="30" y="12" width="78" height="116" fill="{P}"/><path d="M118 20l14 4-18 100-8 8-2-12z" fill="{R}"/>',
 '<rect x="20" y="12" width="88" height="116" rx="4"/><path d="M30 12v116"/><path d="M16 26h10M16 44h10M16 62h10M16 80h10M16 98h10M16 116h10" stroke-width="1.8"/><path d="M40 34h56M40 48h48M40 62h54M40 76h36M40 90h50" stroke-width="1.2"/><path d="M118 20l14 4-18 100-8 8-2-12z"/><path d="M104 120l10 4M120 26l-12 74" stroke-width="1.4"/>')
# Casque audio
C["casque"] = ("0 0 150 130", "Croquis d'un casque audio",
 f'<path d="M24 78C22 30 128 30 126 78" fill="none" stroke="{K}" stroke-width="10"/><rect x="14" y="70" width="28" height="44" rx="10" fill="{B}"/><rect x="108" y="70" width="28" height="44" rx="10" fill="{B}"/><rect x="34" y="76" width="12" height="32" rx="5" fill="{O}"/><rect x="104" y="76" width="12" height="32" rx="5" fill="{O}"/>',
 '<path d="M20 78C18 22 132 22 130 78M30 76C30 34 120 34 120 76" stroke-width="2"/><rect x="14" y="70" width="28" height="44" rx="10"/><rect x="108" y="70" width="28" height="44" rx="10"/><rect x="34" y="76" width="12" height="32" rx="5"/><rect x="104" y="76" width="12" height="32" rx="5"/><path d="M62 92c4-6 4-12 0-18M72 98c8-10 8-24 0-34" stroke-width="1.6"/>')
# Cadenas
C["cadenas"] = ("0 0 120 140", "Croquis d'un cadenas",
 f'<path d="M34 62V42c0-16 12-28 26-28s26 12 26 28v20" fill="none" stroke="{K}" stroke-width="9"/><rect x="18" y="60" width="84" height="70" rx="8" fill="{O}"/><circle cx="60" cy="90" r="8" fill="{E}"/>',
 '<path d="M30 62V42c0-18 13-32 30-32s30 14 30 32v20M40 62V42c0-12 9-22 20-22s20 10 20 22v20" stroke-width="2"/><rect x="18" y="60" width="84" height="70" rx="8"/><circle cx="60" cy="90" r="8"/><path d="M60 98v16" stroke-width="3"/><path d="M28 72h10" stroke-width="1.4"/>')
# Paquet cadeau
C["cadeau"] = ("0 0 140 140", "Croquis d'un paquet cadeau",
 f'<rect x="20" y="60" width="100" height="70" fill="{R}"/><rect x="14" y="44" width="112" height="18" fill="{S}"/><rect x="62" y="44" width="16" height="86" fill="{O}"/>',
 '<rect x="20" y="60" width="100" height="70"/><rect x="14" y="44" width="112" height="18"/><path d="M62 44v86M78 44v86"/><path d="M70 44c-10-18-34-24-36-12-2 10 20 12 36 12zM70 44c10-18 34-24 36-12 2 10-20 12-36 12z"/><path d="M30 76c6 4 12 4 18 0" stroke-width="1.2"/>')
# Musette (sac du kit, reprise de l'accueil)
C["musette"] = ("0 0 160 108", "Croquis de la musette DUMB",
 f'<path d="M38 40C40 6 120 6 122 40" fill="none" stroke="{K}" stroke-width="7"/><path d="M16 40h128l-8 62H24z" fill="{K}"/><path d="M16 40h128l-10 30c-34 10-74 10-108 0z" fill="{S}"/><rect x="70" y="58" width="20" height="16" fill="{O}"/><rect x="112" y="76" width="22" height="13" fill="{R}"/>',
 '<path d="M38 40C40 6 120 6 122 40M45 40C47 14 113 14 115 40" stroke-width="1.8"/><path d="M16 40h128l-8 62H24z"/><path d="M16 40c4 10 6 20 10 30 34 10 74 10 108 0 4-10 6-20 10-30"/><path d="M30 64c32 8 68 8 100 0" stroke-dasharray="3 5" stroke-width="1.4"/><rect x="70" y="58" width="20" height="16"/><path d="M80 62v8"/><path d="M30 94c32 3 68 3 100 0" stroke-dasharray="3 5" stroke-width="1.4"/><rect x="112" y="76" width="22" height="13"/><path d="M116 82h14" stroke-width="1.4"/>')
# Bulle de message (messagerie, SMS)
C["message"] = ("0 0 150 130", "Croquis de deux bulles de message",
 f'<path d="M14 18h80c6 0 10 4 10 10v34c0 6-4 10-10 10H44l-18 16 4-16H14c-6 0-10-4-10-10V28c0-6 4-10 10-10z" fill="{BL}"/><path d="M66 58h66c6 0 10 4 10 10v28c0 6-4 10-10 10h-8l4 14-18-14H66c-6 0-10-4-10-10V68c0-6 4-10 10-10z" fill="{O}"/>',
 '<path d="M14 18h80c6 0 10 4 10 10v34c0 6-4 10-10 10H44l-18 16 4-16H14c-6 0-10-4-10-10V28c0-6 4-10 10-10z"/><path d="M20 36h56M20 48h38" stroke-width="1.6"/><path d="M66 58h66c6 0 10 4 10 10v28c0 6-4 10-10 10h-8l4 14-18-14H66c-6 0-10-4-10-10V68c0-6 4-10 10-10z"/><path d="M72 76h50M72 88h30" stroke-width="1.6"/>')

def svg(nom, vb, titre, aplats, traits, filters_inline=True):
    w, h = vb.split()[2:]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{vb}" role="img" aria-label="{titre}"><title>{titre}</title>{DEFS}'
            f'<g filter="url(#riso)">{aplats}</g><g filter="url(#main)" transform="translate(-3 -2)" fill="none" stroke="{E}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{traits}</g></svg>\n')

if __name__ == "__main__":
    racine = os.path.join(os.path.dirname(__file__), "..", "img", "croquis")
    os.makedirs(racine, exist_ok=True)
    for nom, (vb, titre, a, t) in C.items():
        open(os.path.join(racine, nom + ".svg"), "w").write(svg(nom, vb, titre, a, t))
    print(len(C), "croquis")
