import cv2
import pandas as pd
from tqdm import tqdm
from facenet_pytorch import MTCNN

class Detection:
    """
    A module for detecting the bounding box
    position of faces in images.
    """

    def __init__(self, save_path, one_face=False):
        self.save_path = save_path
        self.one_face = one_face
        pass

    def detect_faces(self, paths):
        batches = self.make_batches(paths)
        faces = self.find_bounding_boxes(batches)
        df = pd.DataFrame(faces, columns=['image_path', 'x_from_per', 'y_from_per', 'x_to_per', 'y_to_per'])
        df.to_csv(self.save_path, index=False)
        return faces

    def make_batches(self, paths):
        # TODO: Better batching imporoves performance
        batches = [[path] for path in paths]
        return batches

    def find_bounding_boxes(self, batches, thresh=0.95):
        # detector = mtcnn.MTCNN()
        detector = MTCNN()
        detected_faces = []
        for paths in tqdm(batches):
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
                    if self.one_face:
                        break
        return detected_faces

    def get_new_size(self, width, height):
        w = int((width / height) * 720)
        h = 720
        return w, h
