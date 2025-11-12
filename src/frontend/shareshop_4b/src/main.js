import './style.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router.js'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons'
library.add(faEye, faEyeSlash)

const app = createApp(App);
app.component('font-awesome-icon', FontAwesomeIcon)
app.use(router)
app.mount('#app')