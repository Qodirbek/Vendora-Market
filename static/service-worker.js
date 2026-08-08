const CACHE_NAME = 'vendora-v3';

// Keshlanishi kerak bo'lgan statik fayllar ro'yxati
const ASSETS_TO_CACHE = [
    '/',
    '/static/manifest.json',
    '/static/auth/login.css',
    '/static/auth/login.js',
    '/static/auth/register.css',
    '/static/auth/register.js'
];

// 1. INSTALL: Service Worker o'rnatilishi va fayllarni keshga saqlash
self.addEventListener('install', (event) => {
    self.skipWaiting(); // Yangi Service Worker'ni kutmasdan darhol faollashtirish
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            // Promise.allSettled - 1 ta fayl topilmasa ham qolganlarini keshlaydi va crash bermaydi
            return Promise.allSettled(
                ASSETS_TO_CACHE.map((url) =>
                    cache.add(url).catch((err) => {
                        console.warn("[SW] Keshga qo'shishda o'tkazib yuborildi (" + url + "):", err);
                    })
                )
            );
        })
    );
});

// 2. ACTIVATE: Eski kesh versiyalarini avtomatik o'chirish
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        console.log("[SW] Eski kesh o'chirildi:", cache);
                        return caches.delete(cache);
                    }
                })
            );
        }).then(() => self.clients.claim()) // Barcha ochiq varaqlarni (tab) darhol nazoratga olish
    );
});

// 3. FETCH: Tarmoq so'rovlarini ushlash va keshdan xizmat ko'rsatish
self.addEventListener('fetch', (event) => {
    // Faqat GET so'rovlarini ushlaymiz (POST, PUT va Firebase API so'rovlariga tegmaydi)
    if (event.request.method !== 'GET') return;

    // HTTP va HTTPS bo'lmagan so'rovlarni (masalan, chrome-extension://) o'tkazib yuboramiz
    if (!event.request.url.startsWith('http')) return;

    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            // 1. Agar fayl keshda bo'lsa, keshdan beramiz
            if (cachedResponse) {
                return cachedResponse;
            }

            // 2. Aks holda serverdan yuklaymiz
            return fetch(event.request).catch(() => {
                // Tarmoq bo'lmaganda va keshda fayl topilmaganda TypeError crash bermasligi uchun Response obyektini qaytaramiz
                return new Response("Internet aloqasi yo'q yoki manbaa topilmadi", {
                    status: 503,
                    statusText: "Service Unavailable",
                    headers: new Headers({ "Content-Type": "text/plain; charset=utf-8" })
                });
            });
        })
    );
});
