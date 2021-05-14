window.onload = () => {
    
    var watchID;
    var zone;

    function getLocation() {
        if(navigator.geolocation) {
            return navigator.geolocation.watchPosition(setCurrentLocationName);
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    }

    // reacticely get the path to the users destination
    function getPath(){
        if(navigator.geolocation) {
            return navigator.geolocation.watchPosition(dynamicallyLoadDirections);
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    }

    // watch the map zone the user is in
    function getZone(){
        if(navigator.geolocation) {
            return navigator.geolocation.watchPosition(getCurrentZone);
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

    function dynamicallyLoadDirections(position) {
        let destination = document.getElementById('myDestination').value;
        // Building paths
        fetch(`/api/shortest_paths/ar/${destination}/${position.coords.latitude}/${position.coords.longitude}`,{
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
            // console.log(jsonResponse.data.positions[0][1][0][1]);

            let meta = jsonResponse.data.meta;

            clearLocations();

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
                    node_entity.setAttribute('scale', '0.5 0.5 0.5');
                    node_entity.setAttribute('gltf-model', `#node-${i}-${id}`);
                    if(i == 0 && id == 0 || look_at === 'camera'){
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
                building_entity.setAttribute('scale', '1.5 1.5 1.5');
                building_entity.setAttribute('gltf-model', `#building-${id}`);
                building_entity.setAttribute('look-at', '[gps-camera]');
                building_entity.setAttribute('animation','property: rotation; to: 0 360 0; loop: true; dur: 10000');
                if(meta !== undefined){
                    building_entity.setAttribute('text',`value: ${name} ${meta.time} mins (${meta.distance}m) away ; color:black; side:double; width: 5;`);
                } else {
                    building_entity.setAttribute('text',`value: ${name}; color:black; side:double; width: 5;`);
                }
                scene.appendChild(building_entity);

                if (latitude === position.coords.latitude && longitude === position.coords.longitude) {
                    alert('Congratulation, you reach the destination');
                    navigator.geolocation.clearWatch(watchID);
                }
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

    function getCurrentZone(position){
        fetch(`/api/zone/${position.coords.latitude}/${position.coords.longitude}`,{
            method: 'GET',
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
            // Do stuff with Object Detection here!!!
            let current_zone = res.data.zone_id;
            if(zone !== current_zone){
                // show button to redirect
            }
        })
        .catch (function(error){
            // show error message
            console.log(error);
        }) 
    }

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

    function clearLocations(){
        document.querySelectorAll("a-entity").forEach(e => e.remove());
        document.querySelectorAll("a-asset-item").forEach(e => e.remove());
        document.querySelectorAll("a-assets").forEach(e => e.remove());
    }

    getLocation();
    loadPlacesNearMe();
    //watchID = getPath();
    getZone();

    let dest = document.getElementById('myDestination');
    dest.addEventListener('change',()=>{
        if(watchID){
            navigator.geolocation.clearWatch(watchID);
        }
        console.log(dest.value);
        watchID = getPath();
        console.log(watchID);
    })

    document.querySelector('div.a-enter-vr').remove()
    document.querySelector('div.a-enter-ar').remove()


}

//json returns root- has indexes of paths, postion- long and lat, meta - distance and time


