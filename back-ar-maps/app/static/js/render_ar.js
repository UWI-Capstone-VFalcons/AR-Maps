window.onload = () => {
    // navigator.mediaDevices.enumerateDevices().then(function(devices) {
    //     var userMediaConstraints = {
    //         audio: false,
    //         video: {
    //             facingMode: 'environment',
    //             width: {
    //                 ideal: this.parameters.sourceWidth,
    //                 min: 1024,
    //                 max: 1920
    //             },
    //             height: {
    //                 ideal: this.parameters.sourceHeight,
    //                 min: 776,
    //                 max: 1080
    //             }
    //         }
    //     }


    //     if (null !== this.parameters.deviceId) {
    //         userMediaConstraints.video.deviceId = {
    //             exact: _this.parameters.deviceId
    //         };
    //     }
    //     // get a device which satisfy the constraints
    //     navigator.mediaDevices.getUserMedia(userMediaConstraints).then(function success(stream) {
    //         // set the .src of the domElement
    //         domElement.srcObject = stream;
    //         var event = new CustomEvent('camera-init', {stream: stream});
    //         window.dispatchEvent(event);
    //         // to start the video, when it is possible to start it only on userevent. like in android
    //         document.body.addEventListener('click', function(){
    //             domElement.play();
    //         });
    //         // domElement.play();
    //                     // TODO listen to loadedmetadata instead
    //         // wait until the video stream is ready
    //         var interval = setInterval(function() {
    //             if (!domElement.videoWidth)	return;
    //             onReady()
    //             clearInterval(interval)
    //         }, 1000/50);

    //         // CUSTOM CODE START
    //         var backCam2 = devices.filter(d=>{
    //             return d.label && d.label == "camera2 0, facing back";
    //             })
    //             if (backCam2.length) {
    //             userMediaConstraints.video.deviceId = backCam2[0].deviceId
    //             }
    //             // CUSTOM CODE END
    

    //     }).catch(function(error) {
    //         onError({
    //             name: error.name,
    //             message: error.message
    //         });
    //     });
    //     }).catch(function(error) {
    //         console.log(error.message);
    //     onError({
    //         message: error.message
    //     });
    // });
    
    var watchID;

    function getLocation() {
        if(navigator.geolocation) {
            return navigator.geolocation.watchPosition(setCurrentLocationName);
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    }

    function getPath(){
        if(navigator.geolocation) {
            return navigator.geolocation.watchPosition(dynamicallyLoadDirections);
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

            // clear all the locations before readding anything
            clearLocations();

            // connect the ar scence
            let scene = document.querySelector('a-scene');

            // get all the positions for the 3d objects
            // create then add them to the scene
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
                    
                    // create the 3d models to direct users
                    let node_asset = document.createElement('a-assets');
                    let node_model = document.createElement('a-asset-item');
                    node_model.setAttribute('id', `node-${i}-${id}`);
                    node_model.setAttribute('src', '/static/3d_models/arrow.glb');
                    node_asset.appendChild(node_model);
                    scene.appendChild(node_asset);

                    // create the trackaable objects
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

            // Finally add destination object to the map
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

                // extract th building information
                let building = res.data;
                let latitude = building.building_latittude;
                let longitude = building.building_longitude;
                let name = building.building_name
                let id = building.building_id

                // create 3d object for the building 
                let building_asset = document.createElement('a-assets');
                let building_model = document.createElement('a-asset-item');
                building_model.setAttribute('id', `building-${id}`);
                building_model.setAttribute('src', '/static/3d_models/sign.glb');
                building_asset.appendChild(building_model);
                scene.appendChild(building_asset);

                // create trackable objects
                let building_entity = document.createElement('a-entity');
                building_entity.setAttribute('gps-entity-place', `latitude: ${latitude}; longitude: ${longitude};`);
                building_entity.setAttribute('scale', '1.5 1.5 1.5');
                building_entity.setAttribute('gltf-model', `#building-${id}`);
                building_entity.setAttribute('look-at', '[gps-camera]');
                building_entity.setAttribute('animation','property: rotation; to: 0 360 0; loop: true; dur: 10000');

                // Add metrics information and 
                // name of the building to the scene
                if(meta !== undefined){
                    building_entity.setAttribute('text',`value: ${name} ${meta.time} mins (${meta.distance}m) away ; color:black; side:double; width: 5;`);
                } else {
                    building_entity.setAttribute('text',`value: ${name}; color:black; side:double; width: 5;`);
                }
                scene.appendChild(building_entity);

                // 
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

    // Call the functions 

    getLocation();
    //loadPlacesNearMe();
    watchID = getPath();

    let dest = document.getElementById('myDestination');
    dest.addEventListener('change',()=>{
        navigator.geolocation.clearWatch(watchID);
        console.log(dest.value);
        console.log(watchID);
        watchID = getPath();
        console.log(watchID);
    })

    document.querySelector('div.a-enter-vr').remove()
    document.querySelector('div.a-enter-ar').remove()


}

//json returns root- has indexes of paths, postion- long and lat, meta - distance and time


