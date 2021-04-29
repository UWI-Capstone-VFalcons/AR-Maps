<template>
  <div> 
        <!-- <h6>// https://www.youtube.com/watch?v=KARBEHUyooM</h6> -->
    <div id="user-location">
      <img src="../assets/images/icons/map-pin.svg">
      <h6>Location: </h6>
    </div>

    <div id="user-destination">
      <form action="">
        <label for="">Destination: </label>
        <select name="destinations" id="dd-dest">
          <option value="" disabled selected>Select Destination Here</option>
          <option value="slt-1">SLT 1</option>
          <option value="slt-2">SLT 2</option>
          <option value="slt-3">SLT 3</option>
          <option value="tech-lib">Science and Technology Library</option>
        </select>
        <button @click="findPath">Find Path</button>
      </form>
    </div>

    <div class="map-btns">
      <button @click="drawMarkers"> Draw Markers </button>

      <button @click="drawDirection"> Draw Direction </button>

      <button @click="clearMap"> Clear Map</button>
    </div>


    <GmapMap
      :center="centre"
      :zoom="17"
      style="width: 100%; height: 100vh;"
    >
      <GmapInfoWindow
      :options="infoWindow.options"
      :position="infoWindow.position"
      :opened="infoWindow.open"
      @closeclick="infoWindow.open=false"
      >
      <div v-html="infoWindow.template"></div>
      </GmapInfoWindow>

      <GmapMarker
        :key="index"
        v-for="(m, index) in markers"
        :position="m.position"
        :title="m.title"
        :label="m.label"
        :icon="m.markerIcon"
        :animation="m.animation"
        :clickable="true"
        :draggable="false"
        @click="openInfoWindowTemplate(index)"
      />

      <gmap-polygon :paths="paths" >  
      </gmap-polygon>
    </GmapMap>

  </div>
</template>

<script>
import axios from 'axios';

const slt1 = {lat:18.005197, lng:-76.749908}
const slt2 = {lat:18.005242, lng:-76.749795}
const uwi = {lat:18.00619408233222, lng:-76.74683600360201}

export default {
  name: 'GoogleMap',
  data(){
    return{
      // Google map variables
      markers:[],
      paths:[],
      infoWindow:{
        options: {
          maxWidth: 300,
          pixelOffset: { width: 0, height: -35 }
        },
        position:{lat:0, lng:0},
        open:false,
        template:'',
      },
      centre:uwi,
      myCoordinates:{
        lat:0,
        lng:0
      },
      // database cached variables
      all_buildings:[],
      all_paths:[],
    }
  },
  created(){
    //get users coordinated from browser request
    this.$getLocation({}) //Prompts the user to reveal the location to our app
      .then(coordinates => {
        // console.log(coordinates);
        this.myCoordinates = coordinates;
      })
        .catch(error => alert(error));
    
    // add all the buildings when the map is creatred
    this.addAllBuildiings();
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

    findPath(){  

    },
    
    addAllBuildiings(){
      const path = this.$host+'api/destinations';
      axios.get(path)
        .then((res) => {
          this.all_buildings = res.data.data;

          // run a loop on the json list and create a
          // marker for each building
          if(this.all_buildings.length > 0){
            for(var i = 0; i < this.all_buildings.length; i ++){
              this.markers.push({
                position: {lat:this.all_buildings[i].building_latittude , lng:this.all_buildings[i].building_longitude},
                title: this.all_buildings[i].building_name,
                label:{
                  text: this.all_buildings[i].building_name,
                  color: "#2270C4",
                  fontSize: "12px",
                }, 
                markerIcon: {
                  url: require('../assets/images/icons/map/building.png'),
                  // size: {width: 60, height: 90, f: 'px', b: 'px',},
                  scaledSize: {width: 30, height: 30, f: 'px', b: 'px',},
                  // labelOrigin: {lat:this.all_buildings[i].building_latittude , lng:this.all_buildings[i].building_longitude},
                  // labelOrigin: {x:this.all_buildings[i].building_latittude-0.001, y:this.all_buildings[i].building_longitude-0.001},
                  labelOrigin: {x:75, y:35},

                },
                animation: 0
              })
            }
          }

        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    openInfoWindowTemplate(index) {
      const building = this.all_buildings[index];
      this.infoWindow.position = { lat: building.building_latittude, lng: building.building_longitude }
      this.infoWindow.template = `<b>${building.building_name}</b><br>${building.building_address1}<br>${building.building_address2} ${building.building_address3}<br>`
      this.infoWindow.open = true
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>