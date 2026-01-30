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
 *
 * @vue-prop {String} text - Der aktueller Wert, den das Element beinhaltet.
 * @vue-prop {String} placeholder - Der Text, welcher als Placeholder dient.
 * @vue-prop {String} label - Das Label, welches das Input Feld auszeichnen soll.
 */
export default {
  props: {
    text: { type: String },
    placeholder: { type: String },
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
