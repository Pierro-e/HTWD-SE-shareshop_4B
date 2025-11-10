<template>
  <NumInput v-model:num.number="fav.menge" />
  <TextInput v-model:text="fav.beschreibung" />
  <SelectArray v-model:choice="fav_unit" :opts="units" display="name" />
  <button @click="alter_fav" class="button-submit">speichern</button>
  <button class="button-delete" @click="delete_fav">
    löschen
  </button>
</template>

<script>
import TextInput from "./TextInput.vue";
import NumInput from "./NumInput.vue";
import SelectArray from "./SelectArray.vue";
import axios from "axios";

export default {
  inject: ["fetchUnits", "user"],
  components: {
    TextInput,
    NumInput,
    SelectArray,
  },
  props: {
    fav: { required: true },
  },
  methods: {
    alter_fav() {
      const url =
        "http://141.56.137.83:8000/fav_produkte_update/nutzer/" +
        this.user.id +
        "/produkt/" +
        this.fav.produkt_id;
      const response = axios.put(url, this.fav);
      // TODO: schließe das PopUp
    },
    delete_fav() {
       const url =
        "http://141.56.137.83:8000/fav_produkte_delete/nutzer/" +
        this.user.id +
        "/produkt/" +
        this.fav.produkt_id;
      const response = axios.delete(url);
      // TODO: updaten der Favoriten
      // TODO: schließe das PopUp
    },
  },
  data() {
    return { units: [], fav_unit: {} };
  },
  async mounted() {
    this.units = await this.fetchUnits();
    // TODO: akutell ausgewählte Einheit anzeigen
    const url = "http://141.56.137.83:8000/einheiten/" + this.fav.einheit_id;
    const response = await axios.get(url);
    this.fav_unit = response.data;
  },
};
</script>
