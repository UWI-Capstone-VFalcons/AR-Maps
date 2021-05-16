<template>
  <div id="home-view">
     <base-top-bar
        title="Frequently Asked Questions"
        title_img_src="images/illustrations/help.png"
        :title_img_enable="true"
        :back_enable="true"
     ></base-top-bar>

    <div id="content">
        <help-section/>
    </div>

    <base-bottom-bar>
    </base-bottom-bar>
  </div>
</template>
<script>
// @ is an alias to /src
import BaseTopBar from '@/components/BaseTopBar';
import BaseBottomBar from '@/components/BaseBottomBar';
import Help_Section from '@/components/Help.vue';


export default {
  name: 'Home',
  components: {
    'base-top-bar':BaseTopBar,
    'base-bottom-bar':BaseBottomBar,
    'help-section': Help_Section,
  },
}
</script>
<style scoped>
#content{
  height: 100%;
  width: 100%;
  padding: 7rem 0.5rem;
  padding-bottom: 7rem;
  display: flex;
  flex-flow: column;
  display: block;
  position: absolute;
}
@media (max-width: 480px) {
  #content{
    padding-top: 6rem;
    padding-bottom: 5rem;
  }
}
</style>