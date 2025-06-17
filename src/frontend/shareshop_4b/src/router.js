import { createRouter, createWebHistory } from 'vue-router'
import Login from './components/Login.vue'
import ProjektEinführung from './components/ProjektEinführung.vue'
import CreateAccount from './components/CreateAccount.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/einfuehrung', component: ProjektEinführung },
  { path: '/registrieren', component: CreateAccount }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router