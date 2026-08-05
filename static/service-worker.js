const CACHE_NAME = "vendora-v1";


const FILES = [
    "/",
    "/static/css/style.css",
    "/static/js/app.js",
    "/static/manifest.json"
];


self.addEventListener(
"install",
event => {

event.waitUntil(

caches.open(CACHE_NAME)
.then(cache => {

return cache.addAll(FILES);

})

);

});


self.addEventListener(
"fetch",
event => {


event.respondWith(

caches.match(event.request)
.then(response => {

return response || fetch(event.request);

})

);


});