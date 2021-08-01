import numpy as np
import pandas as pd

class ThresholdClustering():
    """
    This class implements a simple clustering algorithm for faces.
    Every two points with distance less than a threshold are in one cluster.
    """
    def __init__(self, threshold=1.1, feature_length=512):
        self.cluster_centroids = np.zeros((0, feature_length))
        self.clusters = []
        self.threshold = threshold

    def run(self, features, talk=False, progress_func=None):
        for i in range(features.shape[0]):
            f = features[i, :]
            if self.cluster_centroids.shape[0] == 0:
                self.clusters.append([i])
                self.cluster_centroids = np.concatenate((self.cluster_centroids, f.reshape(1, -1)), axis=0)
            else:
                dists = np.linalg.norm(self.cluster_centroids - f, axis=1)
                closest_index = np.argmin(dists)
                closest_dist = dists[closest_index]
                if i == 10:
                    break
                if closest_dist < self.threshold:
                    self.clusters[closest_index].append(i)
                    self.cluster_centroids[closest_index] = self.__get_new_mean(
                        self.cluster_centroids[closest_index], len(self.clusters[closest_index]), f)
                else:
                    self.clusters.append([i])
                    self.cluster_centroids = np.concatenate(
                        (self.cluster_centroids, f.reshape(1, -1)), axis=0)
            if talk:
                print('Face {} clustered.'.format(i + 1))
            if progress_func is not None:
                progress_func(max(14, int((i + 1) * 1000 / features.shape[0])))
        return self.clusters

    def __get_new_mean(self, old_mean, num, new_vector):
        return ((num - 1) * old_mean + new_vector) / num

