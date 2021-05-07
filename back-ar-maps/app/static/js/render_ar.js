window.onload = () => {
// getting places from APIs

    function getLocation() {
        if(navigator.geolocation) {
            navigator.geolocation.watchPosition(setLocationName);
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    }

    function setLocationName(position){
        console.log('test');
        fetch(`/api/location_name/${position.coords.latitude},${position.coords.longitude}`,{
            method:'GET',
            headers:{
                Accept: 'application/json'
            }
        })
        .then(function (response) {
            if (!response.ok) {
                throw Error(response.statusText);
            }
            return response.json();
        })
        .then(function (res) {
            // show success message
            console.log(res);
            if(typeof res.data.error === 'undefined'){
                if(typeof res.data.name !== 'undefined'){
                    my_loc = document.getElementById('myLocation');
                    my_loc.value = res.data.name;
                }
            }else{
                console.log(res.data.error);
            }
        })
        .catch (function(error){
            // show error message
            console.log(error);
        })
    }

    function dynamicallyLoadPlaces() {

        fetch('/api/shortest_paths/ar/1/18.005621/-76.748550',{
            method:'GET',
            headers:{
                Accept: 'application/json'
            }
            // credentials: 'same-origin'
        })
        
        .then(function (response) {
            if (!response.ok) {
                throw Error(response.statusText);
            }
            return response.json();
        })
        .then(function (jsonResponse) {
            // show success message
            console.log(jsonResponse);
        })
        .catch (function(error){
            // show error message
            console.log(error);
        })              

    }
    dynamicallyLoadPlaces();
    getLocation()

  //  renderPlaces(places);
};

//json returns root- has indexes of paths, postion- long and lat, meta - distance and time


// window.onload = () => {
//     const scene = document.querySelector('a-scene');

//     // first get current user location
//     return navigator.geolocation.getCurrentPosition(function (position) {

//         // than use it to load from remote APIs some places nearby
//         loadPlaces(position.coords)
//             .then((places) => {
//                 places.forEach((place) => {
//                     const latitude = place.location.lat;
//                     const longitude = place.location.lng;

//                     // add place name
//                     const placeText = document.createElement('a-link');
//                     placeText.setAttribute('gps-entity-place', `latitude: ${latitude}; longitude: ${longitude};`);
//                     placeText.setAttribute('title', place.name);
//                     placeText.setAttribute('scale', '15 15 15');
                    
//                     placeText.addEventListener('loaded', () => {
//                         window.dispatchEvent(new CustomEvent('gps-entity-place-loaded'))
//                     });

//                     scene.appendChild(placeText);
//                 });
//             })
//     },
//         (err) => console.error('Error in retrieving position', err),
//         {
//             enableHighAccuracy: true,
//             maximumAge: 0,
//             timeout: 27000,
//         }
//     );
// };