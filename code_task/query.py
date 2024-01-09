def query_index(word, filenames_file='filenames', index_file='index'):
    with open(filenames_file, 'r') as f:
        filenames = f.read().splitlines()

    index = {}
    with open(index_file, 'r') as f:
        for line in f:
            parts = line.split()
            word = parts[0]
            frequencies = list(map(int, parts[1:]))
            index[word] = frequencies

    if word in index:
        result = sorted(zip(index[word], filenames), reverse=True)
        for freq, filename in result:
            print(f"{freq} {filename}")
    else:
        print(f"The word '{word}' is not found in the index.")