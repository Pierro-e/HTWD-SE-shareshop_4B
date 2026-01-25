<template>
  <label>
    {{ label }}
    <select :value="choice" @change="onChange">
      <option disabled value="">Keine Angabe</option>
      <option
        v-for="(option, index) in options"
        :key="index"
        :value="option[valueKey]"
      >
        {{ option[displayKey] }}
      </option>
    </select>
  </label>
</template>

<script>
/**
 * Ein Input-Select Feld, was die Auswahl zwischen definierten Möglichkeiten gibt.
 * @vue-prop {Array} options - Die Möglichkeiten, zwischen denen ausgewählt werden kann.
 * @vue-prop {String} displayKey - Die Eigenschaft, die dem Nutzer als Identifizierung der Möglichkeiten gezeigt wrid.
 * @vue-prop {String} valueKey - Die Eigenschaft, die als Wert der Möglichkeiten betrachtet wrid.
 * @vue-prop {Object} choice - Die Möglichkeit, die ausgewählt ist.
 * @vue-prop {String} label - Das Label, welches das Feld auszeichnen soll.
 */
export default {
  name: "SelectArray",
  emits: ["update:choice"],
  props: {
    options: { type: Array, required: true },
    displayKey: { type: String, required: true },
    valueKey: { type: String, require: true },
    choice: { required: true },
    label: { type: String },
  },
  data() {
    return { local_choice: "" };
  },
  methods: {
    /**
     * Event Handler, der aufgerufen wird, wenn eine neue Möglichkeit ausgewählt wurde.
     * @param event {event} Event-Objekt
     */
    onChange(event) {
      const newValue = event.target.value;
      this.$emit("update:choice", newValue);
    },
  },
};
</script>

<style scoped>
label {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 1.25rem;
}

select {
  margin-top: 0.5rem;
}
</style>
