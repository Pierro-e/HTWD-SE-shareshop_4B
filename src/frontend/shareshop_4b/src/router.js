import { createRouter, createWebHistory } from "vue-router";
import Login from "./components/Login.vue";
import ProjektEinführung from "./components/ProjektEinführung.vue";
import CreateAccount from "./components/CreateAccount.vue";
import ListOverview from "./components/ListOverview.vue";
import ListCreator from "./components/ListCreator.vue";
import List from "./components/List.vue";
import UserSettings from './components/UserSettings.vue';
import ProductDetail from './components/ProductDetail.vue';

const routes = [
  { path: "/", component: Login },
  { path: "/einfuehrung", component: ProjektEinführung },
  { path: "/registrieren", component: CreateAccount },
  { path: '/settings', component: UserSettings },
  { path: "/listen", component: ListOverview },
  { path: "/neueliste/", component: ListCreator },
  {path: "/list/:id", component: List, props: true },
  { path: "/listen/:listenId/produkte/:produktId/nutzer/:nutzerId", component: ProductDetail, props: true },
];
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
