const CACHE_NAME = 'Travel Game';

const FILES = [
    './index.html',
    './main.css',
    './sw.js',
    './'
]

// caches = Cache Storage API
// Cache = Cache API
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                return cache.addAll(FILES);
            })
    )

    // aggiornamento
    caches.keys()
        .then(
            cachesName => cachesName.map(name => {
                if(name !== CACHE_NAME){
                    caches.delete(name)
                }
            })
        )
})


self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(
                Response => Response ? Response : fetch(event.request)
            )
    )
})