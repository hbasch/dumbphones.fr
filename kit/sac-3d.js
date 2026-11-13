// Visionneuse Gaussian splatting de la musette.
// Le fichier est indiqué par data-src sur #sac-3d. Tant qu'il n'existe pas, on garde le texte d'attente.
// Rien n'est téléchargé avant que le visiteur clique : le fichier fait plusieurs Mo.
const figure = document.getElementById('sac-3d');
const scene = figure && figure.querySelector('.kit-3d-scene');

async function existe(url) {
  try {
    const r = await fetch(url, { method: 'HEAD' });
    if (!r.ok) return 0;
    return Number(r.headers.get('content-length')) || 1;
  } catch (e) { return 0; }
}

async function lancer(src) {
  scene.innerHTML = '<p class="kit-3d-attente">Chargement de la musette…</p>';
  try {
    const GS = await import('https://cdn.jsdelivr.net/npm/@mkkellogg/gaussian-splats-3d@0.4.7/build/gaussian-splats-3d.module.js');
    const viewer = new GS.Viewer({
      rootElement: scene,
      cameraUp: [0, -1, 0],
      initialCameraPosition: [0, -1, -4],
      initialCameraLookAt: [0, 0, 0],
      sharedMemoryForWorkers: false, // GitHub Pages n'envoie pas les en-têtes COOP/COEP
      gpuAcceleratedSort: false,
      dynamicScene: false,
      useBuiltInControls: true
    });
    await viewer.addSplatScene(src, { showLoadingUI: false, progressiveLoad: true });
    scene.querySelector('.kit-3d-attente')?.remove();
    viewer.start();
  } catch (e) {
    scene.innerHTML = '<p class="kit-3d-attente">La 3D ne marche pas sur ce navigateur. Désolé !</p>';
  }
}

(async () => {
  if (!figure) return;
  const src = figure.dataset.src;
  const taille = await existe(src);
  if (!taille) return;
  const mo = taille > 1 ? ' (' + Math.max(1, Math.round(taille / 1e6)) + ' Mo)' : '';
  scene.innerHTML = '';
  const bouton = document.createElement('button');
  bouton.type = 'button';
  bouton.className = 'kit-3d-bouton';
  bouton.textContent = 'Tourner autour du sac en 3D' + mo;
  bouton.addEventListener('click', () => lancer(src), { once: true });
  scene.appendChild(bouton);
})();
