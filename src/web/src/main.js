import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from "./routes"
import * as ConfirmDialog from 'vuejs-confirm-dialog'

createApp(App)
.use(router)
.use(ConfirmDialog)
.mount('#app')
