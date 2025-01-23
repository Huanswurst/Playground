<template>
  <div id="app">
    <router-view />
    <AppFooter />
  </div>
</template>

<script setup>
import AppFooter from './components/Footer.vue'
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
