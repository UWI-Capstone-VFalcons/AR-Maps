<template>
    <div>
        <qrcode-stream class="full_cam" @decode="onDecode"></qrcode-stream>
    </div>
</template>

<script>
// import qr code scanner from vue qr from https://github.com/gruhn/vue-qrcode-reader

// import { QrcodeStream, QrcodeDropZone, QrcodeCapture } from 'vue-qrcode-reader'
import { QrcodeStream} from 'vue-qrcode-reader'


export default {
    name: 'QRScanner',
    components: {
        QrcodeStream,
        // QrcodeDropZone,
        // QrcodeCapture
    },
    props: {
    },
    mounted () {
    },
    methods:{
        onDecode (decodedString) {
            let building_object = JSON.parse(decodedString);
            console.log(building_object.building_id);
        }
    }

}
</script>