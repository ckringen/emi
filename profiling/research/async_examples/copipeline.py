# copipe.py
#
# A simple example showing how to hook up a pipeline with
# coroutines.   To run this, you will need a log file.
# Run the program logsim.py in the background to get a data
# source.

import time
import collections


def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        print("calling next")
        next( cr )
        return cr
    return start


# A data source.  This is not a coroutine, but it sends
# data into one (target)
def tokenize(token_string, target):
    tokens = token_string.split( )
    while True:
         s = tokens[0]
         tokens = tokens[1:]
         if s == "data":
             time.sleep(0.1)    # Sleep briefly
             continue
         target.send( s )

@coroutine
def loadOnQueue( target ):
    while True:
        element = (yield)
        if len(deq) < 8:
            deq.append( element )
        elif len(deq) == 8:
            print(deq)
            target.send( deq )
            deq.popleft( )

         
# A filter.
@coroutine
def skipgram(pattern,target):
    while True:
        line = (yield)           # Receive a line
        for k,v in enumerate(line):
            if k == len(line):
                break
            else:
                target.send((line[k],line[k+window_size]))    # Send to next stage

            
# A sink.  A coroutine that receives data
@coroutine
def count():
    while True:
        line = (yield)
        #c = c( line )
        print( line, )


if __name__ == '__main__':

    a = '''this is a this is bytes bytes file file file to test bigram bigram counting.
    for what it's worth worth here is some more tasty data.'''

    deq = collections.deque( )

    window_size = 2

    c = collections.Counter( )
    
    tokenize( a,
           loadOnQueue( 
                        skipgram( 'python',
                                  count( ) ) ) )
