import os
import cv2
import pandas as pd
from time import time
from facenet_pytorch import MTCNN

class Detection:
    """
    A module for detecting the bounding box
    position of faces in images.
    """

    def __init__(self, csv_files, save_folder, preferred_batch_size, default_height=720, one_face=False, device='gpu'):
        """
        Initialize a detection object with given settings.
        """
        self.save_folder = save_folder
        self.one_face = one_face
        self.csv_files = csv_files
        self.preferred_batch_size = preferred_batch_size
        self.detector = MTCNN(select_largest=False, device=device)
        self.current_split = 1
        self.H = default_height

        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        self.total_images = 0
        for csv_file in csv_files:
            self.total_images += int(csv_file.split('_')[-2])

        print('-----------------------')
        print('Face detection phase has begun...\n')

    def detect_faces(self, thresh=0.99):
        """
        Go through all csv files containing image paths and ratio groups.
        Detect faces in all images and write to csv files.
        """
        result = []
        processed_images = 0
        start = time()
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
                    img = cv2.imread(path['path'])[:, :, ::-1]
                    if size == None:
                        size = self.get_new_size(path['ratio_group'])
                    img = cv2.resize(img, size)
                    # img = Image.fromarray(img)
                    imgs.append(img)

                # detect faces in image batch and save in a list
                bboxes_imgs, probs = self.detector.detect(imgs)

                for idx, (bbox_img, prob) in enumerate(zip(bboxes_imgs, probs)):

                    if bbox_img is None:
                        continue
                    if self.one_face:
                        bbox_img = bbox_img[:1]
                    else:
                        bbox_img = bbox_img[prob >= thresh]
                    for i in range(len(bbox_img)):
                        x_from = int(bbox_img[i][0] * 100 / size[0])
                        x_to = int(bbox_img[i][2] * 100 / size[0])
                        y_from = int(bbox_img[i][1] * 100 / size[1])
                        y_to = int(bbox_img[i][3] * 100 / size[1])
                        detected_faces.append((image_paths.iloc[position+idx]['path'], x_from, y_from, x_to, y_to))
                
                position += batch_size
                processed_images += batch_size
                duration = time() - start
                print('Processed {} / {} images ({:.2f} seconds) ({:.2f} it/sec)'.format(processed_images, self.total_images, duration, batch_size / duration))
                start = time()

            result.append(self.save_in_csv(detected_faces))
        
        print('Face detection phase has finished')
        print('-----------------------')
        return result

    def save_in_csv(self, faces):
        """
        Saves a batch of paths in one csv file.
        """
        df = pd.DataFrame(faces, columns=['image_path', 'x_from_per', 'y_from_per', 'x_to_per', 'y_to_per'])
        save_path = os.path.join(self.save_folder, 'bounding_boxes_{}_{}_.csv'.format(self.current_split, len(df)))
        df.to_csv(save_path, index=False)
        self.current_split += 1
        return save_path

    def get_new_size(self, rg):
        """
        Determine the size of image according to its ratio group.
        """
        h = self.H
        w = 0
        if rg == -3:
            w = int(h * 0.5)
        elif rg == -2:
            w = int(h * 0.62)
        elif rg == -1:
            w = int(h * 0.83)
        elif rg == 1:
            w = int(h * 1.2)
        elif rg == 2:
            w = int(h * 1.6)
        else:
            w = int(h * 2)
        return w, h
