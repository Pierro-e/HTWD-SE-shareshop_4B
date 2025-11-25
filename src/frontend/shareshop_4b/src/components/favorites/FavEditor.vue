<template>
  <NumInput v-model:num="fav.menge" />
  <TextInput v-model:text="fav.beschreibung" />
  <SelectArray v-model:choice="fav_unit" :opts="units" display="name" />
  <button @click="alter_fav" class="button-submit">speichern</button>
  <button class="button-delete" @click="delete_fav">löschen</button>
</template>

<script>
import TextInput from "../input/TextInput.vue";
import NumInput from "../input/NumInput.vue";
import SelectArray from "../input/SelectArray.vue";
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
    async alter_fav() {
      const url =
        "http://141.56.137.83:8000/fav_produkte_update/nutzer/" +
        this.user.id +
        "/produkt/" +
        this.fav.produkt_id;
      const response = await axios.put(url, this.fav);
      // close PopUP
      this.$parent.$emit("close");
      // Favoriten aktuallisiern (improve!!!)
      this.$parent.$parent.$parent.$parent.get_favs();
    },
    async delete_fav() {
      const url =
        "http://141.56.137.83:8000/fav_produkte_delete/nutzer/" +
        this.user.id +
        "/produkt/" +
        this.fav.produkt_id;
      const response = await axios.delete(url);
      // close PopUP
      this.$parent.$emit("close");
      // Favoriten aktuallisiern (improve!!!)
      this.$parent.$parent.$parent.$parent.get_favs();
    },
  },
  data() {
    return { units: [], fav_unit: {} };
  },
  async mounted() {
    try {
      this.units = await this.fetchUnits();
    } catch (error) {
      console.log(error);
      return;
    }
    if (this.fav.einheit_id) {
      const url = "http://141.56.137.83:8000/einheiten/" + this.fav.einheit_id;
      try {
        const response = await axios.get(url);
      } catch (error) {
        console.log(error);
        return;
      }
      this.fav_unit = response.data;
    }
  },
};
</script>
