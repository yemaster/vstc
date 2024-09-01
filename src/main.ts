import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHashHistory } from 'vue-router'

// Naive Fonts
import 'vfonts/Lato.css'
import 'vfonts/FiraCode.css'

// Basic Styles
import './style.css'

// Router
const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        { path: '/', name: 'Index', component: () => import("./pages/IndexView.vue") },
        { path: '/t/:id', name: 'Test', component: () => import("./pages/TestView.vue") },
        { path: '/update-logs', name: 'Update Logs', component: () => import("./pages/UpdateLog.vue") },
        { path: '/notfound', name: 'Not Found', component: () => import("./pages/NotFound.vue") },
    ]
})

createApp(App)
    .use(router)
    .mount('#app')
