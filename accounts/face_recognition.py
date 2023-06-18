from deepface import DeepFace
import cv2
import os
from os import listdir,makedirs
import numpy as np
import pandas as pd
from PIL import Image

"""Importing dataset"""

data_path = 'path_of_folder'

"""Preprocessing dataset"""

f = data_path
os.listdir(f)

# Resizing images into 512*512

for file in os.listdir(f):
    f_img = f+"/"+file
    img = Image.open(f_img)
    img = img.resize((512,512))
    img.save(f_img)


# Convert to gray scale image

path = data_path # Source Folder
path_folders = path.parse('/')
last_folder = path_folders.pop() 
last_folder += '_gray' 
path_folders.append(last_folder) 
dstpath = '/'.join(path_folders) # Destination folder

try:
    makedirs(dstpath)
except:
    print ("Directory already exist, images will be written in asme folder")

# Folder won't used

files = os.listdir(path)

for image in files:
    img = cv2.imread(os.path.join(path,image))
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(dstpath,image),gray)

""" Face recognition class """

class Face_reconition_model():
  
  def __init__(self):
    # Models and detectors used in deepface functions
    self.models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
    self.backends = ['mediapipe', 'ssd', 'dlib', 'mtcnn', 'retinaface']

  def verify_face(self, image1_path, image2_path):
    is_verified = DeepFace.verify( image1_path, image2_path, detector_backend =self.backends[3] ,model_name= self.models[2], distance_metric='cosine')
    is_verified = is_verified["verified"] #use mtcnn, also use openface model
    return is_verified

  def recognize_face(self, image_path,folder_path):
    is_recongnized = DeepFace.find(image_path, folder_path, detector_backend =self.backends[4],enforce_detection=False,model_name= self.models[2]) 
    if(np.size(is_recongnized)):
      is_recongnized = is_recongnized[:][0]
    else:
      is_recongnized = "Null"
    return is_recongnized

def recognized(im,folder):
  model=Face_reconition_model()
  rec= model.recognize_face(im,folder)
  df=pd.DataFrame(rec)
  return df['identity'][0]

image_path = ''

im= cv2.imread(image_path)
im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im = cv2.resize(im, (512,512), interpolation = cv2.INTER_AREA)
filename = 'Preprocessed.jpg'
cv2.imwrite(filename,im)

im="/Preprocessed.jpg"
fpath=dstpath
recognized(im,fpath)
