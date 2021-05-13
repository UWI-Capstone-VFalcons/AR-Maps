<template>
  <div id="home-view">
    <TestServer/>
     <base-top-bar></base-top-bar>

    <div id="content">
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

    <base-bottom-bar>
    </base-bottom-bar>
  </div>
</template>

<script>
// @ is an alias to /src
import BaseTopBar from '@/components/BaseTopBar';
import BaseBottomBar from '@/components/BaseBottomBar';
import router from '@/router';
import TestServer from '@/components/TestServerConnection.vue';


export default {
  name: 'Home',
  components: {
    'base-top-bar':BaseTopBar,
    'base-bottom-bar':BaseBottomBar,
     TestServer,
  },

  methods:{
    toMaps: function(){
      router.push({ name: 'Map'});

    },
  },
}
</script>
<style scoped>
#home-view{
  height: 100%;
  width: 100%;
}
#content{
  height: 100%;
  width: 100%;
  padding: 6rem 0.5rem;
  padding-bottom: 7rem;
  display: flex;
  flex-flow: column;
  display: block;
  position: relative;
}

#content .top{
    height: 30%;
}

#content .top img{
    width: 100%;
    height: 100%;
}

#content .bottom{
    height: 70%;
    width: 100%;
    padding-top: 2rem;
    overflow-y: auto;
}

#content .bottom .btn-holder{
    margin-top: 5rem;
 
}

#content .bottom .btn-holder .btn{
    padding: 0.5rem 5rem;
    border-radius: 2rem;
}
</style>
