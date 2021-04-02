<template>
  <div id="app">
    <!-- Top Bar -->
    <div id="app-bar" class="main_bar">
      <h2 id="v-title">{{ title }}</h2>
    </div>
    <!-- Main Contnent area -->
    <div id="main-content">
      <router-view />
    </div>
    <!-- Bottom Navigation bar -->
    <div id="bottom-nav" class="main_bar">
      <router-link to="/">
        <div class="nav-el">
          <img src="./assets/images/icons/home.svg" alt="home"/>
        </div>
      </router-link>
      <router-link to="/map">
        <div class="nav-el">
          <img src="./assets/images/icons/map-pin.svg" alt="home"/>
        </div>
      </router-link>
      <router-link to="/scan">
        <div class="nav-el">
          <img src="./assets/images/icons/qr-code.svg" alt="home"/>
        </div>
      </router-link>
        <div class="nav-el">
          <a href="http://localhost:5000/nav">
            <img src="./assets/images/icons/ar-view.svg" alt="home"/>
          </a>
        </div>
    </div>
  </div>
</template>

<script>
import EventBus from '@/event-bus';

export default {
  data() {
    return {
      title: 'UWI AR Maps'
    };
  },
  
  methods:{
    test: function(a){
      this.$title = a;
    }
  },
  
  computed: {
  },
  mounted() {
    EventBus.$on("changeTitle", data =>{
      this.title = data;
    });
  },
  watch: {
    '$route' (to, from) {
      document.title = to.meta.title || 'UWI AR Maps'
      this.title = to.meta.title
      from
    }
  },
};
</script>