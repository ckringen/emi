
# I want to be able to do all stages of the skipgram pipeline "at once"

from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import sys

a = '''this is a this is bytes bytes file file file to test bigram bigram counting.
for what it's worth worth here is some more tasty data.'''.split( )

window_size=2

q = deque( )


def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start


# possibly want a generator?
def produceVals( tokens ):
    log = logging.getLogger('produceVals')
    log.info('running')
    
    i = 0
    if tokens:
        yield tokens[i]
        i += 1
    log.info('done')
        

def loadQueue( *args  ):
    log = logging.getLogger('run_loadQueue')
    log.info('starting')
    
    print(*args)
    if len(q) < 8:
        q.append( *args )
    elif len(q) == 8:
        print(q)
        q.popleft( )
        
    log.info('done')    

    
def skipgramAsync( q ):
    try:
        countwords( (q[idx], q[idx+window_size] ) )    
    except IndexError as e:
        print(e)

        
def countwords( two_tup ):
    if two_tup in dict:
        dict[two_tup] += 1
    else:
        dict[two_tup] = 1

def n( gen ):
    log = logging.getLogger('produceVals')
    log.info('running')

    try:
        return next(gen)
    except StopIteration:
        print("donezo")

    log.info('done')
    
if __name__ == "__main__":
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(threadName)10s %(name)18s: %(message)s',
        stream=sys.stderr,
    )

    generator = (word + '!' for word in 'baby let me iterate ya'.split())
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [ ] 
        futures.append(executor.submit( n, generator ))
        futures.append(executor.submit( n, generator ))
        futures.append(executor.submit( n, generator ))
        futures.append(executor.submit( n, generator ))
        futures.append(executor.submit( n, generator ))
        futures.append(executor.submit( n, generator ))

        for future in as_completed(futures):
            print(future.result( ))
