import argparse
import numpy as np
from clustering import ThresholdClustering

def main(features_path):
    features = np.load(features_path)
    tc = ThresholdClustering()
    clusters = tc.run(features, talk=True)
    print(clusters)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='How to evaluate threshold clustering algorithm')
    parser.add_argument('path', help='Path of .npy file containing feature vectors/')
    args = parser.parse_args()
    
    features_path = args.path
    main(features_path)
