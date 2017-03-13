import random
import numpy as np

from levenshtein import levenshtein_distance

MAX_ITERATIONS = 1000


def kmeans(samples, k, metric):
    centroids = randomize_centroids(samples, k)
    old_centroids = randomize_centroids(samples, k)
    clusters = []
    iterations = 0
    while not (has_converged(centroids, old_centroids, iterations)):
        iterations += 1

        # assign samples points to clusters
        clusters = assign_nearest(samples, centroids, metric)

        old_centroids = centroids
        centroids = calculate_centroids(clusters, metric)

    return clusters, centroids, iterations


def assign_nearest(samples, centroids, metric):
    clusters = [[] for _ in range(len(centroids))]
    for sample in samples:
        mu_index = min([(i, metric(sample, centroid)) for (i, centroid) in enumerate(centroids)], key=lambda t: t[1])[0]
        try:
            clusters[mu_index].append(sample)
        except KeyError:
            clusters[mu_index] = [sample]

    for cluster in clusters:
        if not cluster:
            cluster.append(samples[np.random.randint(0, len(samples), size=1)])

    return clusters


def calculate_centroid(cluster, metric):
    return min([(sample, average_distance(cluster, sample, metric)) for sample in cluster], key=lambda t: t[1])[0]


def average_distance(cluster, sample, metric):
    return np.mean([metric(sample, other) for other in cluster])


def calculate_centroids(clusters, metric):
    return [calculate_centroid(cluster, metric) for cluster in clusters]


def randomize_centroids(samples, k):
    return random.sample(samples, k)


def has_converged(centroids, old_centroids, iterations):
    if iterations > MAX_ITERATIONS:
        return True
    return old_centroids == centroids


if __name__ == '__main__':
    metric = levenshtein_distance
    samples = ['bob', 'abc', 'def', 'efg', 'abc', 'def', 'efg', 'abc', 'def', 'efg', 'abc', 'def', 'efg', 'abc', 'def', 'efg', 'abc', 'def', 'efg', 'abc', 'def', 'efg', 'abc', 'def', 'efg']
    clusters, centroids, iterations = kmeans(samples, 3, metric)

    print("The total number of samples instances is: " + str(len(samples)))
    print("The total number of iterations necessary is: " + str(iterations))
    print("The means of each cluster are: " + str(centroids))
    print("The clusters are as follows:")
    for cluster in clusters:
        print("Cluster with a size of " + str(len(cluster)) + " starts here:")
        print(cluster)
        print("Cluster ends here.")
