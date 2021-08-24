import time
import argparse
import numpy as np
from clustering.utils.utils import bcubed
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import normalized_mutual_info_score

def main(features_path, labels_path):
    features = np.load(features_path)
    ac = AgglomerativeClustering(n_clusters=None, distance_threshold=1.1, compute_full_tree=True, linkage='single')
    tick = time.time()
    clusters = ac.fit(features)
    tock = time.time()
    print()
    print('Clustering duration: {:.2f}s'.format(tock - tick))
    if labels_path:
        labels = np.load(labels_path)
        p, r, f = bcubed(clusters.labels_, labels)
        nmi = normalized_mutual_info_score(clusters.labels_, labels)
        print('Precision: {:.3f}, Recall: {:.3f}, F: {:.3f}'.format(p, r, f))
        print('NMI: {:.3f}'.format(nmi))
    else:
        print('Predicted labels: ')
        print('\t{}'.format(clusters.labels_))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='How to evaluate threshold clustering algorithm')
    parser.add_argument('path', help='Path of .npy file containing feature vectors')
    parser.add_argument('--labels_path', help='Path of .npy file containing labels')
    args = parser.parse_args()
    
    features_path = args.path
    labels_path = args.labels_path
    main(features_path, labels_path)
