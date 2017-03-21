
import numpy as np
import sklearn.cluster
from levenshtein import levenshtein_distance


def cluster(samples, metric, getter=lambda x: x, **kwargs):
    n_samples = np.asarray(samples)
    print 'Calculating similarity'
    similarity = -1 * np.array([[metric(getter(str_a), getter(str_b), **kwargs) for str_a in n_samples] for str_b in n_samples])
    print 'Done calculating similarity'

    affprop = sklearn.cluster.AffinityPropagation(affinity="precomputed", verbose=True)
    affprop.fit(similarity)

    cluster_ids = np.unique(affprop.labels_)
    centroids = [n_samples[affprop.cluster_centers_indices_[cluster_id]] for cluster_id in cluster_ids]
    clusters = [n_samples[np.nonzero(affprop.labels_ == cluster_id)] for cluster_id in cluster_ids]

    return centroids, clusters

if __name__ == '__main__':
    samples = ['ala', 'aga', 'abba', 'dupa', 'kupa', 'sraka']

    centroids, clusters = cluster(samples, levenshtein_distance)

    for (cluster_id, cluster) in enumerate(clusters):
        cluster_str = ", ".join(cluster)
        print(" - *%s:* %s" % (centroids[cluster_id], cluster_str))
