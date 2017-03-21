import random
import numpy as np

from levenshtein import levenshtein_distance

MAX_ITERATIONS = 1000


def cluster(samples, k, metric, getter=lambda x: x, **kwargs):
    centroids = randomize_centroids(samples, k)
    old_centroids = randomize_centroids(samples, k)
    clusters = []
    iterations = 0

    similarity = np.zeros((len(samples), len(samples)))
    for i, sample_a in enumerate(samples):
        for j, sample_b in enumerate(samples):
            if j % 100 == 0: print 'Progress: {}%'.format((float(i) + float(j) / len(samples)) / len(samples) * 100)
            if i == j:
                continue
            elif i > j:
                similarity[i][j] = similarity[j][i]
            else:
                similarity[i][j] = metric(getter(sample_a), getter(sample_b), **kwargs)

    while not (has_converged(centroids, old_centroids, iterations)):
        iterations += 1

        # assign samples points to clusters
        clusters = assign_nearest(samples, centroids, similarity)

        old_centroids = centroids
        centroids = calculate_centroids(clusters, similarity)

    return clusters, centroids, iterations, similarity


def assign_nearest(samples, centroids, similarity):
    clusters = [[] for _ in range(len(centroids))]
    for i, sample in enumerate(samples):
        mu_index = \
            min([(j, similarity[i][centroid_id]) for j, centroid_id in enumerate(centroids)], key=lambda t: t[1])[0]
        try:
            clusters[mu_index].append(i)
        except KeyError:
            clusters[mu_index] = [i]

    for cluster in clusters:
        if not cluster:
            cluster.append(np.random.randint(0, len(samples)))

    return clusters


def calculate_centroid(cluster, similarity):
    return min([(sample, average_distance(cluster, sample, similarity)) for sample in cluster], key=lambda t: t[1])[0]


def average_distance(cluster, sample_id, similarity):
    return np.mean([distance for distance in [similarity[sample_id][i] for i in cluster]])


def calculate_centroids(clusters, similarity):
    return [calculate_centroid(cluster, similarity) for cluster in clusters]


def randomize_centroids(samples, k):
    return random.sample(xrange(len(samples)), k)


def has_converged(centroids, old_centroids, iterations):
    if iterations > MAX_ITERATIONS:
        return True
    return old_centroids == centroids


if __name__ == '__main__':
    samples = ['ala', 'aga', 'abba', 'abc', 'def']

    clusters, centroids, iterations = cluster(samples, 3, levenshtein_distance)

    print 'Finished after {} iterations'.format(iterations)
    for (cluster_id, cluster) in enumerate([[samples[i] for i in cluster] for cluster in clusters]):
        cluster_str = ", ".join(cluster)
        print(" - *%s:* %s" % (samples[centroids[cluster_id]], cluster_str))
