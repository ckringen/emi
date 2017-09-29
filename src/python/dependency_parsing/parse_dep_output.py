
# walk ascii output of dependency parser for collecting path length counts

import cPickle
import sys
import collections
import itertools

flat = itertools.chain.from_iterable

def readPMPF( src ):
    p_string = [ ]

    # gzip src
    while True:
        l = src.readline( )
        if l:
            if len(l) > 1:                     
                line = l.lower( ).strip( ).split( )                
                line = [ line[ 0 ], line[ 1 ], line[ 7 ], line[ 6 ] ]
                p_string.append( line )
            else:
                yield parsePMPF( p_string )
                p_string = [ ]
        else:
            break
        
    # for line in src:
    #     try:
    #         line = line.lower( ).strip( ).split( )
    #         if line:
    #             line = [ line[ 0 ], line[ 1 ], line[ 7 ], line[ 6 ] ]
    #             p_string.append( line )
    #         else:
    #             yield parsePMPF( p_string )
    #             p_string = [ ]
    #     except (IndexError, TypeError) as e:
    #         print("error: ", line)
                
def parsePMPF( p_list ):
    nodes = { "0" : "ROOT" }
    edges = [ ]
    for i in p_list:
        nodes[i[0]] = i[1]
        edges.append([i[0],i[3]])
    for e in edges:
        f = nodes[e[0]]
        s = nodes[e[1]]
        e[0] = f
        e[1] = s        
        yield [(e[0], e[1])] 
        
def countPaths( deq ):
    grams = flat( deq )    
    counts = collections.Counter(grams) 
    return counts
    
def main( file_handle ) :    
    deq = collections.deque(flat( readPMPF( file_handle ))  )
    c = countPaths( deq )
    b = cPickle.dumps(c, protocol=cPickle.HIGHEST_PROTOCOL)
    return b
