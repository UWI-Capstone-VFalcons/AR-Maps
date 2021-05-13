<template>
    <div id="card" :class="card_classes">
        <div id="tab_btn"
            @click="toggleBar">
            <div class="bar"></div>
        </div>
        <div id="content">
            <div class="walk-icon">
                 <img src="../assets/images/icons/walk.svg">
            </div>
            <div >
                <p id="metrics" class="font-weight-bold">{{setTime}} ({{setDistance}})</p>
                <p id="place">To {{destination}}</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'BottomMetric',
    props:{
        distance: Number,
        time: Number,
        destination: String,
        active_card: Boolean
    }, 
    data(){
        return{
            toggle: true,
            card_classes:['slide-in','gone'],
        }
    },
    computed:{
        setDistance(){
            if(this.distance>= 1000){ return (this.distance/1000).toFixed(1)+" m"}
            return (this.distance).toFixed(1)+" m"
        },
        setTime(){
            if(this.time>=3600){return (this.time/3600).toFixed(1)+" hrs";}
            else if(this.time>=60){return (this.time/60).toFixed(1)+" mins"}
            return (this.time).toFixed(1)+" secs"
        },
    },
    watch:{
        active_card: function(){
            if(this.active_card){ 
                this.toggle = true;
                this.card_classes.splice(this.card_classes.indexOf('gone'),1);
                this.card_classes.push('slide-out');
                this.card_classes.splice(this.card_classes.indexOf("slide-in"),1);
            }else
            { 
                this.toggle = false;
                this.card_classes.push('gone');
                this.card_classes.push('slide-in');
                this.card_classes.splice(this.card_classes.indexOf("slide-out"),1);
            }
        },
        toggle: function(){
            if(this.toggle){
                this.card_classes.push('slide-out');
                this.card_classes.splice(this.card_classes.indexOf("slide-in"),1);
            }else{
                this.card_classes.push('slide-in');
                this.card_classes.splice(this.card_classes.indexOf("slide-out"),1);
            }
        }
    },
    methods:{
        toggleBar(){this.toggle = !this.toggle}
    }
}
</script>
<style scoped>
#card{
    height: 8rem;
    width: 100%;
    display: flex;
    flex-wrap: nowrap;
    justify-content: flex-end;
    transition: 1s;
}
#tab_btn{
    height: 100%;
    width: 1rem;
    background-color:var(--main-background-color);
    border-top-left-radius: 15px;
    border-bottom-left-radius: 15px;   
    display: flex;
    justify-content: center;
    align-items: center;
}
.bar{
    width: 0.8rem; 
    height:6rem;
    margin: 0px 5px;
    display: block;
    background-color: white;
    opacity: 40%;
    border-radius: 5px;
}

#content{
    width: 100%;
    background-color: var(--main-background-white);
    display: flex;
    flex-wrap: nowrap;
    align-items: center;
    justify-content: flex-start;
}

.walk-icon{
    width: 5rem;
    height: auto;
}

#content div{
    text-align: initial;
    padding: 1rem;
}

#metrics{
    font-size: x-large;
}

#place{
    font-size: medium;
    word-wrap: normal;
}

/* animations */
.slide-in {
    transform: translateX(calc(100% - 1rem));
}

.slide-out {
    transform: translateX(0%);
}

.gone{
    display: none !important;
}
</style>