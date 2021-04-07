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

extract_features()