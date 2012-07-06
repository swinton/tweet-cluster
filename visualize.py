#!/usr/bin/env python

import csv
import os
import sys
import json
import random
import pdb

from sentence_similarity import sentence_similarity
from clusters import scaledown, draw2d

def distances(documents, distance_fn=sentence_similarity):
    # Initialize 2d matrix
    matrix = [[0.0 for j in xrange(len(documents))] 
                 for i in xrange(len(documents))]

    # Populate matrix with distances
    for i in xrange(len(documents)):
        for j in xrange(len(documents)):
            d1 = documents[i]
            d2 = documents[j]

            # Don't compare document with itself
            if i == j:
                continue

            # Only compare documents once
            if i > j:
                continue

            # Calculate distance
            distance = distance_fn(d1, d2, documents)
            matrix[i][j] = distance
            matrix[j][i] = distance

    return matrix

def visualize(tweets, jpeg="tweets.jpg"):
    ids = [tweet["id_str"] for tweet in tweets]
    texts = [tweet["text"] for tweet in tweets]

    matrix = distances(texts)

    coords = scaledown(matrix)

    draw2d(coords, ids, jpeg=jpeg)

    return ids, matrix, coords

if __name__ == "__main__":
    tweets = json.load(open(sys.argv[1]))

    ids, matrix, coords = visualize(tweets)
    ids = [str([id]) for id in ids]

    for filename, obj in (("ids.csv", ids), ("matrix.csv", matrix), ("coords.csv", coords)):
        writer = csv.writer(open(filename, "wb"))
        writer.writerows(obj)

    os.system("open tweets.jpg")
