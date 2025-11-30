<template>
  <form @submit.prevent="alter_fav">
    <TextInput v-model:text="fav.beschreibung" label="Beschreibung" />
    <NumInput v-model:num="fav.menge" label="Menge" />
    <SelectArray
      v-model:choice="fav.einheit_id"
      :opts="units"
      display="name"
      label="Einheit"
    />
    <button type="submit" class="button-submit">speichern</button>
    <button class="button-delete" @click="delete_fav">löschen</button>
  </form>
</template>

<script>
import TextInput from "../input/TextInput.vue";
import NumInput from "../input/NumInput.vue";
import SelectArray from "../input/SelectArray.vue";
import axios from "axios";
import { inject } from "vue";

export default {
  inject: ["fetchUnits", "user", "updateFavorites"],
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
      this.updateFavorites();
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
      this.updateFavorites();
    },
  },
  data() {
    return { units: [], fav_unit: {} };
  },
  async mounted() {
    try {
      this.units = await this.fetchUnits();

      const url = "http://141.56.137.83:8000/einheiten/" + this.fav.einheit_id;
      const response = await axios.get(url);
      this.fav_unit = response.data.id;
    } catch (error) {
      console.log(error);
      return;
    }
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
