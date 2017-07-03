from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("sin_cython", ["sin_cython.pyx"])]

setup(
    name="cython_sin_app",
    cmdclass = {'build_ext':build_ext},
    ext_modules = ext_modules
)
