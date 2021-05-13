<template>
    <div id="app-bar" class="base_bar">
        <p 
            v-if="setBackEnable"
            id="back_message"
            @click="goBack">
            {{back_message}}
        </p>
        <div id="title_containter" v-if="setShowTitle">
            <h2 id="v-title">{{ setTitle }}</h2>
        </div>
        <div id="top_container">
            <slot></slot>
        </div>
    </div>
</template>

<script>
import router from '@/router';

export default {
    name:'BaseTopBar',
    props:{
        title: {String},
        show_title: {Boolean},
        back_enable: {Boolean},
    },
    data(){
        return{
            back_message: "< Swipe to go back"
        }
    },
    computed:{
        setTitle(){ return (this.title == null ||  this.title === 'undefined') ? this.$title : this.title},
        setShowTitle(){ return (this.show_title == null ||  this.show_title === 'undefined') ? true: this.show_title},
        setBackEnable(){ return (this.back_enable == null ||  this.back_enable === 'undefined') ? false: this.back_enable},
    },
    methods:{
        goBack(){
            router.go(-1)
        },
    }
}
</script>
<style scoped>
#app-bar{
    height: auto;
    width: 100%;   
    min-height: 4.5rem;
    position: absolute;
    z-index: 2;
    top: 0;
    color: white;
    border-bottom-left-radius: 15px;
    border-bottom-right-radius: 15px;
    padding-top: 1rem;
}

#title_containter{

}

#v-title{
    width: fit-content;
    padding: 0.5rem 1rem;
    color: whitesmoke;
}

#top_container{
    height: auto;
    width: 100%;
}

#back_message{
    text-align:start;
    padding: 0rem 1rem;
    padding-top: 0.5rem;
    margin-bottom: 0px;
}
</style>