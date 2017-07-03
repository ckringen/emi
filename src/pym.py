""" Pitman-Yor Mixture entropy estimation 

Just an interface to the MATLAB code: https://github.com/pillowlab/PYMentropy

@article{archer2014bayesian,
  author  = {Evan Archer and Il Memming Park and Jonathan W. Pillow},
  title   = {Bayesian Entropy Estimation for Countable Discrete Distributions},
  journal = {Journal of Machine Learning Research},
  year    = {2014},
  volume  = {15},
  pages   = {2833-2868},
}
"""
import math

import pymatbridge

PYM_PATH = "/Users/canjo/src/PYMentropy/src/"

LOG2 = math.log(2)
INF = float('inf')

M = pymatbridge.Matlab()
M.start()

class MatlabException(Exception):
    pass

def matlabfunc(path, nargout):
    def f(*args):
        result_obj = M.run_func(path, *args, nargout=nargout)
        if result_obj['success']:
            return result_obj['result']
        else:
            raise MatlabException(result_obj)
    return f

multiplicitiesFromCounts = matlabfunc(PYM_PATH + "multiplicitiesFromCounts.m", 2)
computeH_PYM = matlabfunc(PYM_PATH + "computeH_PYM.m", 2)

def entropy(xs):
    """ Entropy estimate from a sequence of counts according to the 
    Pitman-Yor Mixture from Archer, Memming & Park (2014).

    In bits.  
    
    Caveats:
    * Sequence must have length > 1.
    * If sequence is all 1s, then estimated entropy is infinite.
    """
    the_entropy, _ = entropy_nats_with_variance(xs)
    return the_entropy / LOG2

def entropy_nats_with_variance(xs):
    """ Entropy estimate from a sequence of counts according to the
    Pitman-Yor Mixture from Archer, Memming & Park (2014), along
    with the variance of the estimate. 

    In nats.

    Caveats:
    * Sequence must have length > 1.
    * If sequence is all 1s, then estimated entropy is infinite.
    """
    mm, icts = multiplicitiesFromCounts(xs)
    result = computeH_PYM(mm, icts, {}, False)
    if isinstance(result, str) and "JSON does not allow non-finite" in result:
        return INF, INF
    else:
        return result

def main(*args):
    print(entropy(list(map(int, args))))

if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
