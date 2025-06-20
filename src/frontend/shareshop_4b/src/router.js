import { createRouter, createWebHistory } from "vue-router";
import Login from "./components/Login.vue";
import ProjektEinführung from "./components/ProjektEinführung.vue";
import CreateAccount from "./components/CreateAccount.vue";
import ListOverview from "./components/ListOverview.vue";
import ListCreator from "./components/ListCreator.vue";
import List from "./components/List.vue";

const routes = [
  { path: "/", component: Login },
  { path: "/einfuehrung", component: ProjektEinführung },
  { path: "/registrieren", component: CreateAccount },
  { path: "/listen", component: ListOverview },
  {
    path: "/neueliste/",
    component: ListCreator,
  },
  {
    component: List,
    path: "/list/:id",
    props: true,
    // TODO: Parameter für Listen übergabe, welcher eine Neue Liste aufruft zum erstellen
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
