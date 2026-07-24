/* 艺术卡片 Service Worker —— 离线可用 + 图片缓存 */
const VER = 'ac-v12';
const SHELL = VER + '-shell';
const IMG = VER + '-img';
const APP = [
  './', './index.html', './data.js', './manifest.webmanifest',
  './icon-192.png', './icon-512.png', './apple-touch-icon.png'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(SHELL).then(c => c.addAll(APP)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => !k.startsWith(VER)).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // 维基图片:cache-first,首次看过即离线可用
  if (url.hostname.endsWith('upload.wikimedia.org')) {
    e.respondWith(
      caches.open(IMG).then(async c => {
        const hit = await c.match(req);
        if (hit) return hit;
        try {
          const res = await fetch(req);
          if (res && (res.ok || res.type === 'opaque')) c.put(req, res.clone());
          return res;
        } catch (_) { return hit || Response.error(); }
      })
    );
    return;
  }

  // 同源(App 文件)
  if (url.origin === self.location.origin) {
    // data.js:network-first —— 数据频繁更新,在线时总取最新,离线才回退缓存
    if (url.pathname.endsWith('data.js')) {
      e.respondWith(
        caches.open(SHELL).then(async c => {
          try { const res = await fetch(req); if (res && res.ok) c.put(req, res.clone()); return res; }
          catch (_) { return (await c.match(req)) || fetch(req); }
        })
      );
      return;
    }
    // 其余 App 文件:stale-while-revalidate,离线也能开、上线又能更新
    e.respondWith(
      caches.open(SHELL).then(async c => {
        const hit = await c.match(req);
        const net = fetch(req).then(res => { if (res && res.ok) c.put(req, res.clone()); return res; }).catch(() => null);
        return hit || net || fetch(req);
      })
    );
  }
});
