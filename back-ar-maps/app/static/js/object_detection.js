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
    if(score >= 0.9){
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
  const webcam = await tf.data.webcam(webcamElement);

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
              let lat_dif = Math.abs(position.coords.latitude - obJ_lat);
              let lng_dif = Math.abs(position.coords.longitude - obj_lng);
              
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
detection();