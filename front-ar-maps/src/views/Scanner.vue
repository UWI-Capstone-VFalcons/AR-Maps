<template>
    <div id="qr-view">
        <base-top-bar 
            title="QR Scanner"
            :back_enable="true">
        </base-top-bar>
        <div id="content">
            <QRScanner/>
        </div>
        <base-bottom-bar></base-bottom-bar>
    </div>    
</template>

<script>
import BaseTopBar from '@/components/BaseTopBar';
import BaseBottomBar from '@/components/BaseBottomBar';
import QRScanner from '@/components/QRScanner.vue';

export default {
    name: 'Scanner',
    components:{
        'base-top-bar':BaseTopBar,
        'base-bottom-bar':BaseBottomBar,
        QRScanner,
    },
    methods: {
  }
}
</script>
<style scoped>
#qr-view{
    height: 100%;
    width: 100%;
}
#content{
    height: 100%;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>