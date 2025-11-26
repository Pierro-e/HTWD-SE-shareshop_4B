<template>
  <div class="list-archive">
    <AppHeader title="Einkaufsarchiv">
      <template #left>
        <button @click="back_to_list" class="button-cancel back-button">
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
      <div class=card-list>
        <ListButton
          v-for="purchase in purchases"
          :key="purchase.einkauf_id"
          :item="purchase"
          :name="`Einkauf vom ${formatDate(purchase.eingekauft_am)}`"
        />
      </div>
    </div>

  </div>
  <BottomBar />
</template>

<script>
import axios from "axios";
import AppHeader from "./AppHeader.vue";
import ListButton from "./ListButton.vue";
import BottomBar from "./BottomBar.vue";

export default {
  name: "ListArchive",
  props: ["list_id", "list_name"],
  components: {
    AppHeader,
    ListButton,
    BottomBar
},

  data(){
      return{
          listName: "",
          purchases: [],
          loadingActive: true,
          errorMessage: "",
      };
  },

  methods: {
    async getData(id) {
      try {
        const response = await axios.get(`http://141.56.137.83:8000/einkaufsarchiv/list/${id}`);

        if (response.data.length === 0) {
          this.purchases = [];
          return;
        }
        this.purchases = response.data;

        if (this.listName === undefined && this.purchases.length > 0 || this.listName === "") {
          this.listName = this.purchases[0].listen_name;
        }

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
    return date.toLocaleDateString("de-DE");  // aus "JJJJ-MM-TT" wird "TT.MM.JJJJ"
    },
  },
  mounted() {
    this.listName = this.list_name || this.$route.params.list_name;
    const id = this.list_id || this.$route.params.listenId;
    this.getData(id);
  },
};
</script>

