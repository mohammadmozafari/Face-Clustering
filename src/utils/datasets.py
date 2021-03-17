import cv2
import pandas as pd
import matplotlib.pyplot as plt
from torch.utils.data import Dataset

class BatchMaker():

    def __init__(self, csv_files):
        self.length = 0
        self.csv_files = csv_files
        self.current_file = 1
        for file in csv_files:
            self.length += int(file.split('_')[-2])

    def __len__(self):
        return self.length

    def __getitem__(self, index):
        
        

class FaceDataset(Dataset):
    """
    A class for iterating over all faces
    specified in a csv file.
    The path of csv file is passed to the constructor. 
    """

    def __init__(self, csv_file):
        """
        Initialize dataset by reading a given csv file.
        This file is supposed to contain the bounding box
        of faces in images.
        """
        self.df = pd.read_csv(csv_file)

    def __len__(self):
        """
        Total number of faces specified in the csv file.
        """
        return len(self.df)

    # TODO: transfer to gpu for faster result
    def __getitem__(self, index):
        """
        Open image of the given index and crop the face part
        according to the bounding box coordinates.
        """
        face = self.df.iloc[index]
        path = face['image_path']
        img = cv2.imread(path)[:, :, ::-1]
        x_from = face['x_from_per'] * img.shape[1] // 100
        x_to = face['x_to_per'] * img.shape[1] // 100
        y_from = face['y_from_per'] * img.shape[0] // 100
        y_to = face['y_to_per'] * img.shape[0] // 100
        face = img[y_from:y_to, x_from:x_to, :]
        face = cv2.resize(face, (112, 112))
        face = face.transpose((2, 0, 1))
        face = (face / 255).astype('float32')
        return face
