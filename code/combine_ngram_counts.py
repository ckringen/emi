""" Given two sorted N-gram counts files, combine them streaming. """
# Just merging sorted streams with addition of counts.
# Could generalize to k streams:
# https://the-algo-blog.blogspot.com/2008/11/merging-sorted-streams.html
import sys

def merge_counts(counts1, counts2):
    counts1 = iter(counts1)
    counts2 = iter(counts2)
    # Get initial values for both streams
    ngram1, count1 = next(counts1)
    ngram2, count2 = next(counts2)
    try:
        while True:
            if ngram1 < ngram2:
                # If stream 1 is behind stream 2, advance stream 1
                yield ngram1, count1
                ngram1, count1 = next(counts1)
            elif ngram2 < ngram1:
                # If stream 2 is behind stream 1, advance stream 2
                yield ngram2, count2
                ngram2, count2 = next(counts2)
            else: # Otherwise they must be equal; then advance both
                assert ngram1 == ngram2
                yield ngram1, count1 + count2
                ngram1, count1 = next(counts1)
                ngram2, count2 = next(counts2)
    except StopIteration: # we get here when one of the streams runs out
        # One of the streams is guaranteed to be empty,
        # so the following gives us the remaining elements of
        # the single non-empty stream:
        remaining = list(counts1) + list(counts2)
        yield from remaining

def test_merge_counts():
    counts1 = [('a', 1), ('b', 2), ('d', 4), ('f', 6)]
    counts2 = [('b', 20), ('c', 30), ('e', 50), ('f', 60), ('g', 70)]
    counts = list(merge_counts(counts1, counts2))
    assert counts == [
        ('a', 1), # a only in list 1
        ('b', 22), # b in list 1 and list 2
        ('c', 30), # c only in list 2
        ('d', 4), # d only in list 1
        ('e', 50), # e only in list 2
        ('f', 66), # f in list 1 and list 2
        ('g', 70) # g only in list 2
    ]

def read_ngram_lines(lines):
    for line in lines:
        ngram, count = line.strip().split("\t")
        yield ngram, int(count)

def main(filename1, filename2):
    with open(filename1, 'rt') as one:
        lines1 = read_ngram_lines(one)
        with open(filename2, 'rt') as two:
            lines2 = read_ngram_lines(two)
            for ngram, count in merge_counts(lines1, lines2):
                print("%s\t%s" % (ngram, str(count)))

if __name__ == '__main__':
    main(*sys.argv[1:])
