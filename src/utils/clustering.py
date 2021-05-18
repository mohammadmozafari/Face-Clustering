from os import close
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

    def find_clusters(self, features_files):
        feature_iter = self.__feature_iter(features_files)
        for i, f in feature_iter:
            if self.cluster_centroids.shape[0] == 0:
                self.clusters.append([i])
                self.cluster_centroids = np.concatenate((self.cluster_centroids, f.reshape(1, -1)), axis=0)
                continue
            dists = np.linalg.norm(self.cluster_centroids - f, axis=1)
            closest_index = np.argmin(dists)
            closest_dist = dists[closest_index]
            if i == 10: break
            if closest_dist < self.threshold:
                self.clusters[closest_index].append(i)
                self.cluster_centroids[closest_index] = self.__get_new_mean(
                    self.cluster_centroids[closest_index], len(self.clusters[closest_index]), f)
            else:
                self.clusters.append([i])
                self.cluster_centroids = np.concatenate((self.cluster_centroids, f.reshape(1, -1)), axis=0)
            print('Face {} clustered.'.format(i + 1))
        return self.clusters

    def __feature_iter(self, features_files):
        """
        This generator goes through all features csv files
        and returns an iterator of all the features.
        """
        current_file = 0
        index = 0
        for _ in range(len(features_files)):
            file_name = features_files[current_file]
            features = pd.read_csv(file_name).values
            for j in range(features.shape[0]):
                yield index, features[j, :]
                index += 1

    def __get_new_mean(self, old_mean, num, new_vector):
        return ((num - 1) * old_mean + new_vector) / num

