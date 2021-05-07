<template>
    <div id="arguide"> 
        <h2>If you are seeing this message, please contact the website admin</h2> 
    </div>
</template>

<script>

export default {
    name: 'ARView',
    Components: {        
    },
    
    props: {

    },
    
    data() {
        return {};
    },
    
    methods:{
        
    },

    watch: {
        
    },

    created(){
        
    },
    
    mounted() {  
        window.location.replace(this.$host+'nav');
    },

}
</script>