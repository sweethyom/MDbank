<template>
  <header class="container">
    <NavBar /> 
    <RouterView />
    <TopScroll />
  </header>
</template>

<script setup>
import { RouterView } from 'vue-router';
import NavBar from './components/common/NavBar.vue'
import TopScroll from './components/common/TopScroll.vue';


</script>

<style scoped>
.container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}
</style>