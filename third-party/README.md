
The profiling done in this emi package allows you to use line_profiler and memory_profiler, which
are two third-party libraries which can be found in the pypi system.

+ [line profiler](https://pypi.python.org/pypi/line_profiler/)
+ [memory profiler](https://pypi.python.org/pypi/memory_profiler)

The usual way to get at these files is to:

1. untar/zip them
2. navigate to their root proj directory
3. install them into your PYTHON_PATH by doing:

$ python setup.py build
$ python setup.py install

But this installs the files globally on your machine, which may be dispreferred.  An alternative way to keep track of
these sorts of things is by using a virtual machine.  However, I have opted for a third option is to build them
inside this project, i.e. refrain from installing them in the PYTHON_PATH, and then modify setup.py to tell it where the
modules may be found (in the dependencies/ directory) which then allows them to be treated as
just any other modules to import.
