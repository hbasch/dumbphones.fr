// Garde la page du minuteur sur le téléphone pour qu'elle s'ouvre même en mode avion.
const CACHE = 'dumb-pause-v1';
const FICHIERS = ['/pause/', '/style.css?v=14', '/favicon.svg'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FICHIERS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
// Réseau d'abord (pour avoir la dernière version), cache si pas de réseau.
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  const page = url.origin === location.origin && url.pathname.startsWith('/pause/');
  const style = url.origin === location.origin && (url.pathname === '/style.css' || url.pathname === '/favicon.svg');
  const polices = /fonts\.(googleapis|gstatic)\.com$/.test(url.hostname);
  if (!page && !style && !polices) return;
  e.respondWith(
    fetch(e.request).then(r => {
      if (r.ok || r.type === 'opaque') { const copie = r.clone(); caches.open(CACHE).then(c => c.put(page ? '/pause/' : e.request, copie)); }
      return r;
    }).catch(() => caches.match(page ? '/pause/' : e.request, { ignoreSearch: !page }))
  );
});
