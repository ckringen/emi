
# can't get this one to work

import sys
from os.path import isdir
from importlib import invalidate_caches
from importlib.abc import SourceLoader
from importlib.machinery import FileFinder


class MyLoader(SourceLoader):
    def __init__(self, fullname, path):
        self.fullname = fullname
        self.path = path
        print("inside myloader",fullname, path)
        
    # def create_module(self, spec):
    #     print("inside create_module")
    #     return None # use default module creation semantics

    
    # def exec_module(self, module):
    #     print("inside exec_module")
    #     with open(self.filename) as f:
    #         data = f.read()
    #     # manipulate data some way...
    #     exec(data, vars(module))

        
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


loader_details = MyLoader("benchmark_test","."), [".py"]

def install():
    # insert the path hook ahead of other path hooks
    sys.path_hooks.insert(0, FileFinder.path_hook(loader_details))
    # clear any loaders that might already be in use by the FileFinder
    sys.path_importer_cache.clear()
    invalidate_caches()

    #import benchmark_test
