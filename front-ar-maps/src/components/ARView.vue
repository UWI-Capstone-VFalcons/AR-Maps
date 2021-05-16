<template>
    <div id="arguide"> 
        <h2>Alert!</h2>
        <h5>If you are seeing this message 
            for more than 2 minutes,
            please contact the website admin. 
            You can use the map to get direction 
            while we resolve the issue. Thank you! 
        </h5> 
    </div>
</template>

<script>

export default {
    name: 'ARView',  
    mounted() {  
        window.location.replace(this.$host+'nav');
    },

}
</script>
<style scoped>
#arguide{
    height: 100%;
    width: 100%;
    display: flex;
    color: white;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    background-color: var(--main-dark-overlay-background);
}

</style>
