#@CPerf
def bench_ichunks( outfile ):
    s = "dog's running real fast, I tell you hwat"
    count_skipgrams.ichunks( s, 3 )


#@CPerf
def bench_tee( outfile ):
    its = itertools.tee(xs, window_size)
    for i, iterator in enumerate(its):
        for _ in range(i):
            next(iterator)

            
#@CPerf
def bench_tokenizeSmallString( outfile ):
    s = "dog's running real fast, I tell you hwat"
    count_skipgrams.tokenize( s )
    

#@CPerf
def bench_islice( outfile ):
    myiter = itertools.islice(sys.stdin, 100000)

    
#@CPerf
def bench_flat( outfile ):
    lst = [['a','b'],'c',['d'], [['e','f'],['g'],['h']],'i',[[[[[['j']]]]]]]
    itertools.chain.from_iterable( lst )

    
#@CPerf
def bench_from_iterable( outfile ):
    grams = flat(map(get_count_skipgrams, map(tokenize, lines)))

    
#@CPerf
def bench_get_skipgrams( outfile ):
    tokens = ['<s>', 'Here', 'Here', 'is', 'is', 'is', 'a', 'a', 'a', 'a', 'is', 'a', 'is', 'a', 'fairly', 'good', 'good', 'fairly', 'example', 'of', 'example', 'of', 'a', 'piece', 'of', 'text', 'of', 'text.', '</s>']
    gen = map(count_skipgrams.get_skipgrams, tokens)
