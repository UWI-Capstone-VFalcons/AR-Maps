<template>
  <div id="home">
    <Test/>
    <div class="top">
      <img src="../assets/images/illustrations/navigate.svg">
    </div>
    <div class="bottom">
      <h1>Turn on your location</h1>
      <p>Get simple, user-friendly and interactive directions <br>
       with the use of Augmented Reality.</p>
      <div class="btn-holder">
        <button type="button" class="btn btn-primary"
        @click="toMaps"
        >Find my destination</button> 
      </div>

    </div>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import router from '@/router';
import Test from '@/components/Test.vue';


export default {
  name: 'Home',
  components: {
     Test,
  },

  methods:{
    toMaps: function(){
      router.push({ name: 'Map'});

    },
  },
}
</script>
