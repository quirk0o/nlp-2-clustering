import string
from datetime import datetime

from preprocessing import *
from clustering import cluster
from levenshtein import levenshtein_distance
from lcs import lcs_distance
from statistics import db_index, dunn_index

DATA_FILENAME = 'data/lines.txt'


def clean_line(line, stopwords):
    words = line.split(' ')
    clean = remove_short_words(remove_stopwords(words, stopwords))
    return string.join(clean, ' ')


if __name__ == '__main__':
    with open(DATA_FILENAME) as data_file:
        text = data_file.read()
        preprocessed = deduplicate_whitespace(remove_special_chars(text.lower()))
        stopwords = find_stopwords(preprocessed)
        lines = preprocessed.split('\n')

        metric = levenshtein_distance
        metric_name = 'lev'
        sample_n = 20
        k = 10
        samples = zip(text.split('\n'), [clean_line(line, stopwords) for line in lines[:sample_n]])

        output_filename = 'clusters/{}.{}.{}.{}.dat'.format(datetime.now().strftime("%Y-%m-%d.%H:%M"), metric_name, sample_n, k)
        with open(output_filename, 'w') as output_file:

            clusters, centroids, iterations, similarity = cluster(samples, k, lcs_distance, getter=lambda sample: sample[1])

            for (i, cluster) in enumerate(clusters):
                print 'Cluster of size: {}'.format(len(cluster))
                print 'Centroid: *{}*'.format(samples[centroids[i]][0])
                output_file.write('*{}*\n'.format(samples[centroids[i]][0]))
                for sample_id in cluster:
                    print samples[sample_id][0]
                    output_file.write(samples[sample_id][0])
                    output_file.write('\n')
                print '-------------------'
                output_file.write('---------------------\n')

            print '\n***************\nStatistics: '
            print 'Davies-Bouldin index: {}'.format(db_index(clusters, centroids, similarity))
            print 'Dunn index: {}'.format(dunn_index(clusters, centroids, similarity))


## Levenshtein
# Davies-Bouldin: 0.43
# Dunn: 0.65

## Longest Common Substring
# Davies-Bouldin: 0.4
# Dunn: 0.5
