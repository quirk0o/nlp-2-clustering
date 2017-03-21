import numpy as np


def average_distance(cluster, similarity):
    return np.mean([similarity[i][j] for i in cluster for j in cluster])


def db_index(clusters, centroids, similarity):
    return sum([max([(average_distance(clusters[i], similarity) + average_distance(clusters[j], similarity)) /
                     similarity[centroid_i][centroid_j] for j, centroid_j in
                     enumerate(centroids) if j != i]) for i, centroid_i in enumerate(centroids)]) / len(
        [sample for cluster in clusters for sample in cluster])


def cluster_size(cluster, centroid, similarity):
    return max([similarity[i][centroid] for i in cluster])


def dunn_index(clusters, centroids, similarity):
    num = min(
        [similarity[ci][cj] for ci in centroids for cj in centroids if ci != cj])
    denom = max(
        [cluster_size(cluster, centroids[i], similarity) for i, cluster in enumerate(clusters)])
    if denom == 0:
        return 1
    return num / denom
