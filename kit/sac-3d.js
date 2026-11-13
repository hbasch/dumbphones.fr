// Visionneuse Gaussian splatting de la musette.
// Le fichier est indiqué par data-src sur #sac-3d. Tant qu'il n'existe pas, on garde le texte d'attente.
// La scène se charge quand le cadre arrive à l'écran, puis la caméra se balance toute seule
// autour du sac (pas de contrôle à la souris).
const figure = document.getElementById('sac-3d');
const scene = figure && figure.querySelector('.kit-3d-scene');
const nombres = (v, defaut) => (v || defaut).split(',').map(Number);

async function existe(url) {
  try {
    const r = await fetch(url, { method: 'HEAD' });
    return r.ok;
  } catch (e) { return false; }
}

async function lancer(src) {
  scene.innerHTML = '<p class="kit-3d-attente">Chargement de la musette…</p>';
  try {
    const [GS, THREE] = await Promise.all([
      import('https://cdn.jsdelivr.net/npm/@mkkellogg/gaussian-splats-3d@0.4.7/build/gaussian-splats-3d.module.js'),
      import('three')
    ]);
    const depart = nombres(figure.dataset.camera, '0,-1,-4');
    const cible = new THREE.Vector3(...nombres(figure.dataset.cible, '0,0,0'));
    const haut = new THREE.Vector3(0, -1, 0);
    const viewer = new GS.Viewer({
      rootElement: scene,
      cameraUp: haut.toArray(),
      initialCameraPosition: depart,
      initialCameraLookAt: cible.toArray(),
      sharedMemoryForWorkers: false, // GitHub Pages n'envoie pas les en-têtes COOP/COEP
      gpuAcceleratedSort: false,
      dynamicScene: false,
      useBuiltInControls: false
    });
    await viewer.addSplatScene(src, { showLoadingUI: false, progressiveLoad: true });
    scene.querySelector('.kit-3d-attente')?.remove();

    // Mouvement : balancier lent de gauche à droite, petite respiration haut/bas et avant/arrière.
    const ecart = new THREE.Vector3(...depart).sub(cible);
    const cote = new THREE.Vector3().crossVectors(haut, ecart).normalize();
    const calme = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const t0 = performance.now();
    const q = new THREE.Quaternion();
    const v = new THREE.Vector3();
    function bouger() {
      const t = calme ? 0 : (performance.now() - t0) / 1000;
      v.copy(ecart);
      q.setFromAxisAngle(haut, 0.45 * Math.sin(t * 0.35));
      v.applyQuaternion(q);
      q.setFromAxisAngle(cote, 0.12 * Math.sin(t * 0.23));
      v.applyQuaternion(q);
      v.multiplyScalar(1 + 0.08 * Math.sin(t * 0.17));
      viewer.camera.position.copy(cible).add(v);
      viewer.camera.up.copy(haut);
      viewer.camera.lookAt(cible);
      requestAnimationFrame(bouger);
    }
    viewer.start();
    bouger();
  } catch (e) {
    scene.innerHTML = '<p class="kit-3d-attente">La 3D ne marche pas sur ce navigateur. Désolé !</p>';
  }
}

(async () => {
  if (!figure) return;
  const src = figure.dataset.src;
  if (!(await existe(src))) return;
  scene.innerHTML = '';
  new IntersectionObserver((entrees, obs) => {
    if (entrees.some(e => e.isIntersecting)) { obs.disconnect(); lancer(src); }
  }, { rootMargin: '200px' }).observe(figure);
})();
