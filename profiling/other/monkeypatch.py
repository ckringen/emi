
# If I did this, I'd be profiling the test, as opposed to the underlying function, which I don't
# necessarily want to do.  Interesting though.

'''
Created on Mar 31, 2011
@author: Nabil Stendardo
'''

import unittest
import simpleFunction

def noop(*args,**kwargs):
    pass

def modify_class(cls,name=None,default=noop):
    """
    Modify an class attribute/method.
    
    This decorator factory returns a decorator which modifies on the fly (i.e. monkeypatches)
    the class "cls" by adding or replacing the attribute (typically method) indicated by the
    variable "name" (which defaults to the name of the wrapper function) with the result 
    of the decorated function, to which is passed as only parameter the old attribute with the same name
    (or a default value, by default a dummy function, if none exists).
    
    @param cls: the class to modify
    @param name: the name of the attribute/method to modify in the class 
    (defaults to the decorated function name)
    @param default: the value which is passed to the decorated function if there is no
    attribute named 'name' in 'cls' (defaults to a dummy function)
    @return: a decorator  
    """
    def wrapper(fn):
        """
        The actual decorator returned by modify_class, which actually modifies the class.
        
        @param fn: the function to decorate
        @return: the argument function.
        """
        if name is None:
            name_ = fn.__name__
        else:
            name_ = name
        original_method = getattr(cls,name_,default)
        new_method = fn(original_method)
        setattr(cls,name_,new_method)

        print( name_, original_method, new_method )

        return fn
    return wrapper



class TestModifyClass(unittest.TestCase):

    def test_modifyClass(self):

        class Foo(object):

            def baz(self):
                return 0
            
            def bar(self,argument):
                return argument**2

        foo = Foo() # Note: the foo object is instantiated BEFORE the class modification 

        @modify_class(Foo)
        def baz(parent):
            def baz(self,argument):
                return self.bar(argument)
            return baz

        @modify_class(Foo)
        def bar(parent):
            def bar(self,argument):
                return parent(self,argument) * 3
            return bar

        @modify_class(Foo,'bar')
        def toto(parent):
            def bar(self,argument):
                return parent(self,argument) + 1
            return bar

        for i in range(25):
            self.assertEqual(foo.baz(i),(i**2)*3+1)

            
if __name__ == '__main__':
    unittest.main()
