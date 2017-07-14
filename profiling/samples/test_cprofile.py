

import cProfile
import pstats


def label(code):
    if isinstance(code, str):
        return ('~', 0, code)    # built-in functions ('~' sorts at the end)
    else:
        return (code.co_filename, code.co_firstlineno, code.co_name)

    
if __name__ == "__main__":

    s = cProfile.Profile()

    s.enable( )
    print(2+1)
    s.disable( )

    entries = s.getstats( )
    self.stats = {}
    callersdicts = {}

    # call information
    for entry in entries:
        print(label(entry.code))
        print(entry.callcount)          # ncalls column of pstats (before '/')
        print(entry.callcount - entry.reccallcount) # ncalls column of pstats (after '/')
        print(entry.inlinetime)         # tottime column of pstats
        print(entry.totaltime)          # cumtime column of pstats
        print( )
        callers = {}
        callersdicts[id(entry.code)] = callers
        self.stats[func] = cc, nc, tt, ct, callers

    # subcall information
    for entry in entries:
        if entry.calls:
            func = label(entry.code)
            print(func)
            for subentry in entry.calls:
                try:
                    #callers = callersdicts[id(subentry.code)]
                    print("Try: ", id(subentry.code))
                    callers = callersdicts[id(subentry.code)]
                except KeyError:
                    continue
                print( subentry.callcount)
                print( subentry.callcount - subentry.reccallcount)
                print( subentry.inlinetime)
                print( subentry.totaltime)
                if func in callers:
                    prev = callers[func]
                    print(prev)
                #callers[func] = nc, cc, tt, ct




    
# import cProfile
# cProfile.run("print(2+1)")

# def print_line(self, func):  # hack: should print percentages
#         cc, nc, tt, ct, callers = self.stats[func]
#         c = str(nc)
#         if nc != cc:
#             c = c + '/' + str(cc)
#         print(c.rjust(9), end=' ', file=self.stream)
#         print(f8(tt), end=' ', file=self.stream)
#         if nc == 0:
#             print(' '*8, end=' ', file=self.stream)
#         else:
#             print(f8(tt/nc), end=' ', file=self.stream)
#         print(f8(ct), end=' ', file=self.stream)
#         if cc == 0:
#             print(' '*8, end=' ', file=self.stream)
#         else:
#             print(f8(ct/cc), end=' ', file=self.stream)
#         print(func_std_string(func), file=self.stream)

