
# # can wrap the native python version of "sin"
# from math import sin
# def f(x):
#     return sin(x**2)

# # -------------------------------------------------------------------

# or import the C version; need to redeclare since cython doesn't parse headers
cdef extern from "math.h":
    double sin(double)

cdef double f(double x):
    return sin(x*x)


# def integrate_f(double a, double b, int N):

#     cdef int i
#     cdef double s, dx
#     s = 0
#     dx = ( b - a )/N

#     for i in range(N):
#         s += f(a+i*dx)
#     return s*dx

# # -----------------------------------------------------------------

# we need to have the evalute method inherit from Function
# lest Python use the slower version -> unsure why though
cdef class Function:
    cpdef double evaluate(self,double x) except *:
        return 0

cdef class SinOfSquareFunction(Function):
    cpdef double evaluate(self,double x) except *:
        return sin(x*x)

# if f were not typed, Python would use the slower version
def integrate(Function f, double a,double b, int N):
    cdef int i
    cdef double s, dx
    if f is None:
        raise ValueError(" f cannot be None " )
    s = 0
    dx = (b-a)/N
    for i in range(N):
        s = f.evaluate(a+i*dx)
    return s*dx
