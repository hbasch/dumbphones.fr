# Sujets d'articles (file d'attente)
Prendre le premier sujet non coché, puis le cocher. Ajouter de nouveaux sujets en bas quand la liste se vide.

À chaque nouvel article, mettre aussi à jour : le bloc ARTICLES-ACCUEIL de /index.html (les 3 plus récents, le plus récent en haut, même format que la liste de /articles/). Titre de page : la question que les gens tapent dans Google, avec « 2026 » quand ça a du sens, 60 caractères maximum.

Structure d'un article (depuis le 12 novembre 2026, copier l'article le plus récent) :
- En-tête : og:image (https://dumbphones.fr/img/og/<slug>.png) et og:image:alt, favicons, données structurées Article (auteur Person Hadrien Basch, publisher avec logo, image, datePublished et dateModified) et BreadcrumbList (Accueil, Articles, titre).
- Bandeau : classe « in stack a-croquis », image <img class="croquis-tete" src="/img/croquis/<nom>.svg" alt="" width="160" height="160">, puis le fil d'Ariane. Croquis disponibles dans img/croquis/ ; pour en ajouter un, modifier _outils/croquis.py puis lancer python3 _outils/croquis.py.
- Fin : bloc <aside class="a-lire"> « À lire aussi » (3 articles du même thème) et « Écrit par Hadrien Basch, fondateur de DUMB. ».
- Fiche modèle (/telephones/<modele>/) : même gabarit, fil d'Ariane Accueil › Comparateur › modèle, lien depuis le comparateur via le champ avis du tableau T (pas le champ lien), puis recopier les cartes générées dans #cartes.

Après l'article, lancer dans l'ordre :
1. ajouter le slug au bon thème (THEMES) et son croquis (CROQUIS) dans _outils/donnees.py, puis python3 _outils/themes.py ;
2. python3 _outils/og.py (crée l'image de partage manquante, Playwright est installé ; regarder l'image) ;
3. python3 _outils/sitemap.py (régénère sitemap.xml, ne plus l'éditer à la main).
Ces fichiers (_outils/, img/og/, sitemap.xml, articles/index.html) font partie des fichiers autorisés pour un article. Faire git pull --rebase avant de pousser.

- [x] Téléphone sans internet pour un ado : lequel choisir en 2026
- [x] Garder WhatsApp sans smartphone : toutes les options
- [x] Passer au dumbphone et garder sa banque : ce que proposent les banques françaises
- [x] Se repérer sans GPS : cartes papier, préparation de trajet, astuces
- [x] La double authentification sans smartphone : clés de sécurité, SMS, codes de secours
- [x] Idées cadeaux de Noël pour décrocher : objets, livres, téléphones simples (à publier avant fin novembre)
- [x] Téléphone pour senior : lequel choisir en 2026 (grosses touches, VoLTE, touche d'urgence)
- [x] Les meilleurs dumbphones de 2026 en France : notre sélection par usage
- [x] Téléphone à touches avec WhatsApp en 2026 : ceux qui marchent encore
- [x] Téléphone portable sans internet : lequel choisir en 2026
- [x] VoLTE : pourquoi ton vieux téléphone risque de ne plus marcher avec la fin de la 2G et de la 3G
- [x] Nokia 3210 4G ou Nokia 2660 Flip : lequel choisir ?
- [x] Rendre son iPhone ennuyeux en 10 minutes
- [x] Rendre son Android ennuyeux : les meilleurs lanceurs minimalistes
- [x] Un réveil pour sortir le téléphone de la chambre
- [x] Écouter de la musique et des podcasts sans smartphone
- [x] 30 jours sans smartphone : à quoi s'attendre semaine par semaine
- [x] Mudita Kompakt, Light Phone III, Minimal Phone : les téléphones minimalistes haut de gamme comparés
- [x] Les billets de train et transports sans smartphone en France
- [x] Ce que dit la recherche sur les écrans et l'attention
- [ ] Le carnet papier : remplacer les notes, listes et agenda du téléphone

## Fiches modèles (une page par téléphone du comparateur, à faire après la file ci-dessus)
Page /telephones/<modele>/ : avis, ce qui marche (WhatsApp, VoLTE, bandes 4G françaises, autonomie), prix relevé avec la date, pour qui, liens vers le comparateur. Ne mettre que des caractéristiques vérifiées sur la fiche du fabricant.
- [ ] Nokia 2660 Flip
- [ ] Nokia 3210 4G
- [ ] Crosscall Core-S5
- [ ] Qin F21 Pro
- [ ] Mudita Kompakt
- [ ] Light Phone III
