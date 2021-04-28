<template>
  <div> 
    <!-- <h6>// https://www.youtube.com/watch?v=KARBEHUyooM</h6> -->

    <div id="app-bar" class="main_bar">
      <div id="user-location">
        <img src="../assets/images/icons/map-pin.svg">
        <h6>{{destination_location}}</h6>
      </div>
    </div>
         
    <!-- </div>
       <div id="user-location">
        <img src="../assets/images/icons/map-pin.svg">
        <h6>{{destination_location}}</h6>
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
        </div>-->
       

    <!-- <div class="map-btns">
      <button @click="drawMarkers"> Draw Markers </button>

      <button @click="drawDirection"> Draw Direction </button>

      <button @click="clearMap"> Clear Map</button>
    </div> -->

    <GmapMap
  :center="centre"
  :zoom="17"
  style="width: 100%; height: 100vh;"
>
  <GmapMarker
    :key="index"
    v-for="(m, index) in markers"
    :position="m.position"
    :clickable="true"
    :draggable="false"
    @click="center=m.position"
  />

  <gmap-polygon :paths="paths" >  
  </gmap-polygon>
</GmapMap>
 
  </div>
</template>

<script>

const slt1 = {lat:18.005197, lng:-76.749908}
const slt2 = {lat:18.005242, lng:-76.749795}
const uwi = {lat:18.00619408233222, lng:-76.74683600360201}


const builing_data = [
  {
  'building_id': 1,
  'building_name':"slt1",
  'building_type':"building.b_type",
  'building_address1': "building.address1",
  'building_address2': "building.address2",
  'building_address3': "building.address3",
  'building_image': "building.image_url",
  'building_latittude': 'lt98.7654',
  'building_longitude':'lg12.3456',
  'building_info': 'building.info' 
  }
]

console.log(builing_data)

export default {
  name: 'GoogleMap',
  data(){
    return{
      destination_location: 'Location:',
      markers:[],
      centre:uwi,
      paths:[],
      myCoordinates:{
        lat:0,
        lng:0
      },
    }
  },
  created(){
    //get users coordinated from browser request
    this.$getLocation({}) //Prompts the user to reveal the location to our app
      .then(coordinates => {
        console.log(coordinates);
        this.myCoordinates = coordinates;
      })
        .catch(error => alert(error));
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

    }
    
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>