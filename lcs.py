import numpy as np


def longest_common_substring(word_a, word_b):
    len_a = len(word_a)
    len_b = len(word_b)

    if min(len_a, len_b) == 0:
        return 0

    lcs = np.zeros([len_a + 1, len_b + 1])

    max_len = 0
    for i, a in enumerate(word_a, start=1):
        for j, b in enumerate(word_b, start=1):
            if a == b:
                lcs[i][j] = lcs[i - 1][j - 1] + 1
                max_len = max(max_len, lcs[i][j])
            else:
                lcs[i][j] = 0

    return int(max_len)


def lcs_distance(word_a, word_b):
    return 1 - float(longest_common_substring(word_a, word_b)) / max(len(word_a), len(word_b))


if __name__ == '__main__':
    print longest_common_substring('kot', 'kot')
    print longest_common_substring('kot', 'kod')
    print longest_common_substring('telefon', 'telegraf')
