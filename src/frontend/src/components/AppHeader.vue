<template>
  <div class="header">
    <!--Slots für die unterschiedlichen Buttons in Einkauf und List-->
    <div class="button-left">
      <slot name="left"></slot>
    </div>

    <h2>{{ title }}</h2>

    <div class="button-right">
      <slot name="right"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "AppHeader",
  props: {
    title: {
      type: String,
      required: true,
    },
  },
};
</script>

<style>
/* Header für Listen und Einkauf */
.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 70px; /* vorher 60px */
  background-color: var(--accent-header-bg-color);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px var(--box-shadow-color);
}

/* h2 mittig im Header */
.header h2 {
  width: 50%;
  margin: 0;
  font-weight: 600;
  font-size: 1.3rem;
  color: white;
  text-align: center;
  display: -webkit-box;
  -webkit-line-clamp: 2; /* Anzahl sichtbarer Zeilen */
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-wrap: break-word;
}

/* Button links */
.button-left {
  position: absolute;
  left: 10px;
  top: 10px;
}

/* Button rechts */
.button-right {
  position: absolute;
  right: 10px;
  top: 10px;
}
</style>

