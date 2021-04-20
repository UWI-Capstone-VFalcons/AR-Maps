<template>
    <div>    
        <Test/>
        <GoogleMap />
    </div>
</template>

<script>
import Test from '@/components/Test.vue';
import GoogleMap from '@/components/GoogleMap.vue'

export default {
    name: 'OverheadMap',
    components: {
        Test,
        GoogleMap,
    }    
}
</script>