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
 * @component
 */
export default {
  name: "SelectArray",
  /**
   * @emits {Object} update:choice - Sendet ausgewählte Möglichkeit.
   */
  emits: ["update:choice"],
  props: {
    /**
     * Die Möglichkeiten, zwischen denen ausgewählt werden kann.
     * @prop {Array}
     * @required
     */
    options: { type: Array, required: true },
    /**
     * Die Eigenschaft, die dem Nutzer als Identifizierung der Möglichkeiten gezeigt wrid.
     * @prop {String}
     * @required
     */
    displayKey: { type: String, required: true },
    /**
     * Die Eigenschaft, die als Wert der Möglichkeiten betrachtet wrid.
     * @prop {String}
     * @required
     */
    valueKey: { type: String, require: true },
    /**
     * Die Möglichkeit, die ausgewählt ist.
     * @required
     */
    choice: { required: true },
    /**
     * Das Label, welches das Feld auszeichnen soll.
     * @prop {String}
     */
    label: { type: String },
  },
  data() {
    return { local_choice: "" };
  },
  methods: {
    /**
     * Event Handler, der aufgerufen wird, wenn eine neue Möglichkeit ausgewählt wurde.
     * @method
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
