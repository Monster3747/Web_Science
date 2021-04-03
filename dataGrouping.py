from random import seed, random
import sys
import itertools
import json
import time


# Obtain the data
tweet_id = []
tweet_time = []
tweet_text = []

with open('./data/StreamData.json', 'r', encoding='utf-8') as streamData:
    streamData = json.load(streamData)
    for i in range(0, len(streamData)):
        if not streamData[i]["retweet"]:
            tweet_id.append(streamData[i]['_id'])
            tweet_time.append(streamData[i]['date'])
            tweet_text.append(streamData[i]['tweet_text'])


def merge_list(L):
    length = len(L)
    for i in range(1, length):
        for j in range(i):
            if L[i] == {0} or L[j] == {0}:
                continue
            x = L[i].union(L[j])
            y = len(L[i]) + len(L[j])
            if len(x) < y:
                L[i] = x
                L[j] = {0}

    return [i for i in L if i != {0}]


def merge_list(L):
    length = len(L)
    for i in range(1, length):
        for j in range(i):
            if L[i] == {0} or L[j] == {0}:
                continue
            x = L[i].union(L[j])
            y = len(L[i]) + len(L[j])
            if len(x) < y:
                L[i] = x
                L[j] = {0}
    return [i for i in L if i != {0}]


def generate_shingles(doc, shingleSize):
    shingles = set([])
    for i in range(len(doc) - shingleSize + 1):
        shingles.add(doc[i:i + shingleSize])
    return shingles


def minHash(shingles, n_hashes, random_strings):
    minhash_row = []
    for i in range(n_hashes):
        minhash = sys.maxsize
        for shingle in shingles:
            hash_candidate = abs(hash(shingle + random_strings[i]))
            if hash_candidate < minhash:
                minhash = hash_candidate
        minhash_row.append(minhash)
    return minhash_row


def bandHashes(minHash_row, bandSize):
    band_hashes = []
    for i in range(len(minHash_row)):
        if i % bandSize == 0:
            if i > 0:
                band_hashes.append(band_hash)
            band_hash = 0
        band_hash += hash(minHash_row[i])
    return band_hashes


def similar_text(text, n_hashes, bandSize, shingleSize, collectIndexes=True):
    hash_bands = {}
    random_strings = [str(random()) for _ in range(n_hashes)]
    docNum = 0
    for x in text:
        shingles = generate_shingles(x, shingleSize)
        minhash_row = minHash(shingles, n_hashes, random_strings)
        band_hashes = bandHashes(minhash_row, bandSize)

        docMember = docNum if collectIndexes else x
        for i in range(len(band_hashes)):
            if i not in hash_bands:
                hash_bands[i] = {}
            if band_hashes[i] not in hash_bands[i]:
                hash_bands[i][band_hashes[i]] = [docMember]
            else:
                hash_bands[i][band_hashes[i]].append(docMember)
        docNum += 1

    similar_docs = set()
    # print(len(hash_bands))
    for i in hash_bands:
        for hash_num in hash_bands[i]:
            if len(hash_bands[i][hash_num]) > 1:
                for pair in itertools.combinations(hash_bands[i][hash_num], r=2):
                    similar_docs.add(pair)

    return similar_docs


# Set parameter
n_hashes = 150
bandSize = 50
shingleSize = 3
count = 0

# Calculate the similarity
r = float(n_hashes / bandSize)
similarity = (1 / r) ** (1 / float(bandSize))
similarText= similar_text(tweet_text, n_hashes, bandSize, shingleSize, collectIndexes=False)

if __name__ == '__main__':
    start = time.time()
    arrayResult = []
    for x in similarText:
        numInfo = {x[0], x[1]}
        arrayResult.append(numInfo)
    clusters = merge_list(arrayResult)
    clusters_new = []
    for x in clusters:
        if len(x) > 5:
            clusters_new.append(x)
            print(len(x))

    print("Total have ", len(clusters), "clusters")
    print("Total have ", len(clusters_new), "clusters_new")