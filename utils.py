import os
import cv2
import mtcnn
from numpy.lib.shape_base import column_stack
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as matimg
from facenet_pytorch import MTCNN
from PIL import Image

def get_images_paths(folder_address, extensions=['.jpg', '.png']):
    """
    Walks through a given directory, finds all images
    in any folder and subfolder and returns the list of
    paths of images.
    """
    paths = []
    for root, _, files in os.walk(folder_address):
        for f in files:
            for extension in extensions:
                if f.endswith(extension):
                    paths.append(os.path.join(root, f))
                    break
    return paths
class Detection:
    """
    A module for detecting the bounding box
    position of faces in images.
    """

    def __init__(self):
        pass

    def detect_faces(self, paths):
        batches = self.make_batches(paths)
        faces = self.find_bounding_boxes(batches)
        df = pd.DataFrame(faces, columns=['image_path', 'x_from_per', 'y_from_per', 'x_to_per', 'y_to_per'])
        df.to_csv('bounding_boxes.csv', index=False)
        return faces

    def make_batches(self, paths):
        # TODO: Better batching imporoves performance
        batches = [[path] for path in paths]
        return batches

    def find_bounding_boxes(self, batches, thresh=0.95):
        # detector = mtcnn.MTCNN()
        detector = MTCNN()
        detected_faces = []
        for paths in batches:
            size = None
            imgs = []
            for path in paths:
                img = cv2.imread(path)[:, :, ::-1]
                if size == None:
                    size = self.get_new_size(img.shape[1], img.shape[0])
                img = cv2.resize(img, size)
                imgs.append(img)
            bboxes_imgs, probs = detector.detect(imgs)
            for idx, (bbox_img, prob) in enumerate(zip(bboxes_imgs, probs)):
                for i in range(len(bbox_img)):
                    if prob[i] > thresh:
                        x_from = int(bbox_img[i][0] * 100 / size[0])
                        x_to = int(bbox_img[i][2] * 100 / size[0])
                        y_from = int(bbox_img[i][1] * 100 / size[1])
                        y_to = int(bbox_img[i][3] * 100 / size[1])
                        detected_faces.append((paths[idx], x_from, y_from, x_to, y_to))
        return detected_faces

    def get_new_size(self, width, height):
        w = int((width / height) * 720)
        h = 720
        return w, h

paths = get_images_paths('.\\data')
d = Detection()
d.detect_faces(paths)
