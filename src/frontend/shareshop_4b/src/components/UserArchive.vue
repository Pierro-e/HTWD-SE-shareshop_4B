<template>
  <div class="list-archive">
    <AppHeader :title="`Einkaufsarchiv für\n${user.name}`">
      <template #left>
        <button @click="back_to_listOverview()" class="button button-cancel back-button">
          <font-awesome-icon icon='arrow-left'/>
        </button>
      </template>
    </AppHeader>

    <div v-if="loadingActive" class="loading">Laden...</div>
    <div v-else-if="errorMessage" class="error">{{ errorMessage }}</div>

    <div v-else-if="purchases.length === 0" class="info">
      Keine Einkäufe
    </div>

    <div v-else>
      <div class="card-list">
        <ListButton
          v-for="purchase in purchases"
          :key="purchase.einkauf_id"
          :item="purchase"
          :name="`${purchase.listen_name} - ${formatDate(purchase.eingekauft_am)}`"
          :isUserArchive="true"
        />
      </div>
    </div>
  </div>
  <BottomBar 
    :highlight-btn="2"
  />
</template>

<script>
import axios from "axios";
import AppHeader from "./AppHeader.vue";
import ListButton from "./ListButton.vue";
import BottomBar from "./BottomBar.vue";
export default {
  name: "userArchive",
  inject: ["user"],
  components: {
    AppHeader, 
    ListButton, 
    BottomBar
  },
  data(){
      return{
          purchases: [],
          loadingActive: true,
          errorMessage: "",
      };
  },
  methods: {
    async getData(id) {
      try {   
        const response = await axios.get(`http://141.56.137.83:8000/einkaufsarchiv/nutzer_alle/${this.user.id}`);
        
        if (response.data.length === 0) {
          this.purchases = [];
          return;
        }
        this.purchases = response.data;

        console.log ("Einkaufsarchiv Daten:", this.purchases);
        
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || "Fehler beim Laden der Daten";
      } finally {
        this.loadingActive = false;
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return "";
      const date = new Date(dateStr);
      return new Intl.DateTimeFormat("de-DE", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric"
      }).format(date);  // aus "JJJJ-MM-TT" wird "TT.MM.JJJJ"
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
.card-list {
  padding-top: 60px;
}
</style>
