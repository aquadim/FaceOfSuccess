<script setup>
</script>

<template>
  <main class="app w3-light-grey">
    <router-view></router-view>
    <DialogsWrapper />
  </main>
</template>

<style scoped>
.app {
  width: 100vw;
  height: 100vh;
  top: 0;
  left: 0;
  position: absolute;
}
</style>
