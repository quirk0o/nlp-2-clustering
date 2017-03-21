import string

from preprocessing import *

DATA_FILE = 'data/lines.txt'

if __name__ == '__main__':
    with open(DATA_FILE) as data_file:
        lines = data_file.read()
        preprocessed = deduplicate_whitespace(remove_special_chars(lines.lower()))
        stopwords = find_stopwords(preprocessed)

        for line in preprocessed.split('\n'):
            words = line.split(' ')
            clean_words = remove_stopwords(remove_short_words(words), stopwords)
            clean_line = string.join(clean_words, ' ')
            print clean_line
