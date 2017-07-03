#!/usr/bin/env python3
""" From dep_search query of form _ < _, extract all field pairs.
Second argument is the field, by default word.
Possible fields are id word lemma pos pos2 infl head rel extra notes
"""
from __future__ import print_function
import sys
import itertools as it
from functools import partial
from collections import deque, namedtuple

Line = namedtuple("Line", "id word lemma pos pos2 infl head rel extra notes".split())
ROOT = Line('0', '_', '_', '_', '_', '_', '_', '_', '_', '_')

try:
    map = it.imap
except NameError:
    pass

consume = partial(deque, maxlen=0)

def isplit(xs, sep, maxsplit=None):
    """ Iterative Split

    Like str.split but operates lazily on any iterable.

    Example:
        >>> foo = iter([0, 1, 2, 3, 'dog', 4, 5, 6, 7, 'dog', 8, 9])
        >>> [list(chunk) for chunk in isplit(foo, 'dog')]
        [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]

    """
    xs_it = iter(xs)
    if maxsplit is None:
        while 1:
            subit = iter(partial(next, xs_it), sep)
            try:
                probe = next(subit)
            except StopIteration:
                raise StopIteration
            yield it.chain([probe], subit)
            consume(subit)
    else:
        count = 0
        while count < maxsplit:
            subit = iter(partial(next, xs_it), sep)
            try:
                probe = next(subit) 
            except StopIteration:
                raise StopIteration
            yield it.chain([probe], subit)
            consume(subit)
            count += 1

def parse_query_results(lines):
    hits = isplit(lines, "\n")
    return map(parse_query_hit, hits)


def parse_query_hit(lines):
    iterlines = iter(lines)
    hittokens = []
    for line in iterlines:
        if not line.startswith("#"):
            iterlines = it.chain([line], iterlines)
            break
        if line.startswith("# hittoken:"):
            hittoken = int(line.split()[2])
            hittokens.append(hittoken)
    else:
        raise ValueError("Unparseable hit")

    lines = list(iterlines)
    for hittoken in hittokens:
        depline = Line(*lines[hittoken - 1].split())
        assert int(depline.id) == hittoken
        head = int(depline.head)
        if head == 0:
            yield ROOT, depline, 0
        else:
            headline = Line(*lines[head - 1].split())
            assert int(headline.id) == head, (head, headline, lines)
            yield headline, depline, int(depline.id) - int(headline.id)

def main(lines, field='word'):
    index = Line._fields.index(field)
    for hit in parse_query_results(lines):
        for head, dep, d in hit:
            one = head[index].lower()
            two = dep[index].lower()
            print(one, two, d, sep="\t")

if __name__ == '__main__':
    main(sys.stdin, *sys.argv[1:])
    
    
    
    
    

    
            
