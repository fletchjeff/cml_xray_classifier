import cdsw
from PIL import Image, ImageFilter
import numpy as np
from io import BytesIO
import base64
import os
import tensorflow as tf

#!ln -s /usr/local/cuda-11.1/targets/x86_64-linux/lib/libcusolver.so.11.0.1.105 /usr/local/cuda-11.1/targets/x86_64-linux/lib/libcusolver.so.10

# If you wish to do any testing of a new model and need an encoded image to use to provide
# arguments, uncomment and run the code below. It will create the `args` variable which you 
# can pass into the `predict()` function as it is the same format as the ajax call that comes
# from the browser.
# ```
# args = {
#   "image" : "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABGgAAALwC ...."
# }
# ``` 
# exec(open("data/base64_test_image_data.py").read())

model = tf.keras.models.load_model('/home/cdsw/models/model_2.h5')

@cdsw.model_metrics
def predict(args):
  im = Image.open(BytesIO(base64.b64decode(args['image'][22:])))#args['image'][22:])))
  im = im.resize((224,224),Image.ANTIALIAS)
  im = im.convert("RGB")
  im_array = tf.keras.preprocessing.image.img_to_array(im)
  im_array = np.expand_dims(im_array, axis=0)
  raw_prediction = model.predict(im_array)
  prediction_value = tf.nn.sigmoid(raw_prediction).numpy()
  if prediction_value >= 0.5:
    prediction = "virus"
  else:
    prediction = "bacteria"
  cdsw.track_metric("input_images", args)
  cdsw.track_metric("prediction",prediction)
  cdsw.track_metric("prediction_value",float(prediction_value))  
  return {
    "prediction":prediction,
    "prediction_value":float(prediction_value)
  }


