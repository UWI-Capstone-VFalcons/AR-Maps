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
    if(score >= 0.95){
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
      console.log(result);
      // document.getElementById('console').innerText = `
      // prediction: ${result[0].class}, probability: ${result[0].score}`;
      processDetection(result);
      webcam.stop()
      break;
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
  console.log(post_data);
}
processDetection(1)
detection();