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
  { path: "/list/:id", component: List, props: true, name: "List" },
  { path: "/fav", component: Favorites },
  {
    path: "/detail/:id/produkte/:produktId/nutzer/:nutzerId",  // id ist hier entweder die list_id oder die purchase_id --- nur noch "detail" in der Route, da es sowohl für Listenprodukte als auch für Archivprodukte genutzt wird
    component: ProductDetail,
    props: route => ({
      id: route.params.id,
      produktId: route.params.produktId,
      nutzerId: route.params.nutzerId,
      readonly: route.query.readonly === 'true' // wird in query gesetzt
    }),
    name: "ProductDetail",
  },
  { path: "/list/:listenId/einkauf", component: Einkauf, props: true },
  { path: "/list/:list_id/archive", component: ListArchive, props: true },
  { path: "/product/archive/:purchase_id", 
    component: ProductArchive, 
    props: route => ({
      purchase_id: route.params.purchase_id,
      list_id: route.params.list_id,
      purchase_name: route.params.purchase_name
    }), 
    name: "ProductArchive" 
  },
];
const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
