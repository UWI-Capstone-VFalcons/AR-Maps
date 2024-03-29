const webcamElement = document.getElementById('webcam');
var net;
webcamElement.height = 1080;
webcamElement.width = 720;

// set the classes for the model 
// to the classes list from the js file
MODEL_CLASSES = CLASSES;

// load the model
async function load_model() {
  console.log('Loading mobilenet..');
  const model = await  tf.loadGraphModel("/static/od_model/scitech_ojects/model.json");
  net = model; 
  console.log('Successfully loaded model');
  return model;
}

// the function to detect the object
async function detectObjects(image){
  tf.engine().startScope();
  var objects = [];
  var score = 0.8;
  var box = [];
  var o_class = 1;

  // convet the image into a tensor
  const pixels = image;
  const detections = await net.executeAsync(pixels.reshape([1, ...pixels.shape]));
  
  // get the number of objects that were detected
  const count = detections[2].dataSync()[0];

  // extract the objects with the highest scores and 
  for(let i = 0; i < count; i++){
    score = detections[6].dataSync()[i];

    // only return objects that get a god confidence score
    if(score >= 0.45){
      box = detections[0].arraySync()[0][i];
      o_class = detections[5].dataSync()[i];
      o_class = MODEL_CLASSES[o_class-1]["name"];

      // create object 
      let d_object = {
        "box": box,
        "score": score,
        "class": o_class
      };

      // add the objects to the list 
      objects.push(d_object);
    }
  }
  // clear the tensor from the memory
  tf.engine().endScope();
  return objects;
}

// activate the user camera and start trying to detect the object
async function detection() {
  await load_model();

  // Create an object from Tensorflow.js data API which could capture image 
  // from the web camera as Tensor.
  const webcam = await tf.data.webcam(webcamElement, {facingMode:'environment'});

  while (true) {
    let img = await webcam.capture();
    // console.log(img.print())

    const result = await detectObjects(img);

    if(result.length > 0){
      // console.log(result);
      // document.getElementById('console').innerText = `
      // prediction: ${result[0].class}, probability: ${result[0].score}`;
      let object_detected = processDetection(result);
      if(object_detected){
        webcam.stop()
        break;
      }
    }
    
    // Dispose the tensor to release the memory.
    img.dispose();

    // Give some breathing room by waiting for the next animation frame to
    // fire.
    await tf.nextFrame();
  }
}

// run this function whenever a object is detected
function processDetection(result){
  // all the data coming from post request
  if(typeof post_data !== 'undefined'){
    // check if the object detected is valid
    // that is to check if its in the zone
    if(typeof post_data.objects !== 'undefined'){
      // console.log(post_data);
      let detected_object_name = result[0].class;

      let zone_objects = post_data.objects;
      zone_objects.forEach(detectable_object => {
        if(detectable_object.object_digital_name == detected_object_name){
          console.log(result)
          // if the object matches calculate the error 
          // and return the error, zone, destination to 
          // the AR screen 

          // get object lat and long
          let obJ_lat = detectable_object.object_lat;
          let obj_lng = detectable_object.object_lng;

          // /get current position
          if(navigator.geolocation){
            navigator.geolocation.getCurrentPosition((position)=>{
              // fing the difference between the longitude and latitude
              // let lat_dif = Math.abs(position.coords.latitude - obJ_lat);
              // let lng_dif = Math.abs(position.coords.longitude - obj_lng);
              let lat_dif = position.coords.latitude - obJ_lat;
              let lng_dif = position.coords.longitude - obj_lng;
              
              // return te calculated error 
              // with the supporting information
              var result = {
                destination: post_data.destination,
                gps_error:{
                  lat:lat_dif,
                  lng:lng_dif
                },
                zone_id:post_data.zone_id
              }
              // console.log(result)

              jsonString = JSON.stringify(result)
              // console.log(jsonString);
              document.getElementById("post-data-field").value = jsonString
              
              // trigger redirection
              document.getElementById("hiddenForm").submit();

              return true

            })
          } else {
            alert("Geolocation is not supported by this browser.")
          }

        }
      });
    }
  }
  return false;
}

// add all the images that can be detected
function addImageOptionsToScreen(){
  if(typeof post_data !== 'undefined'){
    if(typeof post_data.objects !== 'undefined'){
      console.log(post_data);

      // display the card
      let bottom_bar = document.getElementById("botoom_option_bar");
      bottom_bar.classList.remove("d-none");

      // assign cancel button function
      let cancel_btn = document.getElementById("od_cancel_btn");
      cancel_btn.onclick = ()=>{
        console.log("cancel button pressed");
        // return te calculated error peviously 
        // with the supporting information
        var result = {
          destination: post_data.destination,
          gps_error: post_data.gps_error,
          zone_id:post_data.zone_id
        }
        console.log(result)

        jsonString = JSON.stringify(result)
        // console.log(jsonString);
        document.getElementById("post-data-field").value = jsonString
        
        // trigger redirection
        document.getElementById("hiddenForm").submit();
      };

      // add all the images detectable
      let images_container = document.getElementById("od-options");
      let zone_objects = post_data.objects;

      // create a list of all the detecable strings
      detectable_object_names = []
      zone_objects.forEach( detectable_object=>{
        detectable_object_names.push(detectable_object.object_digital_name)
      });

      console.log(detectable_object_names)

      MODEL_CLASSES.forEach( object=>{
        if(detectable_object_names.includes(object.name)){
          const htmlImg = `
          <div class="detectable_image">
            <img src="${object.image}"/>
          </div>
          `;
          images_container.innerHTML += htmlImg;
        }
      });
    }
  }
}

// object example
// var object_result = [
//   {
//       "box": [
//           0.014361947774887085,
//           0.004940152168273926,
//           0.9824674129486084,
//           1
//       ],
//       "score": 0.9105483293533325,
//       "class": "18.0053657_-76.7491452_physicssign"
//   }
// ]
// processDetection(object_result)

window.onload = ()=>{
  // set the title
  let app_bar_title_container = document.getElementById("title_containter");
  let app_bar_title = document.getElementById("v-title");
  app_bar_title_container.classList.remove("gone")
  app_bar_title.classList.remove("gone");
  app_bar_title.innerHTML = "GPS Calibration"

  addImageOptionsToScreen() 
  detection();
}
