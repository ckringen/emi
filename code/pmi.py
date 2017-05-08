""" Calculate pmi values from ngram counts. """
import sys
from collections import Counter
from math import log

def read(lines):
    for line in lines:
        thing, count = line.strip().split("\t")
        count = int(count)
        yield tuple(thing.split()), count

def pmi(counts):
    xy_counts = Counter(dict(counts))
    Z = sum(xy_counts.values())
    A = log(Z)
    x_counts = Counter()
    y_counts = Counter()
    for (x, y), count in xy_counts.items():
        x_counts[x] += count
        y_counts[y] += count
    for (x, y), xy_count in xy_counts.items():
        unnorm = log(xy_count) - log(x_counts[x]) - log(y_counts[y])
        yield (x, y), unnorm + A

if __name__ == '__main__':
    results = pmi(read(sys.stdin))
    for (x, y), pmi in results:
        print(x, y, pmi, sep="\t")
