""" Count skip bigrams. A 0-skip bigram count is a regular bigram count, a count
of w1 and w2. A 1-skip bigram is a count of w1 and w3, etc. Read from stdin. """
import sys
import itertools
from collections import Counter

BOS = "<s>"
EOS = "</s>"

def err(x):
    print(x, file=sys.stderr)
    sys.stderr.flush()

def sliding(xs, n):
    """ Sliding

    Yield adjacent elements from an iterable in a sliding window
    of size n.

    Parameters:
        xs: Any iterable.
        n: Window size, an integer.

    Yields:
        Tuples of size n.

    Example:
        >>> lst = ['a', 'b', 'c', 'd', 'e']
        >>> list(sliding(lst, 2))
        [('a', 'b'), ('b', 'c'), ('c', 'd'), ('d', 'e')]

    """
    its = itertools.tee(xs, n)
    for i, iterator in enumerate(its):
        for _ in range(i):
            next(iterator)
    return zip(*its)

def ichunks(iterable, size):
    while True:
        yield itertools.islice(iterable, size)        

def skipgrams(xs, k):
    for block in sliding(xs, 2+k):
        yield block[0], block[-1]

def tokenize(line):
    parts = line.strip().split()
    parts.insert(0, BOS) 
    parts.append(EOS)
    # Another option here would be to insert EOS and BOS k times.
    # That would mean that in an ngram like "<s> the dog is big </s>",
    # "<s> the" would count as a k-skip bigram for all k.
    # This would be similar to the padding used by kenlm, which
    # has e.g. 5grams like "<s> <s> <s> <s> the". On the other
    # hand, it doesn't seem quite right to me.
    return parts

# en.00.xz is 380,996,016 lines
# bible.txt is 33802 lines
# takes 0.85 to process bible.txt from xzcat
# therefore it should take 2.6 hours to process en.00.xz... hoorah!

# counting in 100000 lines is documented to take 0m4.923s/0m6.475s user
# the real thing is 3809.96016 longer...
# so that's 6.85 hours. But I've been running it for 9:12:26 so far...
# maybe that was the version with sorting? and it's not the gzip version
# anyway.

# size ratio:
# en_small.xz is 2.5M
# en_bigrams_small.gz is 5.7M
# possible factor of 2 increase in size... so big ngrams will be 3.876 TB?
# 

# but I keep running out of memory... 100 GB is not enough;
# if that's not enough then there is no effective upper bound.

# How about breaking long files into multiple counts, writing those out,
# and then merging them? (Is the merge truly O(1) space in the average case?)

flat = itertools.chain.from_iterable

def skipgrams_from_lines(lines, k):
    for line in lines:
        parts = tokenize(line)
        yield from skipgrams(parts, k)

def run_trigrams(lines):
    def get_trigrams(xs):
        return sliding(xs, n)
    grams = flat(map(get_trigrams, map(tokenize, lines)))
    return Counter(grams).items()
    
def run(lines, d):
    assert d >= 0
    def get_ngrams(xs): # gets called as many times as there are lines
        return sliding(xs, d)
    grams = flat(map(get_ngrams, map(tokenize, lines)))
    # All the work happens here:
    counts = Counter(grams) # goes to optimized C subroutine _count_elements 
    return counts.items()

def main(d, s=None):
    err("Beginning skipgram counts")
    if s is None:
        chunks = [sys.stdin]
    else:
        s = int(s)
        chunks = ichunks(sys.stdin, s)
    for chunk in chunks:
        err("Counting ngrams...")
        result = run(chunk, d)
        err("Printing %s ngrams..." % len(result))
        if result:
            for key, count in result:
                print(" ".join(key), count, sep="\t")
        else:
            break

if __name__ == '__main__':
    main(*sys.argv[1:])
                


