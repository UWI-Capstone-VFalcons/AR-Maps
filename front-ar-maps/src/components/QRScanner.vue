<template>
    <div id="qrscanner">  
        <qrcode-stream id="scanner" class="full_cam" 
        @decode="onDecode"
        :camera="camera">
            <div id="qr-overlay">
                <p>Place your QR code in view</p>
                <div id="qr-box"></div>
            </div>
        </qrcode-stream>
    </div>
</template>

<script>
// import qr code scanner from vue qr from https://github.com/gruhn/vue-qrcode-reader

// import { QrcodeStream, QrcodeDropZone, QrcodeCapture } from 'vue-qrcode-reader'
import { QrcodeStream} from 'vue-qrcode-reader';
import router from '@/router';


export default {
    name: 'QRScanner',
    components: {
        QrcodeStream,
        // QrcodeDropZone,
        // QrcodeCapture
    },
    
    props: {
    },
    
    data() {
        return{
            camera: 'auto'
        }
    },
    
    methods:{
        onDecode (decodedString) {
            try{
                let building_object = JSON.parse(decodedString);
                if(building_object.qrType == "building"){
                    router.push({name: 'BuildingInfo', params: {buildingObject: building_object} });
                }else{
                    this.camera = "off";
                    alert("Invalid QR code used!");
                }
            }catch(error){
                this.camera = "off";
                alert("Invalid QR code used!");
            }
        }
    },

    watch: {
        'camera' (newval, oldval){
            if (newval == "off"){
                this.$nextTick(()=>{
                    this.camera = "auto";
                });
            }
            oldval
            // console.log("from "+oldval+" to "+newval);
        }
    },

    created(){
    },

    mounted () {
    },

}
</script>
<style>
#qrscanner{
    width: 100%;
    height: 100%;
    background-color: grey;
    display: flex;
    justify-content: center;
    align-items: center;
}

#scanner{
    display: block;
}
.qrcode-stream-overlay{
    display: flex;
    justify-content: center;
    align-items: center;
}

#qr-overlay{
    height: 70%;
    width: 70%;
    display: flex;
    flex-flow: column;
    justify-content: center;
    align-items: center;
}

#qr-overlay p{
    width: fit-content;
    color: grey;
    background-color: white;
    padding: 0.2rem 0.5rem;
    font-weight: bold;
    border-radius: 0.4rem;
}

#qr-box{ 
    width: 90%;
    height: 90%;
    border: 0.4rem dashed blue ;
    border-radius: 0.4rem;
    /* position: relative; */
    z-index: 10;
}

.full_cam{
    width:  auto !important;
    height: auto !important;
}
</style>