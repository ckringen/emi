
# exposes the source of the module as just the file itself, prompting the user
# to read it in as a string, and then modify, say via AST, or something else
# kind of expected something different... seems like I could could do the same
# thing bypassing the metapath by just reading in the file.
# must be something I'm not getting.

import sys
import os.path
from inspect import getmembers, isclass, ismethod

from importlib.abc import Loader, MetaPathFinder, InspectLoader, SourceLoader
from importlib.util import spec_from_file_location

class MyMetaFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        print("find_spec getting called")

        if path is None or path == "":
            print("top level import")
            path = [os.getcwd()] # top level import -- 
        if "." in fullname:
            print(". in name")
            *parents, name = fullname.split(".")
        else:
            name = fullname
            print("name = fullname", name)
        for entry in path:
            print("entry is ", entry )
            if os.path.isdir(os.path.join(entry, name)):
                # this module has child modules
                print("we have hcild modules")
                filename = os.path.join(entry, name, "__init__.py")
                submodule_locations = [os.path.join(entry, name)]
            else:
                filename = os.path.join(entry, name + ".py")
                submodule_locations = None
                print("filename is ", filename)
            if not os.path.exists(filename):
                print("does not exist")
                continue

            return spec_from_file_location(fullname, filename, loader=iLoader(filename),
                submodule_search_locations=submodule_locations)

        return None # we don't know how to import this

class MyLoader(Loader):
    def __init__(self, filename):
        self.filename = filename
        print("inside loader ",self.filename)

    def create_module(self, spec):
        print("inside create_module")
        return None # use default module creation semantics

    
    # here, "module" is the loader object
    # we need to pass the string object read from the __file__ attr
    # to exec so it can become reified as a module object
    def exec_module(self, module):
        print("inside exec_module")

        with open(self.filename) as f:
            data = f.read()
        exec(data, vars(module))

        
class iLoader(SourceLoader):
    def __init__(self, filename):
        self.filename = filename
        print("inside loader ",self.filename)

    def create_module(self, spec):
        print("inside create_module")
        return None # use default module creation semantics

    def exec_module(self, module):
        print("inside exec_module")

        # print(type(module.__file__))
        
        # for n,v in getmembers(module):
        #     print(n,v)
        
        #add_attr(module, "bench_read_mmap")
        
        # manipulate data some way...
        with open(self.filename) as f:
            data = f.read()
            
        # why do I need to exec this? and what's vars?
        exec(data, vars(module))

    def get_code( self, fullname):
        print("inside get code")

    def get_source( self, fullname ):
        print( "inside get_source")

    def get_filename(self, fullname):
        print("inside get_filename")
        return self.path

    
    def get_data(self, filename):
        """exec_module is already defined for us, we just have to provide a way
        of getting the source code of the module"""
        print("get data getting called")
        with open(filename) as f:
            data = f.read()
            print(data)
        # do something with data ...
        # eg. ignore it... return "print('hello world')"
        return data
        
        
def install():
    """Inserts the finder into the import machinery
        gets called by main.py to """
    print("inside install")
    sys.meta_path.insert(0, MyMetaFinder())

    import benchmark_test

    #add_attr(benchmark_test, "bench_mmap_file")

    b = benchmark_test.benchmark( "myfunc" )
    b.bench_read_mmap("myout.txt")

    # return benchmark_test

