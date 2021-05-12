import { MapElementFactory } from "vue2-google-maps";

export default MapElementFactory({
    name: "directionsRenderer",

    ctr: () => google.maps.DirectionsRenderer, // eslint-disable-line

    events: ['directions_changed'],

    // create your watchers in `afterCreate()`.
    mappedProps: { 
        routeIndex: { type: Number }, 
        // options: { type: Object },  
        panel: { }, 
        directions: { type: Object }, 
        //// If you have a property that comes with a `_changed` event,
        //// you can specify `twoWay` to automatically bind the event, e.g. Map's `zoom`:
        // zoom: {type: Number, twoWay: true}
    },

    props: {
        origin: { type: Object },
        destination: { type: Object },
        travelMode: { type: String },
        options: { type: Object }, 
        toggle: {type: Boolean}  
    },

    // Actions you want to perform before creating the object instance using the
    // provided constructor (for example, you can modify the `options` object).
    // If you return a promise, execution will suspend until the promise resolves
    beforeCreate (options) {}, // eslint-disable-line

    // Actions to perform after creating the object instance.
    afterCreate(directionsRendererInstance) {
        let directionsService = new google.maps.DirectionsService(); // eslint-disable-line
      
        this.$watch(
        () => [this.origin, this.destination, this.travelMode, this.options, this.toggle],
        () => {
            let { origin, destination, travelMode, options, toggle } = this;
            if (!origin || !destination || !travelMode || !options || !toggle)  return;

            if(toggle == true){
                directionsService.route(
                {
                    origin,
                    destination,
                    travelMode
                },
                (response, status) => {
                    if (status == "OK"){
                        directionsRendererInstance.setDirections(response);
                        directionsRendererInstance.setOptions(options);
                    }else{
                        return;
                    }
                }
                );
            }else{
                directionsRendererInstance.unbindAll();
            }
        } 
        );
    }
});
