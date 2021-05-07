window.onload = () => {
// getting places from APIs

function dynamicallyLoadPlaces() {

    fetch('/api/shortest_paths/ar/1/18.005621/-76.748550',{
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

        const scene = document.querySelector('a-scene');
        coordinates = jsonResponse.data.positions[0][1];
        coordinates.forEach(coordinate => {
            const latitude = coordinate[0];
            const longitude = coordinate[1];

            console.log(latitude);
            console.log(longitude);


             // add place name
             const placeText = document.createElement('a-link');
             placeText.setAttribute('gps-entity-place', `latitude: ${latitude}; longitude: ${longitude};`);
             placeText.setAttribute('title', coordinate.name);
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

    dynamicallyLoadPlaces();

}

//json returns root- has indexes of paths, postion- long and lat, meta - distance and time


