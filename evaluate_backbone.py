import os
import sys
import torch
from src.utils.feature_extraction import FeatureExtractor

def extract_features():
    bbox_csv_folder = sys.argv[1]
    destination_folder = sys.argv[2]
    device = torch.device('cuda:0')
    bbox_csvs = os.listdir(bbox_csv_folder)
    bbox_csvs = [os.path.join(bbox_csv_folder, bbox_csv) for bbox_csv in bbox_csvs]
    fe = FeatureExtractor(bbox_csvs, destination_folder, device, batch_size=64)
    paths = fe.extract_features()
    return paths

def evaluate_results():
    pairs_files = './data/pairs.txt'
    with open(pairs_files) as f:
        lines = f.readlines()
        for line in lines:
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
            

# extract_features()
evaluate_results()
