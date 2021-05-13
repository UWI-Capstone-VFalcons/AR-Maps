<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
};
</script>
<style>
#app{
    height: 100%;
    width: 100%;
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    overflow:hidden;
    position: absolute;
    top: 0;
    z-index: 1;
    background-color: whitesmoke;
}
</style>