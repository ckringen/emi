
import time
import collections
import multiprocessing
import concurrent.futures
import itertools
import dis
import pdb

def playing(func):
    def thedozens(*args,**kwargs):
        print(dis.dis(*args))
        return
    return thedozens


#@profile
def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        next( cr )
        return cr
    return start

    
# if buffer size is 100000, time taken is 1.6 sec
# but if it's 8 or 10, time taken drops to .47; possibly due to average word size??
#@profile
def read_mmap( f, target ):
    pdb.set_trace( )
    buffer_size = 10
    while True:
        buf = f.read(buffer_size)
        if not buf:
            print("breaking")
            break

        #this either has a bug, or is just super slow
        # if you read part way into a word, read some more until you hit a space
        if buf[-1] != 32:
            extra = b""
            while True:
                extra_byte = f.read(1)
                if extra_byte:
                    if extra_byte[0] != 32:
                        extra = extra + str.encode(extra_byte)
                    else:
                        buf = buf + extra + str.encode(extra_byte)
                        break
                else:
                    break

        target.send( buf )
        

def skip( idx, text ):
    offset = 2
    bigram = [(text[idx], text[idx+offset])]
    return bigram


@coroutine
def skipgramProcess( ):   
    while True:
        text = (yield)
        text = text.split( )
        try:
            executor = concurrent.futures.ProcessPoolExecutor(max_workers=10)
            copies = itertools.repeat(text,len(text))
            skips = range(0,len(text),window_size)

            for idx, bigram in zip(skips, executor.map(skip, skips, copies)):
                #print('%d idx has as skips: %s' % (idx, bigram))
                deq.append( bigram )
            
        except IndexError as e:
            pass #print(e)

        
@coroutine
def skipgramThread( ):   
    while True:
        text = (yield)
        text = text.split( )
        try:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
            copies = itertools.repeat(text,len(text))
            skips = range(0,len(text),window_size)

            for idx, bigram in zip(skips, executor.map(skip, skips, copies)):
                #print('%d idx has as skips: %s' % (idx, bigram))
                deq.append( bigram )
            
        except IndexError as e:
            pass #print(e)

    
        
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



@coroutine
#@profile
def skipgram():#,target):
    while True:
        line = (yield)           # Receive a line
        line = line.split()
        try:
            while line:
                deq.append([(line[0],line[window_size])])
                del line[0]
        except IndexError as e:
            pass


            
# A sink.  A coroutine that receives data
@coroutine
def count():
    while True:
        line = (yield)
        c.update( line )


if __name__ == '__main__':

    # deq = collections.deque( )
    # window_size = 2
    # f = open("../../SampleData/large_file.txt", "r")
    
    # print(read_mmap( f,
    #            skipgram( ) ) )
    #                #count( ) ) )

    # #print(c)
    # grams = itertools.chain.from_iterable( deq )
    # c = collections.Counter( grams )
    # #print(c)

    print(dis.dis(read_mmap))
