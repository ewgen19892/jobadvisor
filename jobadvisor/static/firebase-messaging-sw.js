importScripts('https://www.gstatic.com/firebasejs/6.4.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/6.4.0/firebase-messaging.js');

firebase.initializeApp({
    'messagingSenderId': '540425893715'
});

const messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function (payload) {
    console.log('[firebase-messaging-sw.js] Received background message ', payload);
    const notificationTitle = 'JobAdvisor';
    const notificationOptions = {
        body: payload["data"]["text"],
        icon: '/static/favicon.ico'
    };
    return self.registration.showNotification(notificationTitle, notificationOptions);
});
