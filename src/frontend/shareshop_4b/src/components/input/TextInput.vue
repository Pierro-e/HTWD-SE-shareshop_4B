<template>
  <label>
    {{ label }}
    <input
      type="text"
      :value="text"
      :placeholder="placeholder"
      maxlength="30"
      @input="$emit('update:text', $event.target.value)"
    />
  </label>
</template>
<script>
/**
 * Ein Input Feld, was textliche Werte akzeptiert.
 * @component
 */
export default {
  props: {
    /**
     * Der aktueller Wert, den das Element beinhaltet.
     * @prop {String}
     */
    text: { type: String },
    /**
     * Der Text, welcher als Placeholder dient.
     * @prop {String}
     */
    placeholder: { type: String },
    /**
     * Das Label, welches das Input Feld auszeichnen soll.
     * @prop {String}
     */
    label: { type: String },
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

input {
  margin-top: 0.5rem;
}
</style>
