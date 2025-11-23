<template>
  <header>
    <h1>{{ user.name }}'s Einkaufslisten</h1>
    <button @click="newList" id="newlist" class="button-add">+</button>
    <button @click="$router.push('/fav')">Favorit</button>
  </header>
  <div v-if="loadingActive" class="loading">Laden...</div>
  <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
  <main>
    <ListButton
      v-for="list in lists"
      :key="list.id"
      :id="list.id"
      :name="list.name"
    />
  </main>
  <!--<footer>
    <button class=button-submit @click="$router.push('/settings')">
      Zu den Profileinstellungen
    </button>
  </footer>-->
  <BottomBar>
    <template #left>
      <button class="bottom-btn" @click="$router.push('/listen')">
        <span class="icon">📋</span>
        Listen
      </button>
    </template>

    <template #middle>
      <button class="bottom-btn" @click="$router.push('/archiv')">
        <span class="icon">📁</span>
        Archiv
      </button>

      <button class="bottom-btn" @click="$router.push('/favoriten')">
        <span class="icon">⭐</span>
        Favoriten
      </button>
    </template>

    <template #right>
      <button class="bottom-btn" @click="$router.push('/settings')">
        <span class="icon">⚙️</span>
        Einstellungen
      </button>
    </template>
  </BottomBar>
</template>

<script>
import ListButton from "./ListButton.vue";
import { inject, ref } from "vue";
import axios from "axios";
import BottomBar from "./BottomBar.vue";

export default {
  data() {
    // momentanen Nutzer holen
    const user = inject("user");

    return { lists: [], user, errorMessage: "", loadingActive: true };
  },
  methods: {
    // Nutzer möchte neue Liste erstellen
    newList() {
      this.$router.push("/neueliste");
    },
  },
  components: {
    ListButton,
    BottomBar,
  },
  async mounted() {
    // Listen des momentanen Nutzers holen
    const user = inject("user");
    const user_id = user.value.id;
    try {
    const response = await axios.get(
      `http://141.56.137.83:8000/nutzer/${user_id}/listen`,
    );
    this.lists = response.data;
    } catch (error) {
      if (
        error.response &&
        error.response.data &&
        error.response.data.detail
      ) {
        this.errorMessage = error.response.data.detail;
      } else {
        this.errorMessage = "Fehler beim Laden der Listen";
      }

    }
    this.loadingActive = false;
  },
};
</script>

<style scoped>

.error{
  width: 300px;
}
</style>
