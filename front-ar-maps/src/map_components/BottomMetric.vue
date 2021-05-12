<template>
    <div id="tab">
        <h1>{{distance}}</h1>
        <h1>{{time}}</h1>
        <h1>{{destination}}</h1>
    </div>
</template>

<script>
export default {
    name: 'BottomMetric',
    props:{
        distance: Number,
        time: Number,
        destination: String
    }, 
}
</script>
<style scoped>
#tab{
    height: auto;
    background-color: aquamarine;
}
</style>