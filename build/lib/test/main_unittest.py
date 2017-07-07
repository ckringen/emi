
import unittest
import sys

from src import count_skipgrams as skip


class count_skipgramTest( unittest.TestCase ):

    def setUp(self):
        pass
            
    # # tokenize battery
    def test_tokenize_SmallString(self):
        s = "the dog ran quickly across the field"
        produced = skip.tokenize( s )  
        target = ['<s>', 'the', 'dog', 'ran', 'quickly', 'across', 'the', 'field', '</s>']
        self.assertEqual( produced, target )

        
    def test_tokenize_EmptyString(self):
        s = ""
        produced = skip.tokenize( s )  
        target = ['<s>','</s>']
        self.assertEqual( produced, target )

        
    def test_tokenize_NonAscii(self):
        s = "Hark, a string with an extended charset µ !"
        produced = skip.tokenize( s )  
        target = ['<s>', 'Hark,', 'a', 'string', 'with', 'an', 'extended', 'charset', 'µ', '!', '</s>']
        self.assertEqual( produced, target )


    def test_tokenize_LineEndings(self):
        s = "What is \nthis, \r\nlatin-1?"
        produced = skip.tokenize( s )  
        target = ['<s>', 'What', 'is', 'this,', 'latin-1?', '</s>'] 
        self.assertEqual( produced, target )
    
    
    # # not sure how to test this
    # def test_ichunks_SmallString(self):
    #     s = "the dog ran quickly across the field".split( )
    #     islice_generator = skip.ichunks(s,3)
    #     ans = ['<s>', 'What', 'is' ]

    #     ctr = 0
    #     for i in ans:
    #         for j in i:
    #             self.assertEqual( j, ans[ctr])
    #             ctr += 1

        
                
    def tearDown(self):
        pass


        
if __name__ == "__main__":
    
    unittest.main( )

