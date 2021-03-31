<template>
    <div id="arguide">  
        <p id="current_location">
        <!-- Current location will be displayed here for testing-->
        </p>
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
import '../ar-dependencies/aframe-extras.loaders.min.js'
import '../ar-dependencies/aframe-ar-nft.js'
import '../ar-dependencies/aframe-look-at-component.min.js'
import '../ar-dependencies/aframe.min.js'

export default {
    name: 'ARView',
    components: {
        
    },
    
    props: {

    },
    
    data() {
    },
    
    methods:{
        
    },

    watch: {
        
    },

    created(){
    },

    mounted () {
    },

}
</script>