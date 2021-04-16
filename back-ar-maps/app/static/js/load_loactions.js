window.onload = () => {
    let places = staticLoadPlaces();
    renderPlaces(places);
};

function staticLoadPlaces() {
   return [
       {
           name: 'Home Test',
           location: {
               lat: 18.0063554,
               lng: -76.7423310,
           }
       },
   ];
}

function renderPlaces(places) {
   let scene = document.querySelector('a-scene');

   places.forEach((place) => {
       let latitude = place.location.lat;
       let longitude = place.location.lng;

       let model = document.createElement('a-entity');
       model.setAttribute('gps-entity-place', `latitude: ${latitude}; longitude: ${longitude};`);
       model.setAttribute('gltf-model', './assets/magnemite/scene.gltf');
       model.setAttribute('rotation', '0 180 0');
       model.setAttribute('animation-mixer', '');
       model.setAttribute('scale', '0.5 0.5 0.5');

       model.addEventListener('loaded', () => {
           window.dispatchEvent(new CustomEvent('gps-entity-place-loaded'))
       });

       scene.appendChild(model);
   });
}