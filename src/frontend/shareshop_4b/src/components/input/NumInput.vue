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
 * @component
 */
export default {
  props: {
    /**
     * Der aktueller Wert, den das Element beinhaltet.
     * @prop {Number}
     */
    num: { type: Number },
    /**
     * Die Schrittweite, welche akzeptierten Eingabe voneinander trennt.
     * @prop {Number}
     * @default 0.25
     */
    step: { type: Number, default: 0.25 },
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
