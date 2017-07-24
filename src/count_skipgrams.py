
""" Count skip bigrams. A 0-skip bigram count is a regular bigram count, a count
of w1 and w2. A 1-skip bigram is a count of w1 and w3, etc. Read from stdin. """

import time
import os, mmap

import sys
import itertools
import collections

import fileinput

    
BOS = "<s>"
EOS = "</s>"

def err(x):
    print(x, file=sys.stderr)
    sys.stderr.flush()

@profile
def ichunks(iterable, size):
    while True:
        yield itertools.islice(iterable, size)        

@profile
def tokenize(line):

    #print("tokenizing")

    parts = line.strip().split()
    parts.insert(0, BOS) 
    parts.append(EOS)
    # Another option here would be to insert EOS and BOS k times.
    # That would mean that in an ngram like "<s> the dog is big </s>",
    # "<s> the" would count as a k-skip bigram for all k.
    # This would be similar to the padding used by kenlm, which
    # has e.g. 5grams like "<s> <s> <s> <s> the". On the other
    # hand, it doesn't seem quite right to me.

    # print("parts are: ", parts)
    
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

@profile
def run(lines, k):
    
    assert k >= 0
    window_size = k + 2
    
    def get_skipgrams(xs): # gets called as many times as there are lines
        
        its = itertools.tee(xs, window_size)   # so xs is an iterable, such that it can return an iterator
        for i, iterator in enumerate(its):
            for _ in range(i):
                next(iterator)

        # for i in zip(*its):
        #     print(i)
        #     print(i[0], i[-1])
        # print("outside")

        for block in zip(*its):
            # tup = (block[0], block[-1])
            # ct = collections.Counter(tup)
            # print(ct)            
            #print( "blocks: ", block[0], block[-1], type(block[0]), type(block))
            yield block[0], block[-1]                          # "window_size-skip-bigrams", e.g. 4-skip-2-grams

    grams = flat(map(get_skipgrams, map(tokenize, lines)))

    #print(type(grams))
    
    # All the work happens here:
    counts = collections.Counter(grams) # goes to optimized C subroutine _count_elements 
    #print(counts.items( ))
    return counts.items()

    
# Ideas:
# (1) insert stuff into a bst
# (2) initialize an array of hashes for the first word, then sort within the
#     array associated with each hash.

# 128GB RAM doesn't seem to cause queueing issues.
# So let's take that as our RAM and figure out what's the largest size
# we can handle within that RAM.
# We want to find m, and currently know
# 100,000 < m < 380,996,016
# Let's take the true lines to be 400,000,000.
# Then bisect to 200,000,000, 100,000,000, 50,000,000, etc.
# Run them in parallel and see which survive.

# OK, looks like 100,000,000 can work with 128 GB RAM.
# It can get through one cycle...pray it gets through all of them.
# It should take 3 cycles, and has taken 3 hours so far...
# total run time 9 hours? that's about when memory ran out in the past.

# Discovery: scancel does not force stdout flush--
# guess it doesn't send SIGINT.

# still need to get size estimate for gzipped N-gram counts file,
# then multiply that by 100,
# then figure out the gzip time,
# then finally we will be able to estimate the time taken by gz-sort.

# gz-sort run time is roughly:
# seconds = time zcat data.gz | gzip > /dev/null
# seconds * entropy * (log2(uncompressed_size/S) + 2)
#

# TODO fix punctuation tokenization in prepro_post_dedup.sh!
# or add it elsewhere!

# time to xzcat | xz : real 824m45.692s / user 855m59.459s
# time to do the broken thing: 640m43.344s / 627m10.260s

# 100,000,000 died, but not before producing its first iteration,
# which was 2G gzipped...how could that be?
# 200,000,000 died

# en_small is 100000 lines unprocessed
#             130926 lines processed
# It takes 15 iterations of s=10000---seems like it should take 14?


@profile
def main2(textfile, k, s=None ):
    ''' textfile can be a regular file, or a fileobject, e.g. sys.stdin '''
    err("Beginning skipgram counts")
    k = int(k)

    if s is None:
        chunks = [textfile]

    else:
        s = int(s)
        chunks = ichunks(textfile, s)
        
    for chunk in chunks:
        #err("Counting skipgrams...")
        result = run(chunk, k)

        #err("Printing %s skipgrams..." % len(result))
        if result:
            print("done")
            # for key, count in result:
            #     print(" ".join(key), count, sep="\t")
        else:
            break

        
def main(k, s=None ):
    err("Beginning skipgram counts")
    k = int(k)
    
    if s is None:
        chunks = [sys.stdin]
    else:
        s = int(s)
        chunks = ichunks(sys.stdin, s)

    for chunk in chunks:
        err("Counting skipgrams...")
        result = run(chunk, k)
        err("Printing %s skipgrams..." % len(result))
        if result:
            print("done")
            # for key, count in result:
            #     print(" ".join(key), count, sep="\t")
        else:
            break



def getSkipgrams(xs): # gets called as many times as there are lines

    print("xs is ", xs)

    its = itertools.tee(xs, 2)   # so xs is an iterable, such that it can return an iterator
    for i, iterator in enumerate(its):
        for _ in range(i):
            next(iterator)
    for block in zip(*its):
        yield block[0], block[-1]

        
if __name__ == '__main__':


    f = open('../profiling/SampleData/large_file.txt', 'r+b')
    mmap_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

    a = time.time( )
    #f = open("../profiling/SampleData/large_file.txt", "r")
    main2(f,2,100000)
    #main(*sys.argv[1:])        
    b = time.time( )

    print(b - a )
