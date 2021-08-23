import time
import numpy as np
from clustering.utils.utils import bcubed
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import normalized_mutual_info_score

def cluster_faces(features_path, labels_path):
    features = np.load(features_path)
    ac = AgglomerativeClustering(
        n_clusters=None, distance_threshold=1.1, compute_full_tree=True, linkage='single')
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
    return clusters.labels_


# class ThresholdClustering():
#     """
#     This class implements a simple clustering algorithm for faces.
#     Every two points with distance less than a threshold are in one cluster.
#     """
#     def __init__(self, threshold=1.1, feature_length=512):
#         self.cluster_centroids = np.zeros((0, feature_length))
#         self.clusters = []
#         self.threshold = threshold
#         self.num_points = 0
#         self.feature_length = feature_length

#     def run(self, features, talk=False, progress_func=None):
#         self.num_points = features.shape[0]
#         print(features.shape)
#         for i in range(features.shape[0]):
#             f = features[i, :]
#             if self.cluster_centroids.shape[0] == 0:
#                 self.clusters.append([i])
#                 self.cluster_centroids = np.concatenate((self.cluster_centroids, f.reshape(1, -1)), axis=0)
#             else:
#                 dists = np.linalg.norm(self.cluster_centroids - f, axis=1)
#                 closest_index = np.argmin(dists)
#                 closest_dist = dists[closest_index]
#                 if closest_dist < self.threshold:
#                     self.clusters[closest_index].append(i)
#                     self.cluster_centroids[closest_index] = self.__get_new_mean(
#                         self.cluster_centroids[closest_index], len(self.clusters[closest_index]), f)
#                 else:
#                     self.clusters.append([i])
#                     self.cluster_centroids = np.concatenate(
#                         (self.cluster_centroids, f.reshape(1, -1)), axis=0)
#             if talk:
#                 print('Face {} clustered.'.format(i + 1))
#             if progress_func is not None:
#                 progress_func(max(14, int((i + 1) * 1000 / features.shape[0])))
#         return self.clusters

#     def cluster2pred(self):
#         preds = np.zeros((self.num_points,), dtype=snp.int32)
#         for i, items in enumerate(self.clusters):
#             for item in items:
#                 preds[item] = i
#         return preds

#     def __get_new_mean(self, old_mean, num, new_vector):
#         return ((num - 1) * old_mean + new_vector) / num
