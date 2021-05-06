window.onload = () => {
    let places = dynamicallyLoadPlaces();
    renderPlaces(places);
};

// getting places from APIs
function dynamicallyLoadPlaces(position) {
    fetch('',{
        method:'GET',
        headers:{
            Accept: 'application/json',
            //'Content-Type': 'multipart/form-data',
            'X-CSRFToken': token
        },
        credentials: 'same-origin'
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