<template>
  <form @submit.prevent="addFavorite">
    <TextInput v-model:text="favName" placeholder="Banane" label="Name" />
    <TextInput
      v-model:text="favDesc"
      placeholder="leicht unreif"
      label="Beschreibung"
    />
    <NumInput v-model:num.number="favAmount" label="Menge" />
    <SelectObjectArray
      v-model:choice="favUnit"
      :options="units"
      displayKey="name"
      valueKey="id"
      label="Einheit"
    />
    <button type="submit" class="form-element button-submit">Hinzufügen</button>
  </form>

  <!-- Fehler Meldungen -->
  <div v-if="errMsg" class="error">{{ errMsg }}</div>
</template>

<script>
import { inject } from "vue";
import axios from "axios";
import TextInput from "../input/TextInput.vue";
import NumInput from "../input/NumInput.vue";
import SelectObjectArray from "../input/SelectObjectArray.vue";

export default {
  inject: ["user", "fetchUnits", "updateFavorites"],
  components: {
    TextInput,
    NumInput,
    SelectObjectArray,
  },
  data() {
    return {
      units: [],
      errMsg: "",
      favName: "",
      favDesc: "",
      favUnit: null,
      favAmount: null,
    };
  },
  async mounted() {
    this.units = await this.fetchUnits();
  },
  methods: {
    resetInput() {
      this.favName = "";
      this.favDesc = "";
      this.favUnit = null;
      this.favAmount = 0;
    },
    async addFavorite() {
      let response;
      let url;

      let id;
      const name = this.favName.trim();
      const amount = this.favAmount;
      const unit = this.favUnit;
      const desc = this.favDesc.trim();

      // Bezugsprodukt finden/erstellen
      try {
        url =
          "http://141.56.137.83:8000/produkte/by-name/" +
          encodeURIComponent(name);
        response = await axios.get(url);
        id = response.data.id;
      } catch (error) {
        // es gibt kein Bezugsprodukt
        if (error.response && error.response.status === 404) {
          try {
            url = "http://141.56.137.83:8000/produkte_create";
            response = await axios.post(url, { name: name });
            id = response.data.id;
          } catch {
            this.errMsg =
              "Anlegen eines Bezugprodukts für eine Favoriten ist fehlgeschlagen.";
            return;
          }
        }
      }
      // Favoriten vorbereiten
      const fav = {
        produkt_id: id,
        menge: amount,
        einheit_id: unit,
        beschreibung: desc,
      };
      // Favoriten erstellen
      try {
        url =
          "http://141.56.137.83:8000/fav_produkte_create/nutzer/" +
          this.user.id;
        await axios.post(url, fav);
      } catch {
        this.errMsg = "Fehler beim erstellen des Favoriten.";
      }
      // Clean Up
      this.updateFavorites();
      this.resetInput();
    },
  },
};
</script>

<style scoped>
button {
  width: 100%;
}

form {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.25rem;
}
</style>
