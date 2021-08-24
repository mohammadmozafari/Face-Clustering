import torch
import argparse
from utils.feature_extraction import FeatureExtractor

def main(images, save_folder):
    device = torch.device('cuda:0')
    fe = FeatureExtractor([images], save_folder, device, batch_size=64, margin=0)
    paths = fe.extract_features(num_workers=2)
    print(paths)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Feature Extraction')
    parser.add_argument('--images', help='CSV file containing bounding boxes')
    parser.add_argument('--save_folder', help='Folder to save features')
    args = parser.parse_args()
    main(args.images, args.save_folder)
    # lfw_prepare_pairs()
    # check_mistakes()
    # evaluate_on_lfw()
