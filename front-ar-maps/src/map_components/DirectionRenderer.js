import { MapElementFactory } from "vue2-google-maps";

export default MapElementFactory({
    name: "directionsRenderer",

    ctr: () => google.maps.DirectionsRenderer, // eslint-disable-line

    events: [],

    // create your watchers in `afterCreate()`.
    mappedProps: { 
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
            // check if any of the variables change
            () => [this.origin,this.destination,this.toggle,this.options],
            () => {
                console.log("direction route changed");
                // set the variables internally
                let { origin, destination, travelMode, options, toggle } = this;

                // check if the routing service is needed
                if(toggle == true){
                    // draw the route on the map if the routing service is needed
                    directionsService.route(
                    {
                        origin: origin,
                        destination: destination,
                        travelMode: travelMode,
                        unitSystem: google.maps.UnitSystem.METRIC // eslint-disable-line
                    },
                    (response, status) => {
                        if (status == "OK"){
                            directionsRendererInstance.setDirections(response);
                            directionsRendererInstance.setOptions(options);
                        }else{
                            console.log(status);
                        }
                    });
                }

            },
            {
                // ensure to check if there was any change inside of the variable 
                // and run the function on the inital start
                deep:true,
                immediate:true,
            }
        );
    }
});
