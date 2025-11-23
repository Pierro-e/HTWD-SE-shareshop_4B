<template>
  <div class="header">
    <!--Slots für die unterschiedlichen Buttons in Einkauf und List-->
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
