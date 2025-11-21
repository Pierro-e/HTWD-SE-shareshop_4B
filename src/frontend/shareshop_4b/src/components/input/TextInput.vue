<template>
  <input
    type="text"
    :value="text"
    :placeholder="placeholder"
    maxlength="30"
    @input="$emit('update:text', $event.target.value)"
  />
</template>
<script>
export default {
  props: {
    text: { type: String },
    placeholder: {type: String},
  },
};
</script>

<style scoped></style>
