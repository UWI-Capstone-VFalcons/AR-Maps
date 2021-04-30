<template>
  <div> 
        <!-- <h6>// https://www.youtube.com/watch?v=KARBEHUyooM</h6> -->
    <div id="user-location">
      <img src="../assets/images/icons/map-pin.svg">
      <h6>Location: {{user_location_name}}</h6>
    </div>

    <div id="user-destination">
      <div >
        <label for="">Destination:</label>
        <select name="destinations" id="dd-dest"  v-model="destination_id">
          <option selected :value="null" disabled >Select Destination Here</option>
          <option v-for="(building, index) in all_buildings" 
          :key="index" 
          :value="building.building_id">
            {{building.building_name }} 
          </option>
        </select>
        <button @click="findPath">Find Path</button>
      </div>
    </div>

    <GmapMap
      :center="userCoordinates"
      :zoom="zoom_level"
      style="width: 100%; height: 100vh;"
    >
      <!-- Draw all the paths that are not travelled on -->
      <gmap-polygon
        :key="'plg'+index"
        v-for="(plg, index) in paths_polygon"
        :editable="plg.editable"
        :draggable="plg.draggable"
        :options="plg.options"
        :path="plg.path"
      />  

      <!-- Draw circle around user showing accuracy of reading -->
      <GmapCircle
        :key="'uc'+userMarker.key"
        :center="userCoordinates"
        :radius="(userCoordinates.accuracy+1)/1000"
        :options="userMarker.circle.options"
      />

      <!-- Marker Window if it is clicked -->
      <GmapInfoWindow
      :options="infoWindow.options"
      :position="infoWindow.position"
      :opened="infoWindow.open"
      @closeclick="infoWindow.open=false"
      >
      <div v-html="infoWindow.template"></div>
      </GmapInfoWindow>

      <!-- Building Markers -->
      <GmapMarker
        :key="'m'+index"
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

      <!-- User Marker -->
      <GmapMarker
        :key="'m'+userMarker.key"
        :position="userCoordinates"
        :title="userMarker.title"
        :icon="userMarker.icon"
        :animation="userMarker.animation"
        :clickable="false"
        :draggable="false"
      />

    </GmapMap>

  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'GoogleMap',
  data(){
    return{
      // Google map variables
      zoom_level:19,
      markers:[],
      paths_polygon:[],
      infoWindow:{
        options: {
          maxWidth: 300,
          pixelOffset: { width: 0, height: -35 }
        },
        position:{lat:0, lng:0},
        open:false,
        template:'',
      },
      // database cached variables
      all_buildings:[],
      all_paths:[],
      // user variables
      userCoordinates:{
        lat:18.00619408233222,
        lng:-76.74683600360201,
        accuracy:0
      },
      userMarker:{
        key:"user",
        title:"User",
        icon: {
          url: require('../assets/images/icons/map/user.png'),
          scaledSize: {width: 25, height: 25, f: 'px', b: 'px',},
          labelOrigin: {x:75, y:35},
        },
        animation:2,
        circle:{
          options:{
            strokeColor: "#FF0000",
            strokeOpacity: 0.2,
            strokeWeight: 2,
            fillColor: "#FF0000",
            fillOpacity: 0.35,
            visible:true,
          },  
        }
      },
      location_avialable: false,
      // navigation variables
      destination_id:null,
      user_location_name:""
    }
  },
  created(){
    // continously set the location data as it change
    // this.watchUserCoordinates(); 
  
    // add all the buildings when the map is creatred
    this.addAllBuildiings();

    // add all the paths to the map
    this.addAllPaths()

    // set the user location name property
    this.setLocationName();
  },
  
  watch:{
    userCoordinates: function(){
      console.log(this.userCoordinates);
      this.setLocationName();
    },

    destination_id: function(to, from){
      if(from != null){
        this.markers[from-1].animation = 0
      }
      this.markers[to-1].animation = 1
    }
  },

  methods:{
    drawMarkers(){
      // this.markers = [
      //   {
      //     position:slt1,
      //   },
      //   {
      //     position:slt2,
      //   },
      // ];
    },

    drawDirection(){
      // this.paths=[slt1,slt2];
    },

    clearMap(){
      this.paths = [];
      this.markers = [];
    },

    findPath(){  
      console.log("finding path")
    },

    watchUserCoordinates(){
      if ("geolocation" in navigator){
        navigator.geolocation.watchPosition(position => {
          this.userCoordinates = {
            lat:position.coords.latitude,
            lng:position.coords.longitude,
            accuracy:position.coords.accuracy
          }
          this.location_avialable = true
          // console.log(position);
        }, err => {
          const errorStr = err.message;
          console.log(errorStr)
        });
      }else{
        this.location_avialable = false;
        console.log("Geolocation not available");
      }
    },

    setLocationName(){
      const path = this.$host+'api/location_name/'+this.userCoordinates.lat+','+this.userCoordinates.lng;
      axios.get(path)
        .then((res) => {
          // console.log(res);
          if(typeof res.data.error === 'undefined'){
            if(typeof res.data.data.name !== 'undefined'){
              this.user_location_name = res.data.data.name;
            }
          }else{
            console.log(res.data.error);
          }
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
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
                  fontSize: "11px",
                }, 
                markerIcon: {
                  url: require('../assets/images/icons/map/building.png'),
                  // size: {width: 60, height: 90, f: 'px', b: 'px',},
                  scaledSize: {width: 28, height: 28, f: 'px', b: 'px',},
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

    addAllPaths(){
      const url_path = this.$host+'api/paths';
      axios.get(url_path)
        .then((res) => {
          this.all_paths = res.data.data;
          for(var indx in this.all_paths){
            // var path_id = this.all_paths[indx].id;
            // var path_name = this.all_paths[indx].name;
            var path_start_1 = {lat: this.all_paths[indx].start_latitude_1, lng: this.all_paths[indx].start_longitude_1};
            var path_start_2 = {lat: this.all_paths[indx].start_latitude_2, lng: this.all_paths[indx].start_longitude_2};
            var path_end_1 = {lat: this.all_paths[indx].end_latitude_1, lng: this.all_paths[indx].end_longitude_1};
            var path_end_2 = {lat: this.all_paths[indx].end_latitude_2, lng: this.all_paths[indx].end_longitude_2};

            this.paths_polygon.push({
              draggable: false,
              editable: false, 
              options:{
                strokeColor: "#FF0000",
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: "#FF0000",
                fillOpacity: 0.35,
              },
              path:[
                path_start_1,
                path_start_2,
                path_end_2,
                path_end_1,
                path_start_1
              ],
            });
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