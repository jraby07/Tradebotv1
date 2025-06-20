self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('tradebot-v1').then((cache) => cache.addAll([
            '/',
            '/index.html',
            '/main.js',
            '/manifest.json',
<<<<<<< HEAD
=======
            '/service-worker.js',
>>>>>>> pr8
        ]))
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => response || fetch(event.request))
    );
});
