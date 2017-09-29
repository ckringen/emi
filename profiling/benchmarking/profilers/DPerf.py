
# decorator cass, wrapper around stdlib disassembler

import dis

class DPerf( ):
    ''' 
    global state object to hold all benchmark functions, plus some utility
    methods for running and formatting according to bytecode
    '''    
    
    def __init__(self, function, out="logging.out"):
        ''' registers a function in the overall state object '''
        self.func = function

    def __call__( self, *args ):
        ''' instance of class getting called triggers this, i.e. a decorated function '''
        outf = self.getFilestream( *args )
        dis.dis(self.func,file=outf)

    def getFilestream( self, output ):
        f = open(output, "w")
        return f
            

