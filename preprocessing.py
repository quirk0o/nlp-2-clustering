import re
from collections import Counter

import math

STOPWORD_MIN_OCCURENCE = 0.025


def remove_special_chars(text):
    return re.sub(r'[^A-Za-z\s]+', ' ', text)


def deduplicate_whitespace(text):
    return re.sub(r'[ \t]+', ' ', text)


def find_stopwords(text):
    words = re.sub(r'\n', ' ', text).split(' ')
    counter = Counter(words)
    len = math.sqrt(sum([x ** 2 for x in counter.values()]))
    vec = dict([(word, float(count) / len) for (word, count) in counter.items()])
    return sorted([w[0] for w in vec.items() if w[1] > STOPWORD_MIN_OCCURENCE], key=vec.get, reverse=True)


def remove_stopwords(words, stopwords):
    return [w for w in words if w not in stopwords]


def remove_short_words(words, min_len=1):
    return [w for w in words if len(w) > min_len]
