import os
import sys
import getopt
import string
from collections import OrderedDict

from query import query_index


def preprocess_word(word):
    word = word.strip(string.punctuation)
    return word.lower()


def build_index(file_paths, filenames_file='filenames', index_file='index'):
    index = OrderedDict()
    filenames = []


    for file_path in file_paths:
        filenames.append(os.path.basename(file_path))
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            words = content.split()

            for word in words:
                word = preprocess_word(word)
                if word not in index:
                    index[word] = [0] * len(file_paths)
                index[word][len(filenames) - 1] += 1

    with open(filenames_file, 'w') as f:
        f.write('\n'.join(filenames))

    with open(index_file, 'w') as f:
        for word, frequencies in index.items():
            line = f"{word} {' '.join(map(str, frequencies))}\n"
            f.write(line)



def main(argv):
    try:
        opts, args = getopt.getopt(argv, "i:n:")
    except getopt.GetoptError:
        print("Usage: python index.py [-i <index_file>] [-n <filenames_file>] file1 file2 ...")
        sys.exit(2)

    filenames_file = 'filenames'
    index_file = 'index'

    for opt, arg in opts:
        if opt == '-i':
            index_file = arg
        elif opt == '-n':
            filenames_file = arg

    if len(args) == 0:
        print("Please provide at least one file to index.")
        sys.exit(2)

    build_index(args, filenames_file, index_file)

    if len(args) > 0 and args[0] == 'query':
        if len(args) < 2:
            print("Please provide a word to query.")
            sys.exit(2)
        query_index(args[1], filenames_file, index_file)

if __name__ == "__main__":
    main(sys.argv[1:])