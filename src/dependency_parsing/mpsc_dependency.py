
import gzip
import os
import mmap
import cPickle
import multiprocessing
import collections

import parse_dep_output as pdo

def pdo_wrapper( idx ):

    #f = open("small_dep{}.txt.gz".format(idx), 'rb')

    data_dir = "/om/user/ckringen/data/parsing2/"
    files = os.listdir(data_dir)
    f = open(data_dir + files[idx], "rb")
        
    mapped = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
    gzfile = gzip.GzipFile(mode="r", fileobj=mapped)

    return pdo.main( gzfile )

def reduce( b1, b2 ):
    d1 = cPickle.loads(b1)
    d2 = cPickle.loads(b2)        
    for key, value in d2.items( ):
        if key in d1:
            d1[key] += value
        else:
            d1[key] = value
    return cPickle.dumps(d1, protocol=cPickle.HIGHEST_PROTOCOL )

if __name__ == "__main__":

    # myobj = cPickle.loads( pdo_wrapper(0) )
    # for key, count in myobj.items( ) :
    #     print("{0} {1}\t{2}".format(key[0], key[1], count))
    
    p = multiprocessing.Pool(94)
    c = collections.deque( p.map(pdo_wrapper, range(0,93) ) )

    while( len(c) >= 2 ):
        first = c.pop( )
        second = c.pop( )
        d = reduce( first, second )
        c.appendleft( d )
            
    outf = gzip.open('dependency_full.pkl.gz','wb')
    obj = cPickle.loads(c.pop( ))
    cPickle.dump(obj, outf)
    outf.close( )

    # final = c.pop( )
    # c = cPickle.loads(final )
    # for key, count in c.items( ) :
    #     print("{0} {1}\t{2}".format(key[0], key[1], count))
