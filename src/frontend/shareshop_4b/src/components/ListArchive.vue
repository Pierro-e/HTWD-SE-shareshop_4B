<template>
  <div class="list-archive">

    <AppHeader :title="`Listenarchiv für\n${list_name}`" class="multiline-title">
      <template #left>
        <button @click="back_to_list" class="button button-cancel back-button">
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
        :name="`Einkauf am ${formatDate(purchase.eingekauft_am)}`"
      />
    </div>

  </div>
</template>

<script>
import axios from "axios";
import AppHeader from "./AppHeader.vue";
import ListButton from "./ListButton.vue";
export default {
  name: "ListArchive",
  props: ["list_id"],
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
        const [listResponse, purchasesResponse] = await Promise.all([
          axios.get(`http://141.56.137.83:8000/listen/by-id/${id}`),
          axios.get(`http://141.56.137.83:8000/einkaufsarchiv/list/${id}`)
        ]);

        this.list_name = listResponse.data.name;
        this.purchases = purchasesResponse.data;

      } catch (error) {
        this.errorMessage = error.response?.data?.detail || "Fehler beim Laden der Daten";
      } finally {
        this.loadingActive = false;
      }
    },
    
    back_to_list() {
        const list_id = this.list_id || this.$route.params.listenId;
        this.$router.push(`/list/${list_id}`);
    },

    formatDate(dateStr) {
    if (!dateStr) return "";
    const date = new Date(dateStr);
    return date.toLocaleDateString("de-DE");
    },
  },
  mounted() {
    const id = this.list_id || this.$route.params.listenId;
    this.getData(id);
  },





};
</script>

<style>
.multiline-title h2 {
    white-space: pre-line;
}
</style>
