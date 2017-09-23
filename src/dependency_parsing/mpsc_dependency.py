
from functools import partial
import pickle
import multiprocessing
import collections

import parse_dep_output as pdo

def pdo_wrapper( idx ):
    f = open("small_dep{}.txt".format(idx), "r")
    return pdo.main( f )

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
    
    p = multiprocessing.Pool(2)
    c = collections.deque( p.map(pdo_wrapper, range(0,2) ) )

    while( len(c) >= 2 ):
        first = c.pop( )
        second = c.pop( )
        d = reduce( first, second )
        c.appendleft( d )
        
    final = c.pop( )
    print( pickle.loads(final ))
    # for key, count in c.items( ) :
    #     print("{0} {1}\t{2}".format(key[0], key[1], count))
