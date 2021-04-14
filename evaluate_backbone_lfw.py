import os
import sys
import cv2
import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.visualization import show_images
from src.utils.datasets import FaceDataset
from src.utils.feature_extraction import FeatureExtractor

def extract_features():
    """
    Goes through all faces (bounding boxes are ready from before)
    and passes each face to a neural network to find an embedding for it.
    """
    bbox_csv_folder = './results/lfw-bboxes'
    destination_folder = './results/lfw-features'
    device = torch.device('cuda:0')
    bbox_csvs = os.listdir(bbox_csv_folder)
    bbox_csvs = [os.path.join(bbox_csv_folder, bbox_csv) for bbox_csv in bbox_csvs]
    fe = FeatureExtractor(bbox_csvs, destination_folder, device, batch_size=64, margin=0)
    paths = fe.extract_features(num_workers=0)
    return paths

def build_data():
    """
    LFW dataset has a pair dataset for testing.
    This function converts that pair dataset
    to a more suitable form for our program
    """
    pairs_files = './data/pairs.txt'
    pairs_csv_file = './results/pairs.csv'
    paths = './results/lfw-paths/paths_1_13233_.csv'
    df = pd.read_csv(paths)
    pairs = []
    print('Building tuples for evaluation ...')
    with open(pairs_files) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0: continue
            parts = line.split()
            target, name1, name2 = None, None, None
            if len(parts) == 3:
                target = 1
                name1 = '{}_{:0>4d}.jpg'.format(parts[0], int(parts[1]))
                name2 = '{}_{:0>4d}.jpg'.format(parts[0], int(parts[2]))
            elif len(parts) == 4:
                target = 0
                name1 = '{}_{:0>4d}.jpg'.format(parts[0], int(parts[1]))
                name2 = '{}_{:0>4d}.jpg'.format(parts[2], int(parts[3]))
            
            idx1 = df[df['path'].str.contains('\{}'.format(name1), regex=False)].index.values[0]
            idx2 = df[df['path'].str.contains('\{}'.format(name2), regex=False)].index.values[0]
            pairs.append((idx1, idx2, target))
            print('Pair {}/{} done.'.format(i, len(lines)-1))
        df = pd.DataFrame(pairs, columns=['first', 'second', 'target'])
        df.to_csv(pairs_csv_file, index=False)
    print('-----------------------')
    return pairs_csv_file

def check_mistakes(pairs_csv_file):
    """
    It's important to know why mistakes have happened.
    This function shows pairs of images that are falsely classified.
    """
    bboxes = './results/lfw-bboxes/bounding_boxes_1_13233_.csv'
    features = './results/lfw-features/features_1_13233_.csv'
    features = pd.read_csv(features).values
    data = pd.read_csv(pairs_csv_file).values

    first = features[data[:, 0]]
    second = features[data[:, 1]]
    labels = data[:, 2]

    diff = np.linalg.norm(first - second, axis=1)
    preds = (diff < 1.1) * 1
    mistakes = np.where(preds != labels)[0]
    
    print('Accuracy =', np.mean(preds == labels))
    print('Number of mistakes =', mistakes.shape[0])
    fds = FaceDataset(bboxes, talk=True)
    for i, mistake in enumerate(mistakes):
        face1, path1 = fds.__getitem__(data[mistake, 0])
        face2, path2 = fds.__getitem__(data[mistake, 1])
        print()
        print('Pair', i+1)
        print(path1)
        print(path2)
        print('Target =', labels[mistake])
        print('Predicted =', preds[mistake])
        face1 = (face1.transpose((1, 2, 0)) * 255).astype('int')
        face2 = (face2.transpose((1, 2, 0)) * 255).astype('int')
        img1 = cv2.imread(path1)[:, :, ::-1]
        img1 = cv2.resize(img1, (112, 112))
        img2 = cv2.imread(path2)[:, :, ::-1]
        img2 = cv2.resize(img2, (112, 112))
        show_images([face1, face2, img1, img2])

if __name__ == "__main__":
    extract_features()
    # data = build_data()
    check_mistakes('./results/pairs.csv')
