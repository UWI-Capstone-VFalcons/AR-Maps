<template>
    <div id="v-buildinginfo">
        <div class="bi-top">
            <img :src="b_image"/>
        </div>
        <div class="bi-body">
            <div class="bi-detail">
                <h1>{{b_name}}</h1>
                <div>
                   <p class="bi-address">{{b_address1}}</p>    
                    <p class="bi-address">{{b_address2}}</p>
                    <p class="bi-address">{{b_address3}}</p> 
                </div>
                <p><b>Building Type:</b> {{b_type}}</p>
                <p><b>Detail: </b> {{b_info}}</p>
                
                

            </div>
        </div>
    </div>
</template>

<script>
import EventBus from '@/event-bus';
import router from '@/router';

export default {
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
        }
       
    },

    methods: {

    },

    created: function (){
        if(this.buildingObject.qrType != "building"){
            router.replace({ name: 'Scan'});
        }else{
            EventBus.$emit('changeTitle', this.b_name)
        }

    }   
}
</script>