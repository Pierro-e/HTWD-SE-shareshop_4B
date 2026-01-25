<template>
  <label>
    {{ label }}
    <input
      type="number"
      :value="num"
      :step="step"
      min="0"
      placeholder="0"
      @input="$emit('update:num', $event.target.value)"
    />
  </label>
</template>

<script>
/**
 * Ein Input Feld, was nummerische Werte akzeptiert.
 * @vue-prop {Number} num - Der aktueller Wert, den das Element beinhaltet.
 * @vue-prop {Number} step - Die Schrittweite, welche akzeptierten Eingabe voneinander trennt.
 * @vue-prop {String} label - Das Label, welches das Input Feld auszeichnen soll.
 */
export default {
  props: {
    num: { type: Number },
    step: { type: Number, default: 0.25 },
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
