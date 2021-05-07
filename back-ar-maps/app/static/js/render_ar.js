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

function dynamicallyLoadDirections(currentLocation, destination) {

    // Building paths
    fetch(`/api/shortest_paths/ar/${destination}/${currentLocation[0]}/${currentLocation[1]}`,{
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

        let scene = document.querySelector('a-scene');

        let paths = jsonResponse.data.positions;
        var i = 0;
        paths.forEach(pos => {
            coordinates = pos[1];
            coordinates.forEach(coordinate => {
                let latitude = coordinate[0];
                let longitude = coordinate[1];
                let id = coordinate[2];
                let look_at = coordinate[3]

                console.log(latitude);
                console.log(longitude);
                
                let node_asset = document.createElement('a-assets');
                let node_model = document.createElement('a-asset-item');
                node_model.setAttribute('id', `node-${i}-${id}`);
                node_model.setAttribute('src', '/static/3d_models/arrow.glb');
                node_asset.appendChild(node_model);
                scene.appendChild(node_asset);


                let node_entity = document.createElement('a-entity');
                node_entity.setAttribute('gps-entity-place', `latitude: ${latitude}; longitude: ${longitude};`);
                node_entity.setAttribute('scale', '0.25 0.25 0.25');
                node_entity.setAttribute('gltf-model', `#node-${i}-${id}`);
                if(i == 0 && id == 0){
                    node_entity.setAttribute('look-at', '[gps-camera]');
                } else {
                    node_entity.setAttribute('look-at',`#node-${i}-${look_at}`);
                }
                scene.appendChild(node_entity);

            });
            i += 1;
        })

        // Finally add destination to map
        fetch(`/api/building/${destination}`, {
            method:'GET',
            headers:{
                Accept: 'application/json'  
            }
        })
        .then(response => {
            if (!response.ok) {
                throw Error(response.statusText);
              }
            return response.json();
        })
        .then(res => {
            console.log(res);

            let scene = document.querySelector('a-scene');

            let building = res.data;
            let latitude = building.building_latittude;
            let longitude = building.building_longitude;
            let name = building.building_name
            let id = building.building_id

            let building_asset = document.createElement('a-assets');
            let building_model = document.createElement('a-asset-item');
            building_model.setAttribute('id', `building-${id}`);
            building_model.setAttribute('src', '/static/3d_models/sign.glb');
            building_asset.appendChild(building_model);
            scene.appendChild(building_asset);


            let building_entity = document.createElement('a-entity');
            building_entity.setAttribute('gps-entity-place', `latitude: ${latitude}; longitude: ${longitude};`);
            building_entity.setAttribute('scale', '1 1 1');
            building_entity.setAttribute('gltf-model', `#building-${id}`);
            building_entity.setAttribute('look-at', '[gps-camera]');
            building_entity.setAttribute('animation','property: rotation; to: 0 360 0; loop: true; dur: 10000');
            building_entity.setAttribute('text',`value: ${name}; color:black; side:double; width: 5;`);
            scene.appendChild(building_entity);
        })
        .catch (function(error){
            // show error message
            console.log(error);
        })  
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
//loadPlacesNearMe();
dynamicallyLoadDirections([18.005621, -76.748550], 1);

}

//json returns root- has indexes of paths, postion- long and lat, meta - distance and time


