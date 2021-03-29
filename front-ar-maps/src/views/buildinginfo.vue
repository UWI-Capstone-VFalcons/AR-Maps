<template>
    <div id="v-buildinginfo">
        <img :src="b_image"/>
        <h1>{{b_name}}</h1>
        <p>{{b_type}}</p>
        <p>{{b_info}}</p>
        <p>{{b_address1}} {{b_address2}} {{b_address3}} </p>
    </div>
</template>

<script>
import EventBus from '../event-bus';

export default {
    props: {
        buildingObject: {
            type: Object,
            // Object or array defaults must be returned from
            // a factory function
            default: function () {
                return { 
                    building_id: -1,
                    building_name:'default',
                    building_type:'none',
                    building_address1:'1234 test road',
                    building_address2:'ally view',
                    building_address3:'Country 10',
                    building_image: 'https://images.pexels.com/photos/1092063/pexels-photo-1092063.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260',
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
            // b_image: ''+this.$host+this.buildingObject.building_image,
            b_image: this.buildingObject.building_image,
            b_type: this.buildingObject.building_type,
            b_info: this.buildingObject.building_info,
            b_longitude: this.buildingObject.building_longitude,
            b_latitiude: this.buildingObject.building_latittude,
        }
       
    },
    methods: {

    },
    created: function (){
        EventBus.$emit('changeTitle', this.b_name)
    }   
}
</script>