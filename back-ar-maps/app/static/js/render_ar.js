window.onload = () => {

function getLocation() {
    if(navigator.geolocation) {
        navigator.geolocation.watchPosition(setCurrentLocationName);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function setCurrentLocationName(position){
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

function dynamicallyLoadDirections() {

    fetch(`/api/shortest_paths/ar/1/18.005620/-76.748580`,{
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
    .then(function (jsonResponse) {
        // show success message
        console.log(jsonResponse);
        console.log(jsonResponse.data.positions[0][1][0][1]);

        const scene = document.querySelector('arrow-asset');

        coordinates = jsonResponse.data.positions[0][1];
        coordinates.forEach(coordinate => {
            const latitude = coordinate[0];
            const longitude = coordinate[1];

            console.log(latitude);
            console.log(longitude);


             const placeText = document.createElement('a-link');
             placeText.setAttribute('gps-entity-place', `latitude: ${latitude}; longitude: ${longitude};`);
             placeText.setAttribute('scale', '15 15 15');
   
             placeText.addEventListener('loaded', () => {
                window.dispatchEvent(new CustomEvent('gps-entity-place-loaded'))
            });

            scene.appendChild(placeText);
        
    });

        (err) => console.error('Error in retrieving position', err),
        {
            enableHighAccuracy: true,
            maximumAge: 0,
            timeout: 27000,
        }
    })
    .catch (function(error){
        // show error message
        console.log(error);
    })              

};

function loadPlacesNearMe() {

    // fetch(`/api/closest/destination/${position.coords.latitude},${position.coords.longitude}`,{
    fetch(`/api/destinations`,{  
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
    .then(function (jsonResponse) {
        // show success message
        console.log(jsonResponse);
        console.log(jsonResponse.data[0].building_latittude);
        console.log(jsonResponse.data[0].building_longitude);
        console.log(jsonResponse.data[0].building_name);

        const scene = document.querySelector('a-scene');

        coordinates = jsonResponse.data;
        coordinates.forEach(coordinate => {
            const latitude = coordinate.building_latittude;
            const longitude = coordinate.building_longitude;

            console.log(latitude);
            console.log(longitude);

             // add place name
             const placeText = document.createElement('a-link');
             placeText.setAttribute('gps-entity-place', `latitude: ${latitude}; longitude: ${longitude};`);
             placeText.setAttribute('title', coordinate.building_name);
             placeText.setAttribute('scale', '15 15 15');
   
             placeText.addEventListener('loaded', () => {
                window.dispatchEvent(new CustomEvent('gps-entity-place-loaded'))
            });

            scene.appendChild(placeText);
        
    });

        (err) => console.error('Error in retrieving position', err),
        {
            enableHighAccuracy: true,
            maximumAge: 0,
            timeout: 27000,
        }
    })
    .catch (function(error){
        // show error message
        console.log(error);
    })              

};

getLocation();
loadPlacesNearMe();
dynamicallyLoadDirections();

}

//json returns root- has indexes of paths, postion- long and lat, meta - distance and time


