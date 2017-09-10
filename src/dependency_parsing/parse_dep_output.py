
# walk ascii output of dependency parser for collecting path length counts

import sys
import collections
import itertools
#from graphviz import Digraph


flat = itertools.chain.from_iterable

def ichunks(iterable, size):
    while True:
        yield itertools.islice(iterable, size)        

def run(lines, k):

    assert k >= 0
    window_size = k + 2

    def get_skipgrams(xs): 
        
        its = itertools.tee(xs, window_size)   # so xs is an iterable, such that it can return an iterator
        for i, iterator in enumerate(its):
            for _ in range(i):
                next(iterator)

        # for i in zip(*its):
        #     print(i)
        #     print(i[0], i[-1])
        # print("outside")

        for block in zip(*its):
            # tup = (block[0], block[-1])
            # ct = collections.Counter(tup)
            # print(ct)            
            #print( "blocks: ", block[0], block[-1], type(block[0]), type(block))
            
            yield block[0], block[-1]                          # "window_size-skip-bigrams", e.g. 4-skip-2-grams

    grams = flat(map(get_skipgrams, map(tokenize, lines)))
    counts = collections.Counter(grams) 
    
    return counts.items()


def main( k, s=None ):
    #err("Beginning skipgram counts")
    k = int(k)
    
    if s is None:
        chunks = [sys.stdin]
    else:
        s = int(s)
        chunks = ichunks(sys.stdin, s)

    for chunk in chunks:
        err("Counting skipgrams...")
        result = run(chunk, k)
        #err("Printing %s skipgrams..." % len(result))
        if result:
            print("done")
            for key, count in result:
                print(" ".join(key), count, sep="\t")
        else:
            break


def readPMPF( filename, graph=False ):
<<<<<<< HEAD
    with open( filename, "r" ) as f:
        p_string = [ ]
        for line in f:
            try:
                line = line.strip( ).split( )
                if line:
                    line = [ line[ 0 ], line[ 1 ], line[ 7 ], line[ 6 ] ]
                    p_string.append( line )
                else:
                    parsePMPF( p_string )
                    if graph:
                        createDotGraph( p_string )
                    p_string = [ ]
            except IndexError as e:
                print("error: ", line)

    # with open( filename, "r" ) as f:
    p_string = [ ]
    for line in sys.stdin:
        try:
            line = line.strip( ).split( )
            if line:
                line = [ line[ 0 ], line[ 1 ], line[ 7 ], line[ 6 ] ]
                p_string.append( line )
            else:
                #print(p_string)
                parsePMPF( p_string )
                # if graph:
                #     createDotGraph( p_string )
                p_string = [ ]
        except IndexError as e:
            print("error: ", line)


            # need to flsuh the leftover bits if we didn't reach another 1
            #print("final p_string: ", p_string)

                
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
        
        deq.append( [(e[0], e[1])] )               # how should we do this part?

        deq.append( [(e[0], e[1])] )               # so here's the main question, how should we do this part?


        
def countPaths( deq ):
    grams = flat( deq )
    counts = collections.Counter(grams) 
    return counts


# def createDotGraph( p_list ):
#     dot = Digraph( comment= "dep_graph" )
#     for i in p_list:
#         dot.node( i[ 0 ], label=i[ 1 ] + ":" + i[ 2 ] )
#         dot.edge( i[ 3 ], i[ 0 ] )
#     dot.render( "dep_graph.gv" )

    
if __name__ == "__main__":

    deq = collections.deque( )

    readPMPF( "../../profiling/SampleData/sample_dep_parses.txt", graph=False )
    
    c = countPaths( deq )

    for key, count in c.items( ) :
        print("{0} {1}\t{2}".format(key[0], key[1], count))

