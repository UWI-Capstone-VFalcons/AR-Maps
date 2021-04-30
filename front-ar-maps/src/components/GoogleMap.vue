<template>
  <div> 
    <!-- <h6>// https://www.youtube.com/watch?v=KARBEHUyooM</h6> -->

    <div id="app-bar" class="main_bar">
      <div id="user-location">
        <img src="../assets/images/icons/map-pin.svg">
        <h6>{{destination_location}}</h6>
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
    </div>
         
   
       

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
import axios from 'axios';

let buildings_ar_paths = [];
let buildings_paths;
const slt1 = {lat:18.005197, lng:-76.749908}
const slt2 = {lat:18.005242, lng:-76.749795}





const test = { lat: 18.005656,  lng: -76.748537}
const test2 = { lat: 18.005612,lng: -76.748541}

const test3 = {lat:18.00533,lng: -76.74919}
const test4 = {lat: 18.005264, lng: -76.749158}


const uwi = {lat:18.00619408233222, lng:-76.74683600360201}






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

      this.addPath();
      // this.drawMarkers();
      this.drawDirection();
      this.print_path();
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
    clearMap(){
      this.paths = [];
      this.markers = [];
    },
    findPath(){

    },
    addPath(){
      const path = this.$host+'api/paths';
      
      axios.get(path)
        .then((res) => {
          for(let i=0; i<res.data.data.length;i++){
            // console.log(res.data.data[i])
            // buildingName = res.data.data[i].name;
            // buildingpos = 
            
            buildings_paths = [
              {
                pathName: res.data.data[i].name,
                position: [
                  {
                    lat:res.data.data[i].start_latitude_1, 
                    lng: res.data.data[i].start_longitude_1,
                  },
                  {
                    lat:res.data.data[i].start_latitude_2, 
                    lng: res.data.data[i].start_longitude_2
                  },
                  {
                    lat:res.data.data[i].end_latitude_1, 
                    lng: res.data.data[i].end_longitude_1
                  },
                  {
                    lat:res.data.data[i].end_latitude_2, 
                    lng: res.data.data[i].end_longitude_2
                  }
                ]

              }
            ]//End of building_paths
            // console.log("Buliding Name:"+buildingName);
            console.log(buildings_paths);
            this.buildings_ar_paths.push(buildings_paths);
            // this.paths=[buildings_paths.position[0],
            //               buildings_paths.position[1],
            //               buildings_paths.position[2],
            //               buildings_paths.position[3]];
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    print_path(){
      // console.log("This is B-AR-Paths")
      // console.log(buildings_ar_paths.length);
      // console.log(buildings_ar_paths.push("Hello"));
      // console.log(buildings_ar_paths.length);

      console.log(buildings_ar_paths);
      // console.log(JSON.stringify(buildings_ar_paths, null, 2));
      
      // 
      
      console.log(buildings_paths);


    },
    drawDirection(){
      // slt1,slt2,
      this.paths=[test,test2,test4,test3];
    },
    
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>









