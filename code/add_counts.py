""" Add counts for adjacent identical ngrams. """

import sys
import operator
import itertools

def read_lines(lines):
    for line in lines:
        try:
            ngram, count = line.strip().split("\t")
            yield ngram, int(count)
        except ValueError as e:
            print(e, file=sys.stderr)
            print("skipping bad line: %s" % line, file=sys.stderr)

def process(lines):
    ngrams = read_lines(lines)
    for ngram, group in itertools.groupby(ngrams, operator.itemgetter(0)):
        yield ngram, sum(count for _, count in group)
    
def main():
    for ngram, count in process(sys.stdin):
        print("%s\t%s" % (ngram, str(count)))

if __name__ == '__main__':
    main()
