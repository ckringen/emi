""" Given an ngram file and a mask, marginalize based on the mask."""
import sys
from collections import Counter
import itertools

def marginalize(lines):
    result = Counter()
    for line, count in lines:
        result[line] += count
    return result.items()

def marginalize_sorted(lines):
    result = Counter()
    curr_start = None
    for line, count in lines:
        result[line] += count
        first, *rest = line.split()
        if curr_start is None:
            curr_start = first
        elif curr_start != first:
            curr_start = None
            yield from result.items()
            result.clear()
    yield from result.items()

def apply_mask(lines, mask):
    for line, count in lines:
        yield " ".join(itertools.compress(line.split(), mask)), count

def read_file(filename):
    with open(filename) as infile:
        for full_line in infile:
            line, count = full_line.split("\t")
            yield line, int(count)

def main(filename, mask_str):
    mask = [bool(int(c)) for c in mask_str]
    lines = read_file(filename)
    new_lines = sorted(apply_mask(lines, mask))
    for line, count in marginalize_sorted(new_lines):
        to_print = str(line) + "\t" + str(count)
        print(to_print)

if __name__ == '__main__':
    main(*sys.argv[1:])
