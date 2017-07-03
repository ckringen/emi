

# can't import f if it's defined using "cdef"
#from sin_cython import integrate_f

#from sin_cython import integrate_f, f

from sin_cython import Function, SinOfSquareFunction, integrate

if __name__ == "__main__":

    #print(integrate_f(.1, .001, 10000))

    print(integrate(SinOfSquareFunction(), 0, 1, 10000))
