<template>
    <div id="arguide">  
        <a-scene
        renderer="logarithmicDepthBuffer: true;"
        embedded
        loading-screen="enabled: false;"
        arjs="sourceType: webcam; debugUIEnabled: false;"
        >
        <a-assets>
            <a-asset-item
                id="animated-asset"
                src="../assets/magnemite/scene.gltf"
                response-type="arraybuffer"
                crossorigin="anonymous"
            ></a-asset-item>
        </a-assets>

        <a-entity
            look-at="[gps-camera]"
            animation-mixer="loop: repeat"
            gltf-model="#animated-asset"
            scale="0.14768864307354904 0.14768864307354904 0.14768864307354904"
            gps-entity-place="latitude: 17.954413960210065; longitude: -76.90484832040967;"
        ></a-entity>

        <a-assets>
            <a-asset-item
                id="animated-asset-2"
                src="../assets/magnemite/scene.gltf"
                response-type="arraybuffer"
                crossorigin="anonymous"
            ></a-asset-item>
        </a-assets>

        <a-entity
            look-at="[gps-camera]"
            animation-mixer="loop: repeat"
            gltf-model="#animated-asset-2"
            scale="0.14768864307354904 0.14768864307354904 0.14768864307354904"
            gps-entity-place="latitude: 17.954594228561096; longitude: -76.9048856513913;"
        ></a-entity>

        <a-camera gps-camera rotation-reader></a-camera>
    </a-scene>
    </div>
</template>

<script>
// import '../ar-dependencies/aframe.min.js'
// import '../ar-dependencies/aframe-look-at-component.min.js'
// import '../ar-dependencies/aframe-extras.loaders.min.js'
// import * as THREE from 'three/build/three';


export default {
    name: 'ARView',
    Components: {
        // THREE,
        
    },
    
    props: {

    },
    
    data() {
        return {};
    },
    
    methods:{
        
    },

    watch: {
        
    },

    created(){
    },
    
    mounted() {
    //   if (document.getElementById('aframe-nft')) return; // was already loaded
    //   var scriptTag = document.createElement("script");
    //   scriptTag.src = "https://raw.githack.com/AR-js-org/AR.js/master/aframe/build/aframe-ar-nft.js";
    //   scriptTag.id = "aframe-nft";
    //   document.getElementsByTagName('head')[0].appendChild(scriptTag);
    },

}
</script>