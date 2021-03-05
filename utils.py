import os
import cv2
import mtcnn
import matplotlib.pyplot as plt
import matplotlib.image as matimg
from facenet_pytorch import MTCNN
from PIL import Image

def get_images_paths(folder_address, extensions=['.jpg', '.png']):
    paths = []
    for root, _, files in os.walk(folder_address):
        for f in files:
            for extension in extensions:
                if f.endswith(extension):
                    paths.append(os.path.join(root, f))
                    break
    return paths

class Detection:

    def __init__(self, paths):
        self.paths = paths

    def detect_faces(self):
        batches = self.make_batches()
        faces = self.find_bounding_boxes(batches)

        for img, a, b, c, d in faces:
            print(img, ':', a, b, c, d)
        # print(faces)

    def make_batches(self):
        # TODO: Better batching imporoves performance
        batches = [[path] for path in self.paths]
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
                        detected_faces.append(
                            (paths[idx], bbox_img[i][0]/size[0], bbox_img[i][1]/size[1], bbox_img[i][2]/size[0], bbox_img[i][3]/size[1]))
        return detected_faces

    def get_new_size(self, width, height):
        w = int((width / height) * 720)
        h = 720
        return w, h

paths = get_images_paths('./data')
d = Detection(paths)
d.detect_faces()
