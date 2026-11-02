/* Newsletter DUMB : popup « guide offert » + formulaires intégrés.
   Les inscriptions vont dans Brevo. Tant que BREVO_ACTION est vide, rien ne s'affiche.
   Pour l'activer : coller l'adresse du formulaire Brevo (Contacts > Formulaires > Partager > lien du formulaire,
   du type https://xxxx.sibforms.com/serve/XXXX) entre les guillemets. */
(function () {
  var BREVO_ACTION = "https://8cad817e.sibforms.com/serve/MUIFAFEEKQY0DOWu9faI24Neh9X5X2MprYni1nPnfgpwoNAEiVCDtZ2LvBugpW4VL-azPelAmrmoXchTC2gFnSryCehsIezXTi3oaEy-V9o49Sl10ZMa_Iamtso2G_F-wdFXz_Ld30Sa7jzPiK32WpuEd2M-5IFXrgPLJVTj2jCkXghBGzCZYBJFOo5yoRLG3Se5B2v6s_3GUQzdZw==";
  var DELAI_MS = 20000;          // popup après 20 s sur la page
  var SCROLL = 0.6;              // ou après 60 % de la page lue
  var PAUSE_JOURS = 14;          // ne revient pas pendant 14 jours si on la ferme
  var CLE = "dumb-nl";

  if (!BREVO_ACTION) return;
  var path = location.pathname;
  var pageSansPopup = /^\/(merci|liens)\//.test(path);

  function lire() { try { return JSON.parse(localStorage.getItem(CLE) || "{}"); } catch (e) { return {}; } }
  function ecrire(v) { try { localStorage.setItem(CLE, JSON.stringify(v)); } catch (e) {} }

  function envoyer(form, ok) {
    var email = form.querySelector('input[type="email"]');
    if (!email.value || !email.checkValidity()) { email.focus(); email.reportValidity && email.reportValidity(); return; }
    var data = new FormData();
    data.append("EMAIL", email.value.trim());
    data.append("email_address_check", "");
    data.append("locale", "fr");
    var bouton = form.querySelector("button");
    bouton.disabled = true; bouton.textContent = "Envoi…";
    fetch(BREVO_ACTION + (BREVO_ACTION.indexOf("?") < 0 ? "?" : "&") + "isAjax=1", { method: "POST", body: data, mode: "no-cors" })
      .then(function () {
        ecrire({ inscrit: true });
        ok.hidden = false; form.hidden = true;
        if (window.goatcounter && window.goatcounter.count) window.goatcounter.count({ path: "newsletter-inscription", event: true });
      })
      .catch(function () {
        bouton.disabled = false; bouton.textContent = "Réessayer";
        ok.hidden = false; ok.textContent = "L'envoi n'a pas marché. Vérifie ta connexion et réessaie.";
      });
  }

  function brancher(racine) {
    var form = racine.querySelector("form"), ok = racine.querySelector(".nl-ok");
    form.addEventListener("submit", function (e) { e.preventDefault(); envoyer(form, ok); });
  }

  // formulaires intégrés aux pages (cachés tant que la newsletter n'est pas active)
  document.querySelectorAll(".nl-bloc").forEach(function (b) { b.hidden = false; brancher(b); });
  document.querySelectorAll(".nl-lien").forEach(function (a) { a.hidden = false; });

  var etat = lire();
  if (pageSansPopup || etat.inscrit || (etat.ferme && Date.now() - etat.ferme < PAUSE_JOURS * 864e5)) return;

  var html =
    '<div class="nl-pop" role="dialog" aria-modal="true" aria-labelledby="nl-titre" hidden>' +
      '<div class="nl-carte">' +
        '<button class="nl-x" type="button" aria-label="Fermer">×</button>' +
        '<p class="label">Offert</p>' +
        '<h2 id="nl-titre">Le guide pour lâcher ton smartphone, en PDF</h2>' +
        '<p>Inscris-toi à la newsletter DUMB : un mail tous les 15 jours, et le guide à imprimer dès ton inscription.</p>' +
        '<form novalidate>' +
          '<label for="nl-email-pop">Ton e-mail</label>' +
          '<input id="nl-email-pop" type="email" name="EMAIL" autocomplete="email" placeholder="toi@exemple.fr" required>' +
          '<button class="btn plein" type="submit">Recevoir le guide</button>' +
        '</form>' +
        '<p class="nl-ok" role="status" hidden>Presque fini : ouvre le mail de confirmation, le guide t\'attend juste après.</p>' +
        '<p class="nl-mini">Un mail tous les 15 jours, désinscription en un clic. Ton adresse sert seulement à DUMB, elle n\'est jamais revendue.</p>' +
      '</div>' +
    '</div>';
  var wrap = document.createElement("div"); wrap.innerHTML = html;
  var pop = wrap.firstChild; document.body.appendChild(pop);
  brancher(pop);

  var montre = false, avant = null;
  function ouvrir() {
    if (montre) return; montre = true;
    avant = document.activeElement;
    pop.hidden = false;
    setTimeout(function () { pop.querySelector("input").focus(); }, 30);
    window.removeEventListener("scroll", surScroll);
  }
  function fermer() {
    pop.hidden = true;
    if (!lire().inscrit) ecrire({ ferme: Date.now() });
    if (avant && avant.focus) avant.focus();
  }
  function surScroll() {
    var h = document.documentElement;
    if ((h.scrollTop + innerHeight) / h.scrollHeight > SCROLL) ouvrir();
  }
  pop.querySelector(".nl-x").addEventListener("click", fermer);
  pop.addEventListener("click", function (e) { if (e.target === pop) fermer(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !pop.hidden) fermer(); });
  setTimeout(ouvrir, DELAI_MS);
  window.addEventListener("scroll", surScroll, { passive: true });
})();
