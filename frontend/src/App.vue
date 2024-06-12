<template>
  <div id="app">
    <NavBar />
    <router-view />
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue";
export default {
  name: "App",
  components: {
    NavBar,
  },
};
</script>

<style>
#app {
  text-align: center;
  margin-top: 20px;
}

body {
  overflow-y: auto;
  overflow-x: hidden;;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 30px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}

</style>
