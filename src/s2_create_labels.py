import os
import cv2
import time
import argparse
import numpy as np
import pandas as pd
from facenet_pytorch import MTCNN
from detection import MTCNNDetection
from visualization import show_images


def main(bboxes, save_folder):
    clusters = {}
    last_id = -1
    df = pd.read_csv(bboxes)
    labels = np.zeros(len(df))
    for i, row in df.iterrows():
        cluster_name = row['image_path'].split('\\')[1]
        if cluster_name not in clusters:
            clusters[cluster_name] = last_id + 1
            last_id += 1
        labels[i] = clusters[cluster_name]
        print('{}/{} labeled.'.format(i+1, len(df)))
    path = os.path.join(save_folder, 'labels_{}_.npy'.format(len(df)))
    np.save(path, labels)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Face detection')
    parser.add_argument('--bboxes', help='CSV file containing bounding boxes')
    parser.add_argument('--save_folder', help='Where to save labels')
    args = parser.parse_args()
    main(args.bboxes, args.save_folder)
