<template>
    <div>
        <base-top-bar 
            title="Building Info"
           :back_enable="true">
        </base-top-bar>
        <div id="v-buildinginfo">
            <div class="bi-top">
                <img :src="b_image"/>
            </div>
            <div class="bi-body">
                <div class="bi-detail">
                    <h1>{{b_name}}</h1>
                    <p class="b-address-t"><b>Address:</b></p>
                    <div>
                        <p class="bi-address">{{b_address1}}</p>    
                        <p class="bi-address">{{b_address2}}</p>
                        <p class="bi-address">{{b_address3}}</p> 
                    </div>
                    <p><b>Building Type:</b> {{b_type}}</p>
                    <p><b>Detail: </b> {{b_info}}</p>
                    <p class="bi-event-t" v-if="b_event_available"><b>Current Event:</b></p>
                    <div v-if="b_event_available"> 
                        <p class="bi-event-detail">Name: {{b_event_name}}</p>
                        <p class="bi-event-detail">Time: from {{b_event_start_time}}, to {{b_event_end_time}}</p>
                    </div>
                </div>
            </div>
        </div>
        <base-bottom-bar></base-bottom-bar>
    </div>
</template>

<script>
import BaseTopBar from '@/components/BaseTopBar';
import BaseBottomBar from '@/components/BaseBottomBar';
import axios from 'axios';
import router from '@/router';

export default {
    name:'BuildingInfo',
    components:{
        'base-top-bar':BaseTopBar,
        'base-bottom-bar':BaseBottomBar,
    },
    props: {
        buildingObject: {
            type: Object,
            // Object or array defaults must be returned from
            // a factory function
            default: function () {
                return { 
                    qrType: 'fake',
                    building_id: -1,
                    building_name:'default',
                    building_type:'none',
                    building_address1:'1234 test road',
                    building_address2:'ally view',
                    building_address3:'Country 10',
                    building_image: 'static/images/building/default_building.jpg',
                    building_latittude:98.7654,
                    building_longitude:12.3456,
                    building_info:'Just a default building',
                  }
            }
        }
    },

    data() {
        return{
            b_id: this.buildingObject.building_id,
            b_name: this.buildingObject.building_name,
            b_address1: this.buildingObject.building_address1,
            b_address2: this.buildingObject.building_address2,
            b_address3: this.buildingObject.building_address3,
            b_image: ''+this.$host+this.buildingObject.building_image,
            // b_image: this.buildingObject.building_image,
            b_type: this.buildingObject.building_type,
            b_info: this.buildingObject.building_info,
            b_longitude: this.buildingObject.building_longitude,
            b_latitiude: this.buildingObject.building_latittude,
            b_event_available: false,
            b_event_name: "",
            b_event_start_time: "",
            b_event_end_time: "",
        }
       
    },

    methods: {
        getEvents: function(){
            const path = this.$host+'api/event/current/'+this.b_id;
            axios.get(path)
            .then((res) => {
                let events = res.data.data;
                if(events.length > 0){
                    let cur_event = events[0]
                    this.b_event_available = true
                    this.b_event_name = cur_event.building_event_name
                    this.b_event_start_time = cur_event.building_event_start_time
                    this.b_event_end_time = cur_event.building_event_end_time
                }else{
                    this.b_event_available = false 
                }
            })
            .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
            });
        },
    },

    created: function (){
        if(this.buildingObject.qrType != "building"){
            router.replace({ name: 'Scan'});
            // this.getEvents()
        }else{
            this.getEvents()
        }
    }   
}
</script>
<style scoped>
/* bi is used as a shortening for building info */

#v-buildinginfo{
    height: 100%;
    width: 100%;
    background-color: gray;
    position: absolute;
    z-index: 1;
}

.bi-top{
    height: 40%;
    width: 100%;
    position: absolute;
    z-index: 1;
}

.bi-top img{
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
}

.bi-body{
    height: 70%;
    width: 100%;
    overflow-y: auto;
    background-color: white;
    border-top-left-radius: 1.5rem;
    border-top-right-radius: 1.5rem;
    z-index: 2;
    position: relative;
    padding-bottom: 8rem;
    top: 35%;
}

.bi-detail{
    padding: 1rem 2rem;
    padding-bottom: 2rem;
    width: 100%;
}

.bi-detail h1, .bi-detail p{
    width: fit-content;
}

.b-address-t, .bi-event-t{
margin-bottom: 5px;
}

.bi-detail h1{
    text-transform: capitalize;
    font-weight: bold;
}

.bi-address, .bi-event-detail{
    color: grey;
    line-height: 0.4rem;
    margin-left: 1rem;
}


@media (max-width: 480px) {
  .bi-detail h1{
    font-size: x-large;
  }
}
</style>