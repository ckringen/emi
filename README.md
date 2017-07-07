
The EMI project
===============

Overview
---------
This project exists to profile python code used in a Natural Language Processing project.


Organization
-------------
The directory structure is as follows: 

emi/
	+-- build
	|
	+-- data
	|
	+-- dependencies
	|
	+-- dist
	|
	+-- emi.egg-info
	|
	+-- profiling
	|
	+-- README
	|
	+-- runProf.sh
	|
	+-- runTests.sh
	|
	+-- setup.py
	|
	+-- src
	|  
	+-- test
	|
	+-- todo.org

with the major components simply being the src/, test/, and profiling/ directories.  With test/, I will attempt to follow,
at least minimally, a test-driven development style, e.g. writing a failing test, writing the minimal necessary code to fix the
failing test, then moving on.

For profiling/, work has gone into investigating how we should best profile code for performance.  To that end, I have 
included basic support for the cProfile library which ships with python's standard lib.  I have also included 
two third-party libraries, line_profiler and memory_profiler, which provide more textured information about the runtime 
behavior and memory usage of a given program.  


Setup
-----
Treating the emi project as a module, in good python fashion, means including a setup.py script in the root.  Practically,
this means that we can have subdirectories (with __init__.py files) refer to each other without touching the PYTHON_PATH
variable, so we can tell python where to find our libraries.  This, however, is more of a side-effect of the overall setup.py
philosophy, which looks further ahead to deployment and shipping logistics.  Thus the main output of running
setup.py is the creation and population of the build/, dist/, and emi.egg-info/ directories, which make the root look 
busier than it really is.  

Although we're pushing (we've pushed) a version of the emi project that has already been "set up", you may periodically refresh
the state of the project by running the following from the root, as per any pyPI package:

$ python setup.py build
$ python setup.py install


Usage
-----
At the outset, or after making any changes to the project, you should run the following:

$ runTests.sh

which will hopefully tell you if you broke anything.  Test support is currently flimsy and more demonstrative than useful, that
is, there's very low coverage.

To track how well the program is running, you will want to make use of the runProf.sh script.  This has been written as a small
unix utility, accepting a few command line arguments (choose which profiler, which functions to profile).  It simply passes
those arguments to a python script, which is written largely identically to the test script.

Still working out some kinks.

Overall, we will probably hone in on a single use-case for the profiling, and it could be that most of the intended features
are dropped in favor of a simpler but more direct profiling methodology.  


Miscellaneous
-------------
I keep track of goals and progress in the todo.org file kept in the root directory.  Org-mode is a language built inside
emacs that offers support for formatting book-keeping files, such as to-do lists.  In emacs, this means there's a lot of
interactivity that comes out of the box, e.g. displaying and contracting lists, headings, moving around the file like its
a directory editor, etc. which get lost in any other text editor, or even an older version of emacs.

*a moment of silence for those peope not using emacs*.

If you don't care about those facets of the project (which you probably don't), then feel free to ignore it.  


Contact Info
-------------

+ Richard Futrell : futrell@mit.edu

+ Chad Kringen : kringen1@gmail.com