import cv2
#import tensorflow as tf
from tflite_runtime.interpreter import Interpreter
import numpy as np
from PIL import Image

from .helpers import *
from .variables import *

# *************** program config *********************
# show_window = True
run_inference = True

print("running model: ", model_filename)

# ************** MODEL CONFIG *******************
# Load TFLite model and allocate tensors.
if run_inference == True:

  #interpreter = tf.lite.Interpreter(model_path=model_filename)
  interpreter = Interpreter(model_path=model_filename)
  interpreter.allocate_tensors()

  # Get input and output tensors.
  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()

# *************** detection config *******************

# Visualization of the results of a detection.
draw_threshold = 0.5 # 0.05

# ***************************************************

# run inference with tensorflow lite model.
def run_lite_inference(large_cropped_pillow, cnn_input_size = 300):

  image = large_cropped_pillow.resize((cnn_input_size,cnn_input_size))
  input_data = np.array(image.getdata()).reshape((1, cnn_input_size, cnn_input_size, 3)).astype(np.float32)
  input_data = cv2.normalize(input_data, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

  # Test model on input image.
  interpreter.set_tensor(input_details[0]['index'], input_data)

  interpreter.invoke()

  detection_boxes = interpreter.get_tensor(output_details[0]['index'])[0]
  detection_classes = interpreter.get_tensor(output_details[1]['index'])[0].astype(np.uint8)
  detection_scores = interpreter.get_tensor(output_details[2]['index'])[0]
  num_boxes = interpreter.get_tensor(output_details[3]['index'])[0]
  detection_classes = (detection_classes + 1)

  return detection_boxes, detection_classes, detection_scores, num_boxes

def process_image(pillow_img):

    H, W = pillow_img.size
    max_square_size = min(H,W)

    pillow_img_cropped = im_crop_center(pillow_img, max_square_size, max_square_size)

    if run_inference:

        detection_boxes, detection_classes, detection_scores, num_boxes = run_lite_inference(pillow_img_cropped)

        # Parse detection results and draw annotation on current frame
        pillow_img_annotated = our_annotation_draw(pillow_img_cropped, detection_boxes, detection_scores, detection_classes, draw_threshold, max_square_size, max_square_size)
        #img_annotated = np.array(pillow_img_annotated)
        #to_draw = img_annotated

        # Color coorection for the image, if needed
        # correct_img_annotated = cv2.cvtColor(img_annotated, cv2.COLOR_BGR2RGB)

        # save to file
        # to_draw_pillow = Image.fromarray(temp_frame_np)
        
        return pillow_img_annotated, detection_boxes, detection_classes, detection_scores
