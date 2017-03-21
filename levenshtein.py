import numpy as np


def levenshtein_distance_old(word_a, word_b, threshold=None):
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
            if threshold and distance[i][j] > threshold:
                return 10000000

    return int(distance[len_a][len_b])


def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


if __name__ == '__main__':
    print levenshtein_distance('kot', 'kot')
    print levenshtein_distance('kot', 'kod')
    print levenshtein_distance('telefon', 'telegraf')
    print levenshtein_distance('cargo partner spedycja srz kamiennogorska poznan eax', 'ssontex zo import export przeclawska nip')
    print levenshtein_distance('pa interior bolshaya lubyanka inn kpp', 'pa interior bolshaya lubyanka inn kpp')
