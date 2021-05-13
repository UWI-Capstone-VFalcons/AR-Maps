<template>
    <div id="success-card">
        <div id="content">
            <h2 class="message">{{message}}</h2>
            <button 
                class="btn btn-primary" 
                @click="endTracking">
                Find another place
            </button>

            <button 
                class="btn btn-success" 
                @click="goToScanner">
                Verify location with QR code
            </button>
        </div>
    </div>    
</template>
<script>
import router from '@/router';

export default {
    name:"SuccessCard",
    props:{
        reachDestination:Boolean
    },
    data(){
        return{
            message:"You are at your destination",
            btnClasses:["btn", "btn-primary"],
        }
    },
    methods:{
        endTracking(){
            this.$emit("close");
        },
        goToScanner(){
            router.push({ name: 'Scan'});
            this.$emit("close");
        }
    }
}
</script>
<style scoped>
#success-card{
    height: 100%;
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 5;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: var( --main-dark-overlay-background);
}

#content{
    height: 50%;
    width: 20rem;
    background-color: white;
    border-radius: 15px;
    display: flex;
    flex-wrap: wrap;
    flex-direction: column;
    padding: 1rem;
}
.message{
    padding: 0.5rem 0rem;
}

.btn{
    padding: 0.5rem;
    margin: 1rem;
}
</style>