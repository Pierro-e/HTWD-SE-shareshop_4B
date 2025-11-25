<template>
  <AppHeader title="Listen">
    <template v-slot:right>
      <button @click="newList" id="newlist" class="button-add">+</button>
    </template>
  </AppHeader>

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
  <footer>
    <button @click="$router.push('/fav')">Favorit</button>
    <button class="button-submit" @click="$router.push('/settings')">
      Zu den Profileinstellungen
    </button>
  </footer>
</template>

<script>
import ListButton from "./ListButton.vue";
import AppHeader from "./AppHeader.vue";
import { inject, ref } from "vue";
import axios from "axios";

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
    AppHeader,
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
      if (error.response && error.response.data && error.response.data.detail) {
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
.error {
  width: 300px;
}
</style>
