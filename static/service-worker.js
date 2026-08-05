const CACHE_NAME = "vendora-v1";

const FILES = [
    "/",
    "/static/style.css",
    "/static/js/app.js"
];


self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
        .then(cache => {
            return cache.addAll(FILES);
        })
    );
});


self.addEventListener("fetch", event => {

    event.respondWith(
        caches.match(event.request)
        .then(response => {

            return response || fetch(event.request);

        })
    );

});