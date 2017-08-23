
# implement functionality of count_skipgrams.py with generator coroutines

import gzip
import collections
import itertools
import mmap
import os
import sys


BOS = "<s>"
EOS = "</s>"


def coroutine( func ):
    def start( *args, **kwargs ):
        cr = func( *args, **kwargs )
        next( cr )
        return cr
    return start


def readFile( fil, target ):
    buffer_size = 1000
    while True:
        buf = sys.stdin.read( buffer_size )
        #buf = fil.read( buffer_size )
        if not buf:
            break
            
        # # this either has a bug, or is just super slow
        # # if you read part way into a word, read some more until you hit a space
        # if buf[-1] != 32:
        #     extra = b""
        #     while True:
        #         extra_byte = sys.stdin.read( 1 )
        #         if extra_byte:
        #             if extra_byte[0] != 32:
        #                 extra = extra + str.encode( extra_byte )
        #             else:
        #                 buf = buf + extra + str.encode( extra_byte )
        #                 break
        #         else:
        #             break
    
        target.send( buf )

    
@coroutine
def tokenize( win_sz, deq ):
    
    while True:
        text = (yield)
        text = text.strip().split( )
        text.insert( 0, BOS ) 
        text.append( EOS )

        try:
            while text:
                bigram = [(text[0], text[win_sz])]
                deq.append(bigram)
                del text[0]               
        except IndexError as e:
            pass


@coroutine
def skipgram( ):
    while True:
        line = (yield)           
        line = line.split()
        try:
            while line:
                deq.append([(line[0],line[window_size])])
                del line[0]
        except IndexError as e:
            pass


def main(textfile, k):

    # f = open(textfile,'r+b')
    # f = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    #f = gzip.open(textfile,"r+b")

    deq = collections.deque( )    
    window_size = int(k)
    
    readFile( textfile, 
        tokenize( window_size, deq ) )
    
    grams = itertools.chain.from_iterable( deq )
    c = collections.Counter( grams )
    print(c)

    # ctr = 0
    # for i in c.keys( ):
    #     if ctr > 20:
    #         break
    #     else:
    #         print(i, c[i])
    #         ctr += 1

if __name__ == "__main__":
    main( sys.argv[1], sys.argv[2] )
