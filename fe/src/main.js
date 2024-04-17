import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios';
import ToastPlugin from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-default.css';

window.axios = axios.create({
    baseURL: import.meta.env.VITE_BE_HOST,
});

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
