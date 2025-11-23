<template>
  <!-- Eingaben -->
  <TextInput v-model:text="fav_name" placeholder="Banane" />
  <TextInput v-model:text="fav_desc" placeholder="leicht unreif" />
  <NumInput v-model:num.number="fav_amount" />
  <SelectArray v-model:choice="fav_unit" :opts="units" display="name" />

  <!-- Fehler Meldungen -->
  <div v-if="errMsg" class="error">{{ errMsg }}</div>

  <!-- "Submit" Button -->
  <button @click="add_fav" class="button-submit">Hinzufügen</button>
</template>

<script>
import { inject } from "vue";
import axios from "axios";
import TextInput from "./input/TextInput.vue";
import NumInput from "./input/NumInput.vue";
import SelectArray from "./input/SelectArray.vue";

export default {
  emits: ["load_fav"],
  inject: ["user", "fetchUnits"],
  components: {
    TextInput,
    NumInput,
    SelectArray,
  },
  data() {
    return {
      units: [],
      errMsg: "",
      fav_name: "",
      fav_desc: "",
      fav_unit: {},
      fav_amount: null,
    };
  },
  async mounted() {
    this.units = await this.fetchUnits();
  },
  methods: {
    async add_fav() {
      let response;
      let url;

      let id;
      const name = this.fav_name.trim();
      const amount = this.fav_amount;
      const unit = this.fav_unit.id;
      const desc = this.fav_desc.trim();

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

      // Favoriten erstellen
      const fav = {
        produkt_id: id,
        menge: amount,
        einheit_id: unit,
        beschreibung: desc,
      };
      try {
        url = "http://141.56.137.83:8000/fav_produkte_create/nutzer/" + this.user.id;
        await axios.post(url, fav);
      } catch {
        this.errMsg = "Fehler beim erstellen des Favoriten.";
      }

      this.$emit("load_fav");
    },
  },
};
</script>

<style scoped></style>
