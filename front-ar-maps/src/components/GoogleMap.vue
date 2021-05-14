<template>
  <div> 
    <GmapMap
      :center="userCoordinates"
      :zoom="zoom_level"
      :options="map_options"
      style="width: 100%; height: 100vh;"
    >
      <!-- Draw all the paths that are not travelled on -->
      <gmap-polygon
        :key="'path_'+index"
        v-for="(plg, index) in paths_polygon"
        :editable="plg.editable"
        :draggable="plg.draggable"
        :options="plg.options"
        :path="plg.path"
      />  

      <!-- Draw all the custom routes-->
      <gmap-polygon
        :key="'route_'+index_r"
        v-for="(plg_r, index_r) in paths_route_polygon"
        :editable="plg_r.editable"
        :draggable="plg_r.draggable"
        :options="plg_r.options"
        :path="plg_r.path"
      />  

      <!-- Render the google generated route -->
      <DirectionsRenderer 
        :travelMode="travel_mode"
        :origin="userCoordinates"
        :destination="starting_point_coord"
        :options="google_route_options"
        :toggle="google_route_options.toggle"
      />

      <!-- Info Window if marker it is clicked -->
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
        :key="'building_'+index"
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

      <!-- Draw circle around user showing accuracy of user reading -->
      <GmapCircle
        :key="'accuracy_'+userMarker.key"
        :center="userCoordinates"
        :radius="(userCoordinates.accuracy+1)/1000"
        :options="userMarker.circle.options"
      />

      <!-- User Marker -->
      <GmapMarker
        v-if="location_avialable"
        :key="'user_'+userMarker.key"
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
import DirectionsRenderer from '../map_components/DirectionRenderer';


export default {
  name: 'GoogleMap',

  components: {
    DirectionsRenderer,
  },

  props:{
    destination_id: {Number},
    destinationName: {String},
    istracking: {Boolean},
  },

  data(){
    return{
      // Google map 
      // construction variables
      zoom_level:18,
      map_options:{
        disableDefaultUI:true
      },
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

      // google map route 
      // direction variables
      paths_route_polygon:[],
      travel_mode:"WALKING",
      starting_point_coord:{
        lat: 18.005636, 
        lng: -76.748542
      },
      google_route_options: {
        suppressMarkers:true,
        preserveViewport:true,
        polylineOptions:{
          strokeColor: "#FF00FF",
          strokeOpacity: 0.8,
          strokeWeight: 2,
          fillColor: "#FF00FF",
          fillOpacity: 0.35,
        },
        toggle:false,
      },

      // google maps 
      // user variables
      userCoordinates:{
        lat: 18.00520017651841, 
        lng: -76.74941982751545, 
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
      location_avialable: true,      

      // navigation variables cache
      user_location_name: {String},
      nav_metrics:{
        distance: 0,
        time: 0,
      },

      // database cached variables
      all_buildings:[],
      all_paths:[],
      best_route_data:{},
      route_paths:[],      
    }
  },

  created(){
    // continously set the location data as it change
    this.watchUserCoordinates(); 
  
    // add all the buildings when the map is creatred
    this.addAllBuildiings();

    // add all the paths to the map
    this.addAllPaths()

    // set the user location name property
    this.setLocationName();

    // test fake walk
    // this.testFakeWalk(-0.00040,-0.00040,5000)

  },
  
  watch:{
    userCoordinates: function(){
      console.log(this.userCoordinates);
      this.setLocationName();
      if(this.istracking==true){
        this.findPath();
      }
    },

    destination_id: function(to, from){
      if(from != null){
        this.markers[from-1].animation = 0
      }
      this.markers[to-1].animation = 1
    },

    istracking:function(){
      if(this.istracking==true){
        this.findPath();
      }else{
        this.google_route_options.toggle = false;
        this.paths_route_polygon = [];
      }
    } 
  },

  methods:{
    findPath(){  
      const path = this.$host+'api/shortest_paths/overheadMap/'+this.destination_id+'&('+this.userCoordinates.lat+','+this.userCoordinates.lng+')';
      axios.get(path)
        .then((res) => {
          
          //clear any previous path
          this.paths_route_polygon = []
          this.route_paths = []

          // console.log(res.data.data);
          this.best_route_data = res.data.data

          // generate path user should follow
          for(var indx_a in this.all_paths){
            if(this.best_route_data.route.includes(this.all_paths[indx_a].id)){
              this.route_paths.push(this.all_paths[indx_a])
            }
          }
          
          // draw the paths on the map
          for(var indx in this.route_paths){
            // var path_id = this.route_paths[indx].id;
            // var path_name = this.route_paths[indx].name;
            var path_start_1 = {lat: this.route_paths[indx].start_latitude_1, lng: this.route_paths[indx].start_longitude_1};
            var path_start_2 = {lat: this.route_paths[indx].start_latitude_2, lng: this.route_paths[indx].start_longitude_2};
            var path_end_1 = {lat: this.route_paths[indx].end_latitude_1, lng: this.route_paths[indx].end_longitude_1};
            var path_end_2 = {lat: this.route_paths[indx].end_latitude_2, lng: this.route_paths[indx].end_longitude_2};

            this.paths_route_polygon.push({
              draggable: false,
              editable: false, 
              options:{
                strokeColor: "#FF00FF",
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: "#FF00FF",
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

          // activate google direction renderer if the person is outside scit tech
          if(this.best_route_data.use_starting_point == true){
            this.starting_point_coord.lat = this.best_route_data.starting_point_latitude;
            this.starting_point_coord.lng = this.best_route_data.starting_point_longitude;
            this.google_route_options.toggle = true;
          }

          // Set the metrix information
          this.nav_metrics.distance = this.best_route_data.metrics.distance;
          this.nav_metrics.time = this.best_route_data.metrics.time;
          this.$emit('nav_metrics_change', this.nav_metrics);

          // check if the user is at their destination 
          // and send a notification if they are
          if(this.best_route_data.reach_destination){
            this.$emit("reachDestination");
          }

        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },

    watchUserCoordinates(){
      // get the users current location from device
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
          // check if there was an error 
          if(typeof res.data.error === 'undefined'){
            if(typeof res.data.data.name !== 'undefined'){
              // save the name if its valid
              this.user_location_name = res.data.data.name;
              this.$emit('location_change', this.user_location_name);
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
          this.$emit('destinations_change', this.all_buildings);
          
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
      // open the window for a marker when clicked
      const building = this.all_buildings[index];
      this.infoWindow.position = { lat: building.building_latittude, lng: building.building_longitude }
      this.infoWindow.template = `<b>${building.building_name}</b><br>${building.building_address1}<br>${building.building_address2} ${building.building_address3}<br>`
      this.infoWindow.open = true
    },

    testFakeWalk(x=1, y=1, delay=1000){
      // test walking in app
      // debugging purposes
      this.polling = setInterval(() => {
        let point = new this.google.maps.Point(
        this.userCoordinates.lat + x,
        this.userCoordinates.lng + y) 
          
        this.userCoordinates.lat = point.x;
        this.userCoordinates.lng = point.y;

        this.setLocationName();
        if(this.istracking==true){
          this.findPath();
        }
      }, delay);
    },

  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>