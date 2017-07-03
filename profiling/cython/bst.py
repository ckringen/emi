
# implement a binary search tree in pure python

class node( ):
    ''' a node is an container, holding an integer value along with two "pointers" 
        each to another node, one whose value is less than the current one,
        and one whose value is greater
    '''
    def __init__( self, val=0, greater=None, lesser=None ):
        self.val = val
        self.nextNode = greater  # another node object, or None
        self.prevNode = lesser
        
    # these should all have try/catch exceptions
    def getVal( self ):
        return self.val
    
    def getNext( self ):
        return self.nextNode.getVal()
    
    def getPrev( self ):
        return self.prevNode.getVal()
    
    def setVal( self, val ):
        self.val = val
        
    def setNext( self, node ):
        self.nextNode = node
        
    def setPrev( self, node ):
        self.prevNode = node
        
        
class BST( ):
    ''' an implementation of a binary search tree '''
    def __init__( self, root=None ):
        first = True
        if isinstance(root, list):
            for i in root:
                if first == True:
                    self.root = node(i)
                    first = False
                else:
                    n = node(i)
                    self.insert(n)
        else:
            self.root = root
    
    # current = node we're visiting/sitting on, fromRoot flags whether or not 
    # we start from the object's root node determined in the init methods, or some other node
    def traverse( self, current=None, fromRoot=True):
        ''' print elements in sorted "inorder" fashion '''
        if fromRoot == True:
            current = self.root
            fromRoot = False
        if current != None:
            self.traverse( current.prevNode, fromRoot )
            print(current.getVal())
            self.traverse( current.nextNode, fromRoot )
    
    
    # search for a value
    def search( self, value, current=None, fromRoot=True ):
        if fromRoot == True:
            current = self.root
            fromRoot = False
        
        # we made it all the way down the tree and ended up on the nullptr of the parent node, i.e. bottom-most node
        if current == None:
            print("no one by that name here")
            
        elif value == current.getVal():
            return current
        
        elif value > current.getVal():
            self.search( node, current.nextNode, fromRoot )
            
        elif value < current.getVal():
            self.search( node, current.prevNode, fromRoot )
        
        
    # we need to keep track of the parent node so that we can point it to the one we're trying to insert into the tree
    def insert( self, node, current=None, parent=None, fromRoot=True ):
        if fromRoot == True:
            current = self.root
            fromRoot = False
            parent = current
            
        # here, we've made it all the way down to the None's of the bottom nodes
        # and need to replace one of those None's with the to-be-inserted node
        if current == None:
            
            # this case covers the creation of a bst with no nodes, i.e. an empty tree
            if parent == None:
                self.root = node
            else:
                if node.getVal() > parent.getVal():
                    parent.setNext( node )
                else:
                    parent.setPrev( node )
                    
        # in these cases, we're still just walking over the tree
        elif node.getVal() > current.getVal():
            parent = current
            self.insert(node, current.nextNode, parent, fromRoot)
        else:
            parent = current
            self.insert(node, current.prevNode, parent, fromRoot)    
        
    
    def minimum( self, current=None, fromRoot=True ):
        if fromRoot == True:
            current = self.root
            fromRoot = false
            
        if current.getPrev() == None:
            return current
        else:
            self.minimum( current, fromRoot )
            
            
    def maximum( self, current=None, fromRoot=True ):
        if fromRoot == True:
            current = self.root
            fromRoot = false
            
        if current.getNext() == None:
            return current
        else:
            self.minimum( current, fromRoot )
        
        
    # Cormen says there's 4 cases; naively, we could just reinsert everything below the node to be deleted
    # granted this is inefficient...
    def delete( self, node, current=None, parent=None, fromRoot=True ):
        if parent == node:
            current = self.root
            fromRoot = False
            parent = current
            
            
        
