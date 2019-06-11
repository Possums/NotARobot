import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import pickle

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

sys.path.append("..")

from utils import label_map_util

from utils import visualization_utils as vis_util


MODEL_NAME = 'object_detection/inference_graph_checkbox'

PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

PATH_TO_LABELS = os.path.join('object_detection/inference_graph_checkbox', 'checkbox-detection.pbtxt')

NUM_CLASSES = 1


detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


IMAGE_SIZE = (12, 8)
TEST_IMAGE_PATHS=""

# In[ ]:


with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    # Definite input and output Tensors for detection_graph
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    # Each box represents a part of the image where a particular object was detected.
    detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
    image = Image.open("findbox.png")
      # the array based representation of the image will be used later in order to prepare the
      # result image with boxes and labels on it.
    image_np = load_image_into_numpy_array(image)
      # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
    image_np_expanded = np.expand_dims(image_np, axis=0)
      # Actual detection.
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})
    width, height = image.size
    ymin = boxes[0][0][0]*height
    xmin = boxes[0][0][1]*width
    ymax = boxes[0][0][2]*height
    xmax = boxes[0][0][3]*width
    print(classes)
    print('Top left')
    print (xmin,ymin)
    print('Bottom right')
    print (xmax,ymax)
    coordinates = [xmin, ymin, xmax, ymax]
    f = open('store.pckl', 'wb')
    pickle.dump(coordinates, f)
    f.close
