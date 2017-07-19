
import numba
import sys
import collections
import itertools

def ichunks(iterable, size):
    while True:
        yield itertools.islice(iterable, size)        

@jit
def NumbaTokenize(line):
    parts = line.strip().split()
    parts.insert(0, BOS) 
    parts.append(EOS)
    return parts

def tokenize(line):
    parts = line.strip().split()
    parts.insert(0, BOS) 
    parts.append(EOS)
    return parts


def prof_NumbaTokenize( ):

    



if __name__ == "__main__":

    
