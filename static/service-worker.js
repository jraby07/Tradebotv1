self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('tradebot-v1').then((cache) => cache.addAll([
            '/',
            '/index.html',
            '/main.js',
            '/manifest.json',
            '/service-worker.js',
        ]))
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => response || fetch(event.request))
    );
});
