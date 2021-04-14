<template>
  <div> 

    <h1>Google Maps Demo</h1>
    <button @click="drawMarkers" style="width:100px;height: 50px;margin-bottom: 10px;margin-right: 5px;">
      Draw Markers
    </button>

    <button @click="drawDirection" style="width:100px;height: 50px;margin-bottom: 10px;margin-right: 5px;">
      Draw Direction
    </button>

    <button @click="clearMap" style="width:100px;height: 50px;margin-bottom: 10px">
      Clear Map
    </button>

    <GmapMap
  :center="centre"
  :zoom="17"
  map-type-id="terrain"
  style="width: 1000px; height: 600px"
>
  <GmapMarker
    :key="index"
    v-for="(m, index) in markers"
    :position="m.position"
    :clickable="true"
    :draggable="true"
    @click="center=m.position"
  />

  <gmap-polygon :paths="paths" >  
  </gmap-polygon>
</GmapMap>
 
  </div>
</template>

<script>

const slt1 = {lat:18.005197, lng:76.749908}
const slt2 = {lat:18.005242, lng:76.749795}
const uwi = {lat:18.006013, lng:76.747103}
export default {
  name: 'GoogleMap',
  data(){
    return{
      markers:[],
      centre:uwi,
      paths:[],
    }
  },
  methods:{
    drawMarkers(){
      this.markers = [
        {
          position:slt1,
        },
        {
          position:slt2,
        },
      ];
    },
    drawDirection(){
      this.paths=[slt1,slt2];
    },
    clearMap(){
      this.paths = [];
      this.markers = [];
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
