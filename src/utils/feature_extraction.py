import os
import time
import torch
import numpy as np
import pandas as pd
from torch.utils.data import DataLoader
from src.utils.datasets import FaceDataset
from src.utils.inception_resnet_v1 import InceptionResnetV1

class FeatureExtractor:

    def __init__(self, csv_files, result_folder, device, batch_size=64):
        """
        Initialize a feature extractor.
        """
        self.total_images = 0
        self.current_split = 1
        self.device = device
        self.batch_size = batch_size
        self.result_folder = result_folder
        self.csv_files = csv_files
        self.net = InceptionResnetV1(pretrained='vggface2', device=device).eval()
        for csv_file in csv_files:
            self.total_images += int(csv_file.split('_')[-2])
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)

    def extract_features(self):
        """
        Goes through all csv files and get face images.
        Extracts featuers from these faces and saves them in csv files.
        """
        counter = 0
        result = []
        tick = time.time()
        begin = time.time()
        with torch.no_grad():
            for csv_file in self.csv_files:
                ds = FaceDataset(csv_file)
                dl = DataLoader(ds, shuffle=False, batch_size=self.batch_size)
                embeddings = np.zeros((len(ds), 512))
                at = 0
                for faces in dl:
                    faces = faces.to(self.device)
                    vecs = self.net(faces)
                    bsize = vecs.shape[0]
                    embeddings[at:at+bsize, :] = vecs.cpu()
                    at += bsize
                    counter += bsize
                    tock = time.time()
                    print('Processed {}/{} faces. ({:.2f} faces per second)'.format(counter, self.total_images, bsize/(tock-tick)))
                    tick = time.time()
                result.append(self.save_to_csv(embeddings))
        end = time.time()
        print()
        print('Average speed: {:.2f} faces per second'.format(self.total_images/(end-begin)))
        print('Feature extraction phase has finished.')
        print('-----------------------')
        return result

    def save_to_csv(self, embeddings):
        """
        Converts given numpy array to pandas
        dataframe and saves it in a csv file.
        """
        df = pd.DataFrame(embeddings, columns=range(512))
        save_path = os.path.join(self.result_folder, 'features_{}_{}_.csv'.format(self.current_split, len(df)))
        df.to_csv(save_path, index=False)
        self.current_split += 1
        return save_path