<template>
    <div id="qrview-main">
        <QRScanner/>
    </div>    
</template>

<script>
import QRScanner from '@/components/QRScanner.vue';
export default {
    name: 'Scanner',
    components:{
        QRScanner
    },
    methods: {
  }
}
</script>