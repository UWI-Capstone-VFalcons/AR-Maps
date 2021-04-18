window.onload = () => {
    let places = staticLoadPlaces();
    let d_places = dynamicallyLoadPlaces();
    renderPlaces(places);
    renderPlaces(d_places);

};

// getting places from APIs
function dynamicallyLoadPlaces(position) {
    const params = {
        radius: 300,    // search places not farther than this value (in meters)
        clientId: 'MUT2A4LTDF03APAIS0MV3FKFLRARQ1PPORIVKDG42ICDX2H5',
        clientSecret: 'BIG1ZI35ZDIF5GS4PZPA2CDHM0L0AIUF4OA5ALVVDEOWRAZA',
        version: '20300101',    // foursquare versioning, required but unuseful for this demo
    };

    // CORS Proxy to avoid CORS problems
    const corsProxy = 'https://cors-anywhere.herokuapp.com/';
    
    (function() {
        var cors_api_host = 'cors-anywhere.herokuapp.com';
        var cors_api_url = 'https://' + cors_api_host + '/';
        var slice = [].slice;
        var origin = window.location.protocol + '//' + window.location.host;
        var open = XMLHttpRequest.prototype.open;
        XMLHttpRequest.prototype.open = function() {
            var args = slice.call(arguments);
            var targetOrigin = /^https?:\/\/([^\/]+)/i.exec(args[1]);
            if (targetOrigin && targetOrigin[0].toLowerCase() !== origin &&
                targetOrigin[1] !== cors_api_host) {
                args[1] = cors_api_url + args[1];
            }
            return open.apply(this, args);
        };
    })();
    // Foursquare API (limit param: number of maximum places to fetch)
    const endpoint = `${corsProxy}https://api.foursquare.com/v2/venues/search?intent=checkin
        &ll=${position.latitude},${position.longitude}
        &radius=${params.radius}
        &client_id=${params.clientId}
        &client_secret=${params.clientSecret}
        &limit=30 
        &v=${params.version}`;
    return fetch(endpoint)
        .then((res) => {
            return res.json()
                .then((resp) => {
                    return resp.response.venues;
                })
        })
        .catch((err) => {
            console.error('Error with places API', err);
        })
};


window.onload = () => {
    const scene = document.querySelector('a-scene');

    // first get current user location
    return navigator.geolocation.getCurrentPosition(function (position) {

        // than use it to load from remote APIs some places nearby
        loadPlaces(position.coords)
            .then((places) => {
                places.forEach((place) => {
                    const latitude = place.location.lat;
                    const longitude = place.location.lng;

                    // add place name
                    const placeText = document.createElement('a-link');
                    placeText.setAttribute('gps-entity-place', `latitude: ${latitude}; longitude: ${longitude};`);
                    placeText.setAttribute('title', place.name);
                    placeText.setAttribute('scale', '15 15 15');
                    
                    placeText.addEventListener('loaded', () => {
                        window.dispatchEvent(new CustomEvent('gps-entity-place-loaded'))
                    });

                    scene.appendChild(placeText);
                });
            })
    },
        (err) => console.error('Error in retrieving position', err),
        {
            enableHighAccuracy: true,
            maximumAge: 0,
            timeout: 27000,
        }
    );
};

function staticLoadPlaces() {
   return [
       {
           name: 'Home Test',
           location: {
               lat: 18.006056,
               lng: -76.742370,
           },
           name: 'Sci-Tech Library',
           location: {
               lat: 18.005283,
               lng: -76.749337,
           },
           name: 'SLT1',
           location: {
               lat: 18.005197,
               lng: -76.749908,
           },
           name: 'SLT2',
           location: {
               lat: 18.005306,
               lng: -76.749755,
           },
           name: 'SLT2 Entry/Exit 2',
           location: {
               lat: 18.005081,
               lng: -76.74980,
           },
           name: 'Aunty Jackie',
           location: {
               lat: 18.005167,
               lng: -76.749480,
           }
       },
   ];
}

function renderPlaces(places) {
   let scene = document.querySelector('a-scene');

   places.forEach((place) => {
       let latitude = place.location.lat;
       let longitude = place.location.lng;

       let model = document.createElement('a-link');
       model.setAttribute('gps-entity-place', `latitude: ${latitude}; longitude: ${longitude};`);
       placeText.setAttribute('title', places.name);
       placeText.setAttribute('scale', '15 15 15');

       model.addEventListener('loaded', () => {
           window.dispatchEvent(new CustomEvent('gps-entity-place-loaded'))
       });

       scene.appendChild(model);
   });
}