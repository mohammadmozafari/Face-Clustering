import os
import cv2
import pandas as pd
from time import time
from facenet_pytorch import MTCNN
from torch.utils.data import DataLoader
from src.utils.datasets import ImageDataset

class Detection:
    """
    A module for detecting the bounding box
    position of faces in images.
    """

    def __init__(self, csv_files, save_folder, batch_size, size, one_face=False, device='cpu', mode='prob', same=False):
        """
        Initialize a detection object with given settings.
        """
        self.save_folder = save_folder
        self.one_face = one_face
        self.csv_files = csv_files
        self.batch_size = batch_size
        self.current_split = 1
        self.detector = None
        self.size = size
        self.same = same
        self.mode = mode

        if mode == 'prob' or mode == 'center':
            self.detector = MTCNN(select_largest=False, device=device)
        elif mode == 'size':
            self.detector = MTCNN(select_largest=True, device=device)

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
        total_start = time()
        detected_faces = []
        
        for csv_file in self.csv_files:
            ids = ImageDataset(csv_file, size=self.size, same=self.same)
            ldr = DataLoader(ids, batch_size=self.batch_size, shuffle=False, num_workers=2)
            for imgs, paths, hs, ws in ldr:
                imgs = imgs.numpy()
                imgs = [imgs[i, :, :, :] for i in range(imgs.shape[0])]
                size = imgs[0].shape[0], imgs[0].shape[1]
                bboxes_imgs, probs = self.detector.detect(imgs)
                for idx, (bbox_img, prob) in enumerate(zip(bboxes_imgs, probs)):
                    if bbox_img is None:
                        continue
                    if self.one_face:
                        bbox_img = self.select_box(bbox_img)
                    else:
                        bbox_img = bbox_img[prob >= thresh]
                    for j in range(len(bbox_img)):
                        x_from = int((bbox_img[j][0] - (size[1] - ws[idx])/2) * 100 / ws[idx])
                        x_to = int((bbox_img[j][2] - (size[1] - ws[idx])/2) * 100 / ws[idx])
                        y_from = int((bbox_img[j][1] - (size[0] - hs[idx])/2) * 100 / hs[idx])
                        y_to = int((bbox_img[j][3] - (size[0] - hs[idx])/2) * 100 / hs[idx])
                        detected_faces.append((paths[idx], x_from, y_from, x_to, y_to))
                processed_images += len(imgs)
                duration = time() - start
                print('Processed {} / {} images ({:.2f} seconds) ({:.2f} it/sec)'.format(processed_images, self.total_images, duration, len(imgs) / duration))
                start = time()
            result.append(self.save_in_csv(detected_faces))

        total_end = time()
        print('Face detection phase has finished')
        print('It took {:.2f} seconds to detect all faces.'.format(total_end - total_start))
        print('-----------------------')
        return result

    def select_box(self, bbox_img):
        if self.mode == 'prob' or self.mode == 'size':
            return bbox_img[0:1]
        middle_x = int(self.size[1] / 2)
        middle_y = int(self.size[0] / 2)
        box_middle_x = ((bbox_img[:, 2] + bbox_img[:, 0]) / 2).astype(int)
        box_middle_y = ((bbox_img[:, 3] + bbox_img[:, 1]) / 2).astype(int)
        min_dist, bbox = -1, None
        for i in range(bbox_img.shape[0]):
            dist = (middle_x-box_middle_x[i]) ** 2 + (middle_y-box_middle_y[i]) ** 2
            if dist < min_dist or min_dist == -1:
                min_dist = dist
                bbox = bbox_img[i:i+1, :]
        return bbox

    def save_in_csv(self, faces):
        """
        Saves a batch of paths in one csv file.
        """
        df = pd.DataFrame(faces, columns=['image_path', 'x_from_per', 'y_from_per', 'x_to_per', 'y_to_per'])
        save_path = os.path.join(self.save_folder, 'bounding_boxes_{}_{}_.csv'.format(self.current_split, len(df)))
        df.to_csv(save_path, index=False)
        self.current_split += 1
        return save_path
