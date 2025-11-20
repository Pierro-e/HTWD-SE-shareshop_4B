<template>
  <div class="list-archive">
    <AppHeader :title="`Einkaufsarchiv für\n${user.name}`">
      <template #left>
        <button @click="back_to_listOverview()" class="button button-cancel back-button">
          Zurück
        </button>
      </template>
    </AppHeader>

    <div v-if="loadingActive" class="loading">Laden...</div>
    <div v-else-if="errorMessage" class="error">{{ errorMessage }}</div>

    <div v-else-if="purchases.length === 0" class="info">
      Es sind noch keine Einkäufe vorhanden.
    </div>

    <div v-else>
      <ListButton
        v-for="purchase in purchases"
        :key="purchase.einkauf_id"
        :item="purchase"
        :name="`Einkauf vom ${formatDate(purchase.eingekauft_am)}`"
      />
    </div>
  </div>
</template>

<script>
import axios from "axios";
import AppHeader from "./AppHeader.vue";
import ListButton from "./ListButton.vue";
export default {
  name: "userArchive",
  inject: ["user"],
  components: {AppHeader, ListButton},

  data(){
      return{
          list_name: "",
          purchases: [],
          loadingActive: true,
          errorMessage: "",
      };
  },
  methods: {
    async getData(id) {
      try {   
        const response = await axios.get(`http://141.56.137.83:8000/einkaufsarchiv/nutzer_alle/${this.user.id}`);
        
        this.purchases = response.data;

        console.log(this.purchases);
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || "Fehler beim Laden der Daten";
      } finally {
        this.loadingActive = false;
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return "";
      const date = new Date(dateStr);
      return date.toLocaleDateString("de-DE");  // aus "JJJJ-MM-TT" wird "TT.MM.JJJJ"
    },
    back_to_listOverview() {
      this.$router.push(`/listen`);
    },
  },
  mounted() {
    this.getData(this.user.id);
  },
};
</script>

<style scoped>
</style>
