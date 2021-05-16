<template>
    <div id="bottom" >
        <div id="bottom_item">
            <slot></slot>
        </div>
        <!-- Bottom Navigation bar -->
        <div id="nav_group" class="base_bar">
            <router-link to="/" class="nav-el">
                <img src="../assets/images/icons/home.svg" alt="home"/>
                <p>Home</p>
            </router-link>
            <router-link to="/map" class="nav-el">
                <img src="../assets/images/icons/map-pin.svg" alt="map"/>
                <p>Map</p>
            </router-link>
            <router-link to="/scan" class="nav-el">
                <img src="../assets/images/icons/qr-code.svg" alt="QR Scanner"/>
                <p>Scan QR</p>
            </router-link>
            <router-link to="/ar" class="nav-el">
                <img src="../assets/images/icons/ar-view.svg" alt="AR Map"/>
                <p>AR</p>
            </router-link>
        </div>
    </div>
</template>

<script>
export default {
    name: 'BaseBottomBar',

}
</script>
<style scoped>
#bottom{
    height:auto;
    width: 100%;  
    min-height: 5rem;
    position: absolute;
    z-index: 2;
    bottom: 0;
    display: table-cell;
    vertical-align: bottom;
}

#bottom_item{
    height: auto;
    width: 100%;
    top: 0;
    margin-bottom: 4.5rem;
}

#nav_group{
    height: auto;
    width: 100%;
    min-height: 4.5rem;
    position: absolute;
    bottom: 0;
    border-top-left-radius: 15px;
    border-top-right-radius: 15px;   
    display: flex;
    flex-direction: row;
    justify-content:space-around;
    align-items: center;
}

.nav-el{
    width: 5rem;
    height: auto;
    margin: 0.5rem 1rem;
    padding: 0.2rem;
    border-radius: 0.5rem;
    color: white;
    text-align: center;
    display: flex;
    flex-flow: column;
    align-items: center;
}

.router-link-exact-active.nav-el{
    background-color: #3787FF;   
}

.nav-el img{
    width: 3rem;
    /* display: none; */
    height: auto;
    padding: 0.1rem;
    -webkit-filter: drop-shadow( 1px 1px 1px rgba(27, 27, 27, 0.7));
    filter: drop-shadow( 1px 1px 1px rgba(27, 27, 27, 0.7)); 
}

.nav-el p{
    margin: 0;
}

@media (max-width: 480px) {
    #nav_group{
        min-height: 5rem;
        justify-content: space-around;
    }
    .nav-el{
        margin: 0 0rem;
        padding: 0.3rem;
    }
    .nav-el img{
       width: 2rem; 
    }
}

</style>