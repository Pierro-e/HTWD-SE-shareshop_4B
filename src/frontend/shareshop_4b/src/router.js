import { createRouter, createWebHistory } from "vue-router";
import Login from "./components/Login.vue";
import ProjektEinführung from "./components/ProjektEinführung.vue";
import CreateAccount from "./components/CreateAccount.vue";
import ListOverview from "./components/ListOverview.vue";
import ListCreator from "./components/ListCreator.vue";
import List from "./components/List.vue";
import UserSettings from "./components/UserSettings.vue";
import ProductDetail from "./components/ProductDetail.vue";
import Einkauf from "./components/Einkauf.vue";
import Favorites from "./components/Favorites.vue"
import ListArchive from "./components/ListArchive.vue";
import ProductArchive from "./components/ProductArchive.vue";

const routes = [
  { path: "/", component: Login },
  { path: "/einfuehrung", component: ProjektEinführung },
  { path: "/registrieren", component: CreateAccount },
  { path: "/settings", component: UserSettings },
  { path: "/listen", component: ListOverview },
  { path: "/neueliste/", component: ListCreator },
  { path: "/list/:id", component: List, props: true },
  { path: "/fav", component: Favorites },
  {
    path: "/listen/:listenId/produkte/:produktId/nutzer/:nutzerId",
    component: ProductDetail,
    props: true,
  },
  { path: "/list/:listenId/einkauf", component: Einkauf, props: true },
  { path: "/list/:list_id/archive", component: ListArchive, props: true },
  { path: "/product/archive/:purchase_id", component: ProductArchive, props: true },
];
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
