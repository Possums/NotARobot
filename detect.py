import pickle
import pyautogui
import time
import os
from PIL import Image, ImageDraw
import pytesseract
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
import requests
from object_detection.utils import label_map_util


captchatype = sys.argv[1]
captchaclass = sys.argv[2]
print(captchatype)
print(captchaclass)
final_image = Image.open('finalimage.png')
width, height = final_image.size

#helper code to map captcha boxes
class Point:
    def __init__(self, xcoord, ycoord):
        self.x = xcoord
        self.y = ycoord

class Rectangle:
    def __init__(self, topLeft, bottomRight):
        self.topLeft = topLeft
        self.bottomRight = bottomRight

#determine which boxes intersect with detections
def intersect(R1, R2):
    if ((R1.topLeft.x > R2.bottomRight.x) or (R1.bottomRight.x < R2.topLeft.x) or (R1.topLeft.y > R2.bottomRight.y) or (R1.bottomRight.y < R2.topLeft.y)):
        return False
    else:
        return True


if captchatype == '3x3':
    #Set up 3x3 grid of captcha squares
    box1 = Rectangle(Point(0,0), Point(int(width/3),int(height/3)))
    print("box1 " + str(box1.topLeft.x) + " " + str(box1.topLeft.y) + ";" + str(box1.bottomRight.x) + "," + str(box1.bottomRight.y))
    box2 = Rectangle(Point(int(width/3)+1,0), Point(2*int(width/3),int(width/3)))
    print("box2 " + str(box2.topLeft.x) + "," + str(box2.topLeft.y) + ";" + str(box2.bottomRight.x) + "," + str(box2.bottomRight.y))
    box3 = Rectangle(Point(2*int(width/3)+1,0), Point(width,int(height/3)))
    print("box3 " + str(box3.topLeft.x) + "," + str(box3.topLeft.y) + ";" + str(box3.bottomRight.x) + "," + str(box3.bottomRight.y))
    box4 = Rectangle(Point(0,int(height/3)+1), Point(int(width/3),2*int(height/3)))
    print("box4 " + str(box4.topLeft.x) + "," + str(box4.topLeft.y) + ";" + str(box4.bottomRight.x) + "," + str(box4.bottomRight.y))
    box5 = Rectangle(Point(int(width/3)+1,int(height/3)+1), Point(2*int(width/3),2*int(height/3)))
    print("box5 " + str(box5.topLeft.x) + "," + str(box5.topLeft.y) + ";" + str(box5.bottomRight.x) + "," + str(box5.bottomRight.y))
    box6 = Rectangle(Point(2*int(width/3)+1,int(height/3)+1), Point((width),2*int(height/3)))
    print("box6 " + str(box6.topLeft.x) + "," + str(box6.topLeft.y) + ";" + str(box6.bottomRight.x) + "," + str(box6.bottomRight.y))
    box7 = Rectangle(Point(0,2*int(height/3)+1), Point(int(width/3),height))
    print("box7 " + str(box7.topLeft.x) + "," + str(box7.topLeft.y) + ";" + str(box7.bottomRight.x) + "," + str(box7.bottomRight.y))
    box8 = Rectangle(Point(int(width/3)+1,2*int(height/3)+1), Point(2*int(width/3),height))
    print("box8 " + str(box8.topLeft.x) + "," + str(box8.topLeft.y) + ";" + str(box8.bottomRight.x) + "," + str(box8.bottomRight.y))
    box9 = Rectangle(Point(2*int(width/3)+1,2*int(height/3)+1), Point(width,height))
    print("box9 " + str(box9.topLeft.x) + "," + str(box9.topLeft.y) + ";" + str(box9.bottomRight.x) + "," + str(box9.bottomRight.y))
    #create list of boxes
    boxlist = []
    boxlist.extend((box1,box2,box3,box4,box5,box6,box7,box8,box9))
    #Set status of nine captchas to false
    box1, box2, box3, box4, box5, box6, box7, box8, box9 = False,False,False,False,False,False,False,False,False
    boxbool = []
    boxbool.extend((box1,box2,box3,box4,box5,box6,box7,box8,box9))
elif captchatype == '4x4':
    #Set up 4x4 grid of captcha squares
    #1   2   3   4
    #5   6   7   8 
    #9  10  11  12
    #13 14  15  16  
    box1 = Rectangle(Point(0,0), Point(int(width/4),int(height/4)))
    print("box1 " + str(box1.topLeft.x) + " " + str(box1.topLeft.y) + ";" + str(box1.bottomRight.x) + "," + str(box1.bottomRight.y))
    box2 = Rectangle(Point(int(width/4)+1,0), Point(2*int(width/4),int(width/4)))
    print("box2 " + str(box2.topLeft.x) + "," + str(box2.topLeft.y) + ";" + str(box2.bottomRight.x) + "," + str(box2.bottomRight.y))
    box3 = Rectangle(Point(2*int(width/4)+1,0), Point(3*int(width/4),int(height/4)))
    print("box3 " + str(box3.topLeft.x) + "," + str(box3.topLeft.y) + ";" + str(box3.bottomRight.x) + "," + str(box3.bottomRight.y))
    box4 = Rectangle(Point(3*int(width/4)+1,0), Point(width,int(height/4)))
    print("box4 " + str(box4.topLeft.x) + "," + str(box4.topLeft.y) + ";" + str(box4.bottomRight.x) + "," + str(box4.bottomRight.y))
    box5 = Rectangle(Point(0,int(height/4)+1), Point(int(width/4),2*int(height/4)))
    print("box5 " + str(box5.topLeft.x) + "," + str(box5.topLeft.y) + ";" + str(box5.bottomRight.x) + "," + str(box5.bottomRight.y))
    box6 = Rectangle(Point(int(width/4)+1,int(height/4)+1), Point(2*int(width/4),2*int(height/4)))
    print("box6 " + str(box6.topLeft.x) + "," + str(box6.topLeft.y) + ";" + str(box6.bottomRight.x) + "," + str(box6.bottomRight.y))
    box7 = Rectangle(Point(2*int(width/4)+1,int(height/4)+1), Point(3*int(width/4),2*int(height/4)))
    print("box7 " + str(box7.topLeft.x) + "," + str(box7.topLeft.y) + ";" + str(box7.bottomRight.x) + "," + str(box7.bottomRight.y))
    box8 = Rectangle(Point(3*int(width/4)+1,int(height/4)+1), Point((width),2*int(height/4)))
    print("box8 " + str(box8.topLeft.x) + "," + str(box8.topLeft.y) + ";" + str(box8.bottomRight.x) + "," + str(box8.bottomRight.y))
    box9 = Rectangle(Point(0,2*int(height/4)+1), Point(int(width/4),3*int(height/4)))
    print("box9 " + str(box9.topLeft.x) + "," + str(box9.topLeft.y) + ";" + str(box9.bottomRight.x) + "," + str(box9.bottomRight.y))
    box10 = Rectangle(Point(int(width/4)+1,2*int(height/4)+1), Point(2*int(width/4),3*int(height/4)))
    print("box10 " + str(box10.topLeft.x) + "," + str(box10.topLeft.y) + ";" + str(box10.bottomRight.x) + "," + str(box10.bottomRight.y))
    box11 = Rectangle(Point(2*int(width/4)+1,2*int(height/4)+1), Point(3*int(width/4),3*int(height/4)))
    print("box11 " + str(box11.topLeft.x) + "," + str(box11.topLeft.y) + ";" + str(box11.bottomRight.x) + "," + str(box11.bottomRight.y))
    box12 = Rectangle(Point(3*int(width/4)+1,2*int(height/4)+1), Point((width),3*int(height/4)))
    print("box12 " + str(box12.topLeft.x) + "," + str(box12.topLeft.y) + ";" + str(box12.bottomRight.x) + "," + str(box12.bottomRight.y))
    box13 = Rectangle(Point(0,3*int(height/4)+1), Point(int(width/4),height))
    print("box13 " + str(box13.topLeft.x) + "," + str(box13.topLeft.y) + ";" + str(box13.bottomRight.x) + "," + str(box13.bottomRight.y))
    box14 = Rectangle(Point(int(width/4)+1,3*int(height/4)+1), Point(2*int(width/4),height))
    print("box14 " + str(box14.topLeft.x) + "," + str(box14.topLeft.y) + ";" + str(box14.bottomRight.x) + "," + str(box14.bottomRight.y))
    box15 = Rectangle(Point(2*int(width/4)+1,3*int(height/4)+1), Point(3*int(width/4),height))
    print("box15 " + str(box15.topLeft.x) + "," + str(box15.topLeft.y) + ";" + str(box15.bottomRight.x) + "," + str(box15.bottomRight.y))
    box16 = Rectangle(Point(3*int(width/4)+1,3*int(height/4)+1), Point((width),height))
    print("box16 " + str(box16.topLeft.x) + "," + str(box16.topLeft.y) + ";" + str(box16.bottomRight.x) + "," + str(box16.bottomRight.y))
    #create list of boxes
    boxlist = []
    boxlist.extend((box1,box2,box3,box4,box5,box6,box7,box8,box9,box10,box11,box12,box13,box14,box15,box16))
    #Set status of nine captchas to false
    box1, box2, box3, box4, box5, box6, box7, box8, box9, box10, box11, box12, box13, box14, box15, box16 = False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False
    boxbool = []
    boxbool.extend((box1,box2,box3,box4,box5,box6,box7,box8,box9,box10,box11,box12,box13,box14,box15,box16))
elif captchatype == '2x4':
    sys.exit('2x4 captchas are not yet implemented')

if (captchaclass == 'car' or captchaclass == 'vehicle'):
    #load model for cars
    MODEL_NAME = 'object_detection/inference_graph_car'
    PATH_TO_LABELS = os.path.join('object_detection/inference_graph_car', 'car-detection.pbtxt')
elif (captchaclass == 'bus'):
    #load model for buses
    MODEL_NAME = 'object_detection/inference_graph_bus'
    PATH_TO_LABELS = os.path.join('object_detection/inference_graph_bus', 'bus-detection.pbtxt')
elif (captchaclass == "hydrant"):
    #load model for hydrants
    MODEL_NAME = 'object_detection/inference_graph_hydrant'
    PATH_TO_LABELS = os.path.join('object_detection/inference_graph_hydrant', 'hydrant-detection.pbtxt')
elif (captchaclass == "light"):
    #load model for stoplights
    MODEL_NAME = 'object_detection/inference_graph_stoplight'
    PATH_TO_LABELS = os.path.join('object_detection/inference_graph_stoplight', 'stoplight-detection.pbtxt')
elif (captchaclass == "bicycle"):
    #load model for bicycles
    MODEL_NAME = 'object_detection/inference_graph_bicycle'
    PATH_TO_LABELS = os.path.join('object_detection/inference_graph_bicycle', 'bicycle-detection.pbtxt') 

PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

NUM_CLASSES = 1

#load pretrained model for captchas
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

#load map of image classes
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

#class to load images
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

#actual detection of captchas
with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        image = Image.open("finalimage.png")
        image_np = load_image_into_numpy_array(image)
        image_np_expanded = np.expand_dims(image_np, axis=0)
        (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})
        width, height = image.size
        newbox = np.squeeze(boxes)
        finalboxes = newbox[~(newbox==0).all(1)]
        numboxes = len(finalboxes)
        draw = ImageDraw.Draw(final_image)
        for x in range(0,numboxes):
            ymin = boxes[0][x][0]*height
            xmin = boxes[0][x][1]*width
            ymax = boxes[0][x][2]*height
            xmax = boxes[0][x][3]*width
            print("Box " + str(x))
            print('Top left')
            print (xmin,ymin)
            print('Bottom right')
            print (xmax,ymax)
            print(" ")
            draw.rectangle(((xmin,ymin),(xmax,ymax)), fill="blue") 
            detectedbox = Rectangle(Point(xmin,ymin),Point(xmax,ymax))
            for x in range(len(boxlist)):
                if intersect(boxlist[x],detectedbox):
                    boxbool[x] = True
            
            final_image.save("detections.png")
            print(*boxbool, sep='\n')
        f = open('final.pckl', 'wb')
        pickle.dump(boxbool, f)
        f.close()
            
