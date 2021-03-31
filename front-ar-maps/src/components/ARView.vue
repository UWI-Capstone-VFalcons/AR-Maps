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