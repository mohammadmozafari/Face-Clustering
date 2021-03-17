import os
import cv2
import pandas as pd
from tqdm import tqdm
from facenet_pytorch import MTCNN

class Detection:
    """
    A module for detecting the bounding box
    position of faces in images.
    """

    def __init__(self, csv_files, save_folder, preferred_batch_size, one_face=False):
        """
        Initialize a detection object with given settings.
        """
        self.save_folder = save_folder
        self.one_face = one_face
        self.csv_files = csv_files
        self.preferred_batch_size = preferred_batch_size
        self.detector = MTCNN()
        self.current_split = 1
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

    def detect_faces(self, thresh=0.95):
        """
        Go through all csv files containing image paths and ratio groups.
        Detect faces in all images and write to csv files.
        """
        for csv_file in self.csv_files:
            image_paths = pd.read_csv(csv_file)
            detected_faces = []
            position = 0
            while position < len(image_paths):
                
                # determine batch size
                batch_size = self.preferred_batch_size
                while (position + batch_size) > len(image_paths):
                    batch_size -= 1
                while (image_paths.iloc[position + batch_size - 1]['ratio_group'] != image_paths.iloc[position]['ratio_group']):
                    batch_size -= 1

                # read a batch of images and resize them
                imgs = []
                size = None
                for idx, path in image_paths.iloc[position:position+batch_size].iterrows():
                    print(path)
                    img = cv2.imread(path['path'])[:, :, ::-1]
                    if size == None:
                        size = self.get_new_size(path['ratio_group'])
                    img = cv2.resize(img, size)
                    imgs.append(img)

                # detect faces in image batch and save in a list
                bboxes_imgs, probs = self.detector.detect(imgs)
                for idx, (bbox_img, prob) in enumerate(zip(bboxes_imgs, probs)):
                    for i in range(len(bbox_img)):
                        if prob[i] > thresh:
                            x_from = int(bbox_img[i][0] * 100 / size[0])
                            x_to = int(bbox_img[i][2] * 100 / size[0])
                            y_from = int(bbox_img[i][1] * 100 / size[1])
                            y_to = int(bbox_img[i][3] * 100 / size[1])
                            detected_faces.append((image_paths.iloc[position+idx]['path'], x_from, y_from, x_to, y_to))
                        if self.one_face:
                            break
                position += batch_size

            self.save_in_csv(detected_faces)

    def save_in_csv(self, faces):
        """
        Saves a batch of paths in one csv file.
        """
        df = pd.DataFrame(faces, columns=['image_path', 'x_from_per', 'y_from_per', 'x_to_per', 'y_to_per'])
        df.to_csv(os.path.join(self.save_folder, 'bounding_boxes_{}_{}_.csv'.format(self.current_split, len(df))), index=False)
        self.current_split += 1

    def get_new_size(self, rg):
        """
        Determine the size of image according to its ratio group.
        """
        h = 720
        w = 0
        if rg == -3:
            w = 257
        elif rg == -2:
            w = 324
        elif rg == -1:
            w = 550
        elif rg == 1:
            w = 1000
        elif rg == 2:
            w = 1728
        else:
            w = 2020
        return w, h
