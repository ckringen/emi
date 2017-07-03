""" Given a counts file and a vocab file resulting from kenlm,
this script will turn it into a tab-separated N-gram counts file """    

import sys
import itertools

import rfutils

NGRAM_TOKEN_SIZE = 4
COUNT_SIZE = 8

def read_vocab_file(filename):
    # KH yue: "The vocab file is null-delimited strings in order of vocab id."
    with open(filename, 'rb') as infile:
        data = infile.read()
    return data.decode().split('\x00')

def decode_number(bytes):
    result = 0
    for i, byte in enumerate(bytes):
        result += 16**(2*i) * byte
    return result
            
def decode_block(block, vocab):
    ngram, count = block[:-8], block[-8:]
    return decode_ngram(ngram, vocab), decode_count(count)

decode_count = decode_number

def decode_ngram(ngram, vocab):
    def gen():
        for word in rfutils.blocks(ngram, NGRAM_TOKEN_SIZE):
            yield vocab[decode_number(word)]
    return tuple(gen())

def read_ngram_file(filename, vocab, order):
    # KH yue: "Each n-gram is an array of 4-byte vocab ids and then a 64-bit
    # count. So if you request 5-grams, each record is 28 bytes: 5 4-byte
    # vocabulary ids and an 8-byte count. n-grams are sorted in suffix order
    # using their vocabulary ids.
    block_size = NGRAM_TOKEN_SIZE * order + COUNT_SIZE
    with open(filename, 'rb') as infile:
        while True:
            block = infile.read(block_size)
            if block:
                yield decode_block(block, vocab)
            else:
                break

def main(ngram_file, vocab_file, order):
    order = int(order)
    vocab = read_vocab_file(vocab_file)
    ngram_counts = read_ngram_file(ngram_file, vocab, order)
    for ngram, count in ngram_counts:
        print("%s\t%s" % (" ".join(ngram), str(count)))

if __name__ == '__main__':
    try:
        main(*sys.argv[1:])
    except TypeError:
        print("Usage: python3 materialize_kenlm_ngrams.py counts_file vocab_file order")
