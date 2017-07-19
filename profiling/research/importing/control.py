
# run set of benchmark functions, appropriately decorated
# to be called (I think) by runProf.sh in the project root

from ArgParser import parseCommandLine
import hook        # redefines import func, so either use it last or, figure out how to do "from lib import func" with it
 

if __name__ == "__main__":

    # args is a list of lists, where each sublist is a set of functions, with the position of
    # each list determining which profiler it is; should probably change... 
    args = parseCommandLine( )
    
    new_exClass = hook.custom_import( "exClass",  args )   # pass in functions here to decorate
    new_exClass.run( )




    # today = datetime.date.today( ).strftime('%Y%m%d')
    
    # # args is a list of lists, where each sublist is a set of functions, with the position of
    # # each list determining which profiler it is; should probably change... 
    # args = parseCommandLine( )
    # designated_benches = [ i for i in itertools.chain.from_iterable(args)]
    
    # benchmarks = hook.custom_import( "benchmarks",  args ) 
    # bench_functions = []
    # for item in benchmarks.__dict__:
    #     if item in designated_benches:
    #         bench_functions.append(benchmarks.__dict__[item])

    # print(bench_functions)
            
    # # # I want some global run function, i.e. benchmarks.run( ) which runs the select functions.  could probably
    # # # put benchmarks in a class and add such a function
    # for b in bench_functions:
    #     if None:
    #         break
    #     else:
    #         outfilename = "{0}_{1}.perf".format(today,b)
    #         print(outfilename)

    #         # further need a benchmark class so we can do setup like the following...
    #         f = open('SampleData/large_file.txt', 'r+b')
    #         m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

            
    #         elapsed = b( m, outfilename )
    #         print(elapsed)
