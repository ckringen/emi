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
        #print("calling next")
        next( cr )
        return cr
    return start

    
# if buffer size is 100000, time taken is 1.6 sec
# but if it's 8 or 10, time taken drops to .47; possibly due to average word size??
def read_mmap( f, target ):
    buffer_size = 8
    while True:
        buf = f.read(buffer_size)
        if not buf:
            print("breaking")
            break

        # this either has a bug, or is just super slow
        # # if you read part way into a word, read some more until you hit a space
        # if buf[-1] != 32:
        #     extra = b""
        #     while True:
        #         extra_byte = f.read(1)
        #         if extra_byte:
        #             if extra_byte[0] != 32:
        #                 extra = extra + str.encode(extra_byte)
        #             else:
        #                 buf = buf + extra + str.encode(extra_byte)
        #                 break
        #         else:
        #             break

        target.send( buf )
        

@coroutine
def tokenize( ): #target ):
    while True:
        text = (yield)
        text = text.split( )
        try:
            while text:
                bigram = [(text[0], text[window_size])]
                deq.append(bigram)
                #target.send( bigram )
                del text[0]               
        except IndexError as e:
            pass #print(e)

        
# @coroutine
# def tokenize(token_string, target):
#     tokens = token_string.split( )
#     while True:
#          s = tokens[0]
#          tokens = tokens[1:]
#          if s == "data":
#              time.sleep(0.1)    # Sleep briefly
#              continue
#          target.send( s )

# @coroutine
# def loadOnQueue( target ):
#     while True:
#         element = (yield)
#         if len(deq) < 8:
#             deq.append( element )
#         elif len(deq) == 8:
#             print(deq)
#             target.send( deq )
#             deq.popleft( )

         
# @coroutine
# def skipgram(pattern,target):
#     while True:
#         line = (yield)           # Receive a line
#         for k,v in enumerate(line):
#             if k == len(line):
#                 break
#             else:
#                 target.send((line[k],line[k+window_size]))    # Send to next stage

            
# A sink.  A coroutine that receives data
@coroutine
def count():
    while True:
        line = (yield)
        c.update( line )


if __name__ == '__main__':

    a = '''this is a this is bytes bytes file file file to test bigram bigram counting.
    for what it's worth worth here is some more tasty data.'''

    deq = collections.deque( )

    window_size = 2


    f = open("../../SampleData/large_file.txt", "r")
    
    read_mmap( f,
               tokenize( ) )
                   #count( ) ) )

    #print(c)
    import itertools
    grams = itertools.chain.from_iterable( deq )
    c = collections.Counter( grams )
    #print(c)
