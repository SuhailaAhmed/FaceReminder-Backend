import glob
import os

# import seaborn as sns
import time
from os import listdir, makedirs

import cv2
import deepface
import numpy as np
import pandas as pd

# import matplotlib.pylab as plt
# from google.colab import drive
import PIL
from deepface import DeepFace
from pandas.core.series import Series
from PIL import Image


class Face_reconition_model:
    """
    A class for face recognition using deepface
    All deepface functions can take model type and backends "Face detector" as arguments, The default is VGG-Face model and opencv detector
    Here we used Facenet model in recognition, and mtcnn in face detection

    Attributes:
      models: A list of the available models to be used in Deepface library
      backends: A list of the available backends to be used in Deepface library

    Methods:
      verify_face: verifies if the two images are matched

          Args:
              image1_path: A string path for the image to be verified
              image2_path: A string path for the image to be matched with

          Returns:
              is_verified: A boolean value saying is it verified or not,
                           It is orginally a part of a dictionary of whether its verified or not, threshold of the detector, .. etc
                           But we only return a boolean value saying is it verified or not


      recognize_face: Recognizes a face in comparasion to a stored folder

          Args:
              image_path: A string path for the image to be recognized
              folder_path: A string path for the folder where the other images are stored to be matched with

          Returns:
            is_recongnized: A string path to the matching image found in a folder,
                            It is orginally a part of a dataframe, we are only interested in the path value
                            If no match is found, "Null" is returned

    """

    def __init__(self):
        # Models and detectors used in deepface functions
        self.models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace"]
        self.backends = ["mediapipe", "ssd", "dlib", "mtcnn", "retinaface"]

    # 3-1
    def verify_face(self, image1_path, image2_path):
        is_verified = DeepFace.verify(
            image1_path, image2_path, detector_backend=self.backends[3], model_name=self.models[2], distance_metric="cosine"
        )
        is_verified = is_verified["verified"]  # use mtcnn, also use openface model
        return is_verified

    def recognize_face(self, image_path, folder_path):
        is_recongnized = DeepFace.find(
            image_path, folder_path, detector_backend=self.backends[4], enforce_detection=False, model_name=self.models[2]
        )

        if np.size(is_recongnized):
            is_recongnized = pd.DataFrame(is_recongnized[0])
        else:
            is_recongnized = None
        return is_recongnized


def recognized(im, folder):
    model = Face_reconition_model()
    rec = model.recognize_face(im, folder)
    if rec is None:
        return rec
    df_columns = ["identity", "das", "ww", "ee", "eae", "rr"]
    df = pd.DataFrame(rec, columns=df_columns)

    return df["identity"][0]
