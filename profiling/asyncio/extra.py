        # import time
    # a = time.time( )
    # myiter = itertools.islice(sys.stdin, 100000)
    # tokens =  map(tokenize, myiter)
    # # print([i for i in tokens])   # for sure just returns tokenized version

    # skips = map(getSkipgrams, tokens)     #returns an iterable holding a generator    

    # # consumes generator object before flat(skips) can see it; produces the same thing
    # # for i in skips:
    # #     for j in i:
    # #         print("j is: ", j)

    # # print(type(skips))
    # sk = flat(skips)    
    # # print(type(sk))
          
    # # for k in flat(skips):
    # #     print("k is ", k)
    
    # c = Counter(sk)            # triggers the getSkipgrams function
    #                            # looks like the map function just assigns a getskipgrams generator func to the tokens iterable?
                               
    # # for k,v in c.items():
    # #     print(k, " : ", v)
    # #     for j in k:
    # #         print(j, " : ", v)

    
    # # text = "Here Here is is is a a a a is a is a fairly good good fairly example of example of a piece of text of text."
    # # main2( 1, text, 100000 )
    # b = time.time( )
    # print(b-a)
