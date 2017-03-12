from preprocessing import *

DATA_FILE = 'data/lines.txt'

if __name__ == '__main__':
    with open(DATA_FILE) as data_file:
        lines = data_file.read()
        preprocessed = deduplicate_whitespace(remove_special_chars(lines.lower()))
        stopwords = find_stopwords(preprocessed)
        for line in preprocessed.split('\n'):
            clean = string.join(remove_stopwords(line.split(' '), stopwords), ' ')
            print clean
