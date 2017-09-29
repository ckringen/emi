
# implement functionality of count_skipgrams.py witha pipeline of posix processes
# we used a joinable queue to get the "queue.task_done( )" functionality, but it doesn't
# appear to be necessary; queue.empty() must trigger the appropriate ending sequence

import gzip
import multiprocessing
import collections
import itertools
import mmap
import os
import sys


BOS = "<s>"
EOS = "</s>"

    
def producer( f, queue, sentinel ):
    buffer_size = 10000
    ctr = 0
    while True:
        buf = f.read(buffer_size)
        if not buf:
            queue.put(sentinel)
            break                    
        queue.put(buf)
        ctr += 1

                
def tokenizer( in_queue, out_queue, counter, sentinel, window_size ):
    ctr = 0
    while True:
        buf = in_queue.get( )
        if buf is sentinel:
            out_queue.put(counter)
            break            
        buf = buf.split( )
        try:
            while buf:
                skip = [(buf[0],buf[window_size])]
                #counter.update( skip )
                #print(counter)
                del buf[0]                                
        except IndexError as e:
            pass
            
            
def skipgrammer( in_queue, out_queue):
    while True:
        buf = in_queue.get( )
        try:
            while buf:
                if buf is sentinel:
                    out_queue.put(sentinel)
                    break
                else:
                    skip = (buf[0], buf[2])
                    out_queue.put(skip)
                    del buf[0]
        except IndexError as e:
            pass
    
def consumer( queue):
    while True:
        buf = queue.get( )
        if buf is sentinel:
            break
        else:
            c = collections.Counter( buf )



def main(textfile, k):
    
    sentinel = None
    window_size = int(k)

    c = collections.Counter( )        
    in_queue = multiprocessing.JoinableQueue()
    out_queue = multiprocessing.JoinableQueue()

    # f = open(textfile,'r+b')
    # f = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    f = gzip.open( textfile, "r+b")

    prod = multiprocessing.Process(target=producer, args=( f, in_queue, sentinel ))
    tok = multiprocessing.Process(target=tokenizer, args=( in_queue, out_queue, c, sentinel, window_size ))

    prod.start()
    tok.start( )

    in_queue.join( )
    prod.join( )
    tok.join( )
    
    # grams = itertools.chain.from_iterable( deq )
    # c = collections.Counter( grams )
    print(out_queue.get( ))


if __name__ == "__main__":
    main( sys.argv[1], sys.argv[2] )
