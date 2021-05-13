<template>
    <div id="arview-main">
        <base-top-bar 
            title="AR Map"
            :back_enable="true">
        </base-top-bar>
        <ARView/>
        <base-bottom-bar></base-bottom-bar>
    </div>
</template>

<script>
import BaseTopBar from '@/components/BaseTopBar';
import BaseBottomBar from '@/components/BaseBottomBar';
import ARView from '@/components/ARView.vue';
export default {
    name: 'ARGuide',
    components: {
        'base-top-bar':BaseTopBar,
        'base-bottom-bar':BaseBottomBar,
        ARView
    },
    methods: {
    } 
}
</script>
<style scoped>
#arview-main{
    height: 100%;
    width: 100%;
}
</style>