
# way simpler multiprocessing interface, but unfortunately, runs out of memory
# slurmstepd: error: Job 9418786 exceeded memory limit (272428464 > 268435456), being killed
# slurmstepd: error: *** JOB 9418786 ON node046 CANCELLED AT 2017-09-22T22:57:57 ***

# so we could 
# 1. profile c++ and python scripts respectively to compare memory usage
# 2. write dependency parser in c++ for the sake of uniformity
# 3. begin python calculations
# 4. final begin write-up

from functools import partial
import sys
import pickle
import multiprocessing
import collections

import count_skipgrams as skip

def cs_wrapper( idx, window_sz ):    
    if idx < 10:
        idx = "0{}".format(idx)    
    f = open("/om/user/ckringen/data/commoncrawl_en_deduped_filtered/en.{}.gz".format(idx), "r")
    return skip.main2( f, window_sz )

def reduce( b1, b2 ):
    d1 = pickle.loads(b1)
    d2 = pickle.loads(b2)        
    for key, value in d2.items( ):
        if key in d1:
            d1[key] += value
        else:
            d1[key] = value
    return pickle.dumps(d1, protocol=pickle.HIGHEST_PROTOCOL )

if __name__ == "__main__":
    window_sz = sys.argv[1]
    p = multiprocessing.Pool(100)
    c = collections.deque( p.map(partial(cs_wrapper, window_sz=window_sz ), range(0,99) ) )

    while( len(c) >= 2 ):
        first = c.pop( )
        second = c.pop( )
        d = reduce( first, second )
        c.appendleft( d )
        
    final = c.pop( )
    print( pickle.loads(final ))
