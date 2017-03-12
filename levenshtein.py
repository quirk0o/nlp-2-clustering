import numpy as np


def levenshtein_distance(word_a, word_b):
    len_a = len(word_a)
    len_b = len(word_b)

    if min(len_a, len_b) == 0:
        return max(len_a, len_b)

    distance = np.empty([len_a + 1, len_b + 1])

    for i in xrange(0, len_a + 1):
        distance[i][0] = i

    for j in xrange(0, len_b + 1):
        distance[0][j] = j

    for i, a in enumerate(word_a, start=1):
        for j, b in enumerate(word_b, start=1):
            distance[i][j] = min(
                distance[i - 1][j] + 1,
                distance[i][j - 1] + 1,
                distance[i - 1][j - 1] + (1 if a != b else 0)
            )

    return int(distance[len_a][len_b])


if __name__ == '__main__':
    print levenshtein_distance('kot', 'kot')
    print levenshtein_distance('kot', 'kod')
    print levenshtein_distance('telefon', 'telegraf')
