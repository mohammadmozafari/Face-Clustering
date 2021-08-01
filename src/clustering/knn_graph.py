import os
import numpy as np
from sklearn.neighbors import NearestNeighbors

def build_knn_graph(features, k, alg):
    nn = NearestNeighbors(n_neighbors=k, algorithm=alg).fit(features)
    indices = nn.kneighbors(return_distance=False)
    graph = np.concatenate((np.arange(features.shape[0]).reshape((features.shape[0], 1)), indices), axis=1)
    return graph
