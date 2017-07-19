
# run performance tests over select functions from the source code, e.g.
# in the src module; each func needs a "profile" decorator, and so to avoid
# modifying and unmodifying the src code directly for each performance run, we
# change the abstract syntax tree of the src code at import to add the decorator
# statements, and use the altered version of the syntax tree here, leaving the src
# module alone where it is

import ast
import unparse  # third-party lib
import src
    
class simpleVisitor( ast.NodeVisitor ):

    def generic_visit(self,node):
        ast.NodeVisitor.generic_visit(self,node)
    
    def visit_Module(self,node):
        ast.NodeVisitor.generic_visit(self,node)
    
    def visit_Name(self,node):
        ast.NodeVisitor.generic_visit(self,node)
    
    def visit_If(self,node):
        ast.NodeVisitor.generic_visit(self,node)

    def visit_Str(self,node):
        print(node.s)
        ast.NodeVisitor.generic_visit(self,node)

    def visit_FunctionDef(self, node):        
        print(type(node).__name__)
        print("item is:", node, type(node))
                                
        for i in node.__dict__:   #.body
            print("decorator list: ", i, node.__dict__[i])

        ast.NodeVisitor.generic_visit(self,node)


# unsure when I need to call generic_visit; doc for ast says to do so if there's kids?
class simpleTransformer( ast.NodeTransformer ):

    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)
    
    def visit_Module(self, node):
        ast.NodeVisitor.generic_visit(self, node)
    
    def visit_Name(self, node):
        ast.NodeVisitor.generic_visit(self, node)
    
    def visit_If(self, node):
        ast.NodeVisitor.generic_visit(self, node)
    
    def visit_FunctionDef(self, node):        
        ast.NodeVisitor.generic_visit(self, node)

        dl = node.decorator_list
        if len(dl) > 0:
            dl[0].id = "profile"

        # unsure what to return; this is the example in the ast doc
        # return copy_location(Subscript(
        #     value=Name(id="profile", ctx=Load()),
        #     slice=Index(value=Str(s=node.id)),
        #     ctx=node.ctx
        # ), node)

        return node
    
    
                            
# really useful pretty-printing functions
def str_node(node):
    if isinstance(node, ast.AST):
        fields = [(name, str_node(val)) for name, val in ast.iter_fields(node) if name not in ('left', 'right')]
        rv = '%s(%s' % (node.__class__.__name__, ', '.join('%s=%s' % field for field in fields))
        return rv + ')'
    else:
        return repr(node)

def ast_visit(node, level=0):
    print('  ' * level + str_node(node))
    for field, value in ast.iter_fields(node):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, ast.AST):
                    ast_visit(item, level=level+1)
        elif isinstance(value, ast.AST):
            ast_visit(value, level=level+1)
            


if __name__ == "__main__":

    # grab the library as a simple string; better way?
    pyth = open("simpleFunction.py", 'r')
    syntax = pyth.read( )
    node = ast.parse( syntax )

    # visit the src code string 
    simpleVisitor( ).visit(node)
    simpleTransformer( ).visit(node)
    node = ast.fix_missing_locations(node)   # unsure when I need to do this

    # syntax error?
    #exec compile(node, '<string>', 'exec')


    # this seems to work??
    print(astunparse.dump(node))


    # good pretty-printer
    # ast_visit(node)


