const CACHE_NAME = 'vendora-v2';

// Keshlanishi kerak bo'lgan statik fayllar ro'yxati
const ASSETS_TO_CACHE = [
    '/',
    '/static/manifest.json',
    '/static/auth/login.css',
    '/static/auth/login.js',
    '/static/auth/register.css',
    '/static/auth/register.js'
];

// 1. INSTALL: Service Worker o'rnatilishi va fayllarni keshlash
self.addEventListener('install', (event) => {
    self.skipWaiting(); // Yangi Service Worker'ni kutmasdan darhol faollashtirish
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            // cache.addAll o'rniga Promise.allSettled ishlatamiz. 
            // Bu 1 ta fayl topilmay qolsa ham qolgan fayllar keshlanishini ta'minlaydi va crash xatosi bermaydi.
            return Promise.allSettled(
                ASSETS_TO_CACHE.map((url) =>
                    cache.add(url).catch((err) => {
                        console.warn(`[SW] Keshga qo'shishda o'tkazib yuborildi (${url}):`, err);
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
                        console.log('[SW] Eski kesh ochirildi:', cache);
                        return caches.delete(cache);
                    }
                })
            );
        }).then(() => self.clients.claim()) // Barcha ochiq varaqlarni (tab) darhol nazoratga olish
    );
});

// 3. FETCH: Tarmoq so'rovlarini ushlab qolish va keshdan xizmat ko'rsatish
self.addEventListener('fetch', (event) => {
    // Faqat GET so'rovlarini keshlaymiz (POST login formalar, Firebase Auth va API so'rovlariga tegmaydi)
    if (event.request.method !== 'GET') return;

    // HTTP va HTTPS bo'lmagan so'rovlarni (masalan, chrome-extension://) o'tkazib yuboramiz
    if (!event.request.url.startsWith('http')) return;

    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            // 1. Agar fayl keshda bor bo'lsa, keshdan beramiz
            if (cachedResponse) {
                return cachedResponse;
            }

            // 2. Aks holda serverdan yuklaymiz
            return fetch(event.request).catch((err) => {
                console.warn('[SW] Tarmoq sorovi amalga oshmadi va keshda topilmadi:', err);
            });
        })
    );
});
