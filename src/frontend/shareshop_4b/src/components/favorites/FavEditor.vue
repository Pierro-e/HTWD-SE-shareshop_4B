<template>
  <form @submit.prevent="alter_fav">
    <TextInput v-model:text="fav_copy.beschreibung" label="Beschreibung" />
    <NumInput v-model:num="fav_copy.menge" label="Menge" />
    <SelectObjectArray
      v-model:choice="fav_copy.einheit_id"
      :options="units"
      displayKey="name"
      valueKey="id"
      label="Einheit"
    />
    <button type="submit" class="button-submit">speichern</button>
    <button type="button" class="button-delete" @click="delete_fav">
      löschen
    </button>
  </form>
</template>

<script>
import TextInput from "../input/TextInput.vue";
import NumInput from "../input/NumInput.vue";
import SelectObjectArray from "../input/SelectObjectArray.vue";
import axios from "axios";

/**
 * Oberflächen zum Bearbeiten eines bereits angelegten Favoriten.
 * @component
 */
export default {
  inject: ["fetchUnits", "user", "updateFavorites"],
  components: {
    TextInput,
    NumInput,
    SelectObjectArray,
  },
  /**
   * Favorit, der bearbeitet werden soll.
   * @prop {Object}
   * @required
   */
  props: {
    fav: { type: Object, required: true },
  },
  /**
   * Aktuallisiert den bearbeiteten Favoriten.
   * @method alter_fav
   */
  methods: {
    async alter_fav() {
      const url =
        "http://141.56.137.83:8000/fav_produkte_update/nutzer/" +
        this.user.id +
        "/produkt/" +
        this.fav.produkt_id;

      const response = await axios.put(url, this.fav_copy);

      this.$parent.$emit("close");
      this.$parent.$emit("update");
    },
    /**
     * Löscht den Favoriten.
     * @method delete_fav
     */
    async delete_fav() {
      const url =
        "http://141.56.137.83:8000/fav_produkte_delete/nutzer/" +
        this.user.id +
        "/produkt/" +
        this.fav.produkt_id;
      const response = await axios.delete(url);

      this.$parent.$emit("close"); // Popup schließen
      this.$parent.$emit("update"); // Fav updaten
    },
  },
  data() {
    return {
      units: [],
      fav_copy: {},
    };
  },
  async mounted() {
    this.fav_copy = { ...this.fav }; // Arbeitskopie
    try {
      this.units = await this.fetchUnits();
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
