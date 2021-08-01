import os
import numpy as np
from sklearn.neighbors import kneighbors_graph

def build_knn_graph(features, k):
    A = kneighbors_graph(features, k, mode='connectivity', include_self=True)
    A = A.toarray()
    dense_matrix = np.zeros((features.shape[0], k+1), dtype=np.int32)
    positions = np.argwhere(A == 1)
    for i in range(A.shape[0]):
        dense_matrix[i, 0] = i
        dense_matrix[i, 1:] = positions[i*k: (i+1)*k, 1]
    return dense_matrix

def main(features_path, output_path, k):
    features = np.load(features_path)
    knn_graph = build_knn_graph(features, k)
    os.mkdir('./data/knn')
    np.save(output_path, knn_graph)

if __name__ == "__main__":
    features_path = './data/features/features_1_9_.npy'
    output_path = './data/knn/knn_graph.npy'
    k = 200
    main(features_path, output_path, k)
