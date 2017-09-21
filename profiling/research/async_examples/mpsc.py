
import pickle
import multiprocessing
import collections

import src.count_skipgrams as skip

def cs_wrapper( idx ):
    f = open("data/en.{}.txt".format(idx), "r")
    return skip.main2( f, 2 )

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

    p = multiprocessing.Pool(5)
    c = collections.deque( p.map(cs_wrapper, range(0,5) ) )

    while( len(c) >= 2 ):
        first = c.pop( )
        second = c.pop( )
        d = reduce( first, second )
        c.appendleft( d )
        
    final = c.pop( )
    print( pickle.loads(final ))
