<template>
    <div id="map-view">   
        <base-top-bar 
            title="QR Scanner" 
            :show_title="false"
            :back_enable="true">
            <div class="form">
                <div :class="formClasses">
                    <label for="current_location" class="form-label col-lg-2 col-form-label" >
                        <img src="../assets/images/icons/map-pin.svg">
                        <p class="font-weight-bold">My Location: </p>
                    </label>
                    <div class="form-field col-lg-10">
                        <input type="text" readonly class="form-control font-weight-bold" id="current_location" :value="user_location_name">
                    </div>
                </div>

                <div :class="formClasses">
                    <label for="select-dest" class="form-label col-lg-2 col-form-label" >
                        <img src="../assets/images/icons/map-pin.svg">
                        <p class="font-weight-bold">Destination :</p>
                    </label>
                    <div class="form-field col-lg-10">
                        <select 
                            name="destinations" 
                            id="select-dest" 
                            class="form-control font-weight-bold"
                            v-model="destination">
                            <option 
                                selected :value="[null, null]" 
                                disabled>
                                Select Destination Here
                            </option>
                            <option 
                                v-for="(building, index) in all_buildings" 
                                :key="index" 
                                :value="[building.building_id, building.building_name]">
                                {{building.building_name }} 
                            </option>
                        </select>
                    </div>
                </div>
                <button :class="btnClasses" 
                    @click="toggleTracking">
                    {{buttonText}}
                </button>

            </div>
        </base-top-bar> 

        <div id="content">
            <GoogleMap 
            :destination_id="destination_id"
            :destinationName="destinationName"
            :istracking="istracking"
            @location_change="setLocation"
            @destinations_change="setDestination"
            @nav_metrics_change="setNavMetrics"
            />
        </div>

        <base-bottom-bar>
            <div id="map-bottom-metrix">
                <bottom-metric
                    :distance="nav_metrics.distance"
                    :time="nav_metrics.time" 
                    :destination="destinationName"
                    :active_card="istracking"
                />
            </div>
        </base-bottom-bar>   

        <success-card
        v-if="reachDestination"
        :reachDestination="reachDestination"
        @close="restMap"
        >
        </success-card>
    </div>
</template>

<script>
import BaseTopBar from '@/components/BaseTopBar';
import BaseBottomBar from '@/components/BaseBottomBar';
import GoogleMap from '@/components/GoogleMap.vue';
import BottomMetric from '@/map_components/BottomMetric';
import SuccessCard from '@/map_components/SuccessCard';


export default {
    name: 'OverheadMap',

    components: {
        'base-top-bar':BaseTopBar,
        'base-bottom-bar':BaseBottomBar,
        'bottom-metric': BottomMetric,
        'success-card': SuccessCard,
        GoogleMap,
    },

    data(){
        return{
            buttonText:'Get Direction',
            formClasses:['form-group'],
            btnClasses:["btn", "btn-primary"],
            user_location_name:"",
            all_buildings:[],
            destination:[null,null],
            istracking:false,
            nav_metrics:{
                distance: 0,
                time: 0,
            },
            reachDestination:false,
        }
    },

    computed:{
        destinationName(){ return this.destination[1] != null? this.destination[1]:'None';},
        destination_id(){return this.destination[0];},
    },

    methods:{
        setLocation(location){this.user_location_name = location},
        setDestination(destins){this.all_buildings = destins},
        setNavMetrics(navMetrics){this.nav_metrics = navMetrics},
        toggleTracking(){
            if(!this.istracking && this.destination[0] != null){
                this.istracking=true;  
                this.buttonText='Stop Tracking'  
                this.formClasses.push('gone');
                this.btnClasses.push('stop-btn');
            }else if(this.istracking){
                this.restMap();
            }else{
                alert("Please select a destination!");
            }  
        },
        restMap(){
            this.reachDestination=false;
            this.istracking=false;   
            this.buttonText='Get Direction'  
            this.formClasses.splice(this.formClasses.indexOf("gone"),1);
            this.btnClasses.splice(this.btnClasses.indexOf("stop-btn"),1);
        }
    }

}
</script>
<style scoped>
#map-view{
    height: 100%;
    width: 100%;
}
#content{
    height: 100%;
    width: 100%;
}

.form{
    padding: 0.5rem;
}

.form-group{
    display: flex;
    flex-wrap: nowrap;
    align-items: center;
    margin-bottom: 0px;
    margin: 5px;
}

.form-label{
    /* width: 55%; */
    display: flex;
    flex-wrap: nowrap;
    align-items: center;
    margin-bottom: 0px;
    padding: 0;
}

.form-label img{
     width: 3rem;
}

.form-label p{
    font-size: 1.2rem;
}

.form-field{
    padding: 0;
}

.form-field input{
}


.gone{
    display: none !important;
}

.stop-btn{
    background-color: #b22222 !important;
}
</style>