import 'vue-select/dist/vue-select.css'
import './style.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router.js'

import vSelect from 'vue-select'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faEye, faEyeSlash, faArrowLeft, faPlus, faXmark, faCheck, faCircleInfo, faCartShopping, faBoxArchive, faGear, faList, faStar, faPen } from '@fortawesome/free-solid-svg-icons'
library.add(faEye, faEyeSlash, faArrowLeft, faPlus, faXmark, faCheck, faCircleInfo, faCartShopping, faBoxArchive , faStar, faList, faGear, faPen)

const app = createApp(App);
app.component('v-select', vSelect)
app.component('font-awesome-icon', FontAwesomeIcon)
app.use(router)
app.mount('#app')