import time
import argparse
import numpy as np
from clustering.knn_graph import build_knn_graph

def main(feat_path, k, alg, out_path):
    features = np.load(feat_path)
    if k is None:
        k = min(200, int(features.shape[0] / 10))
    print(features.shape)
    print('begin')
    tick = time.time()
    knn_graph = build_knn_graph(features, int(k), alg)
    tock = time.time()
    np.save(out_path, knn_graph)
    print('K: {}'.format(k))
    print('Algorithm: {}'.format(alg))
    print('Duration: {:.3f}s'.format(tock - tick))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='How to build k nearest neighbor graph for features')
    parser.add_argument('--feat_path', help='Path of .npy file containing feature vectors')
    parser.add_argument('--k', help='Number of nearest neighbors for each point')
    parser.add_argument('--alg', help='The algorithm used for finding nearest neighbors')
    parser.add_argument('--out_path', help='Where to save the final knn graph')
    args = parser.parse_args()
    main(args.feat_path, args.k, args.alg, args.out_path)
