<template>
  <header>
    <div>
      <slot name="left"></slot>
    </div>
    <div>
      <h2>{{ title }}</h2>
    </div>
    <div>
      <slot name="right"></slot>
    </div>
  </header>
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

<style scoped>
/* Header für Listen und Einkauf */
header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 10%;
  background-color: var(--accent-header-bg-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 5px var(--box-shadow-color);
}

header h2 {
  font-weight: 600;
  font-size: 1.3rem;
  text-align: center;
}

/* nur ein Slot wird genutzt -> grobes Layout */
div {
  width: 33%;
}
</style>
