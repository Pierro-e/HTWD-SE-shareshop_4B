import 'vue-select/dist/vue-select.css'
import './style.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router.js'
import vSelect from 'vue-select'

const app = createApp(App)
app.component('v-select', vSelect)
app.use(router)
app.mount('#app')