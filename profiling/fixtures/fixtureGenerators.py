
import collections
import itertools

import benchmarking


def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        next( cr )
        return cr
    return start


class benchGenerator( benchmarking.BenchFixture ):

    def __init__( self ):
        self.f = ""
        self.deq = None
        self.window_size = 2
        self.setUp( )
            
    def setUp( self ):
        self.deq = collections.deque( )
        self.window_size = 2
        self.f = open("/home/aik/PersonalProjects/Building46/emi/profiling/SampleData/large_file.txt", "r")
    
    def tearDown( self ):
        pass
    
    def read_mmap( self, target ):

        print("file is: ", self.f)

        buffer_size = 10
        while True:
            buf = self.f.read(buffer_size)
            if not buf:
                break

            # #this either has a bug, or is just super slow
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
    def tokenize( self ): #target ):
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
                pass
        
    @coroutine
    def loadOnQueue( self, target ):
        while True:
            element = (yield)
            if len(deq) < 8:
                deq.append( element )
            elif len(deq) == 8:
                print(deq)
                target.send( deq )
                deq.popleft( )

    @coroutine
    def skipgram(self):#,target):
        while True:
            line = (yield)           
            line = line.split()
            try:
                while line:
                    self.deq.append([(line[0],line[self.window_size])])
                    del line[0]
            except IndexError as e:
                pass
            
    @coroutine
    def count( self ):
        while True:
            line = (yield)
            c.update( line )


    def runPipe( self, outfilename ):
        self.read_mmap(
                   self.skipgram( ) )
        
        grams = itertools.chain.from_iterable( self.deq )
        c = collections.Counter( grams )

        
if __name__ == '__main__':
    benchmarking.Benchmark( )
