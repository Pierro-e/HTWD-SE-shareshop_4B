<template>
  <div class="header">
    <slot name="left"></slot>

    <h2>{{ title }}</h2>

    <slot name="right"></slot>
  </div>
</template>

<script>
export default {
  name: "AppHeader",
  props: {
    title: {
      type: String,
      required: true,
    }
  }
};
</script>
