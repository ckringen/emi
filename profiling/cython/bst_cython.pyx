
# implement a binary search tree class in cython

# let's assume we're only going to put ints inside the bst
cdef class cnode:
    cdef cnode nextNode
    cdef cnode prevNode
    cdef int val

    def __init__( self, val=0, greater=None, lesser=None ):
        self.val = val
        self.nextNode = greater
        self.prevNode = lesser
    
    # need to do None-checking per function though
    def __cinit__(self, int val=0, cnode greater=None, cnode lesser=None ):
        self.val = val
        self.nextNode = greater
        self.prevNode = lesser
                
    cpdef int getVal( self ) except *:
        return self.val
    
    cdef cnode getNext( self ):
        return self.nextNode.getVal()
    
    cdef cnode getPrev( self ):
        return self.prevNode.getVal()
    
    cdef void setVal( self, int val ) except *:
        self.val = val
        
    cdef void setNext( self, cnode m  ) except *:
        self.nextNode = m
        
    cdef void setPrev( self, cnode m ) except *:
        self.prevNode = m
        
        
cdef class BST:
    cdef cnode root

    def __cinit__( self, root=None ):
        if isinstance(root, list):                         # costly type checking?
            for i in root:
                n = cnode(i)
                self.insert(n)
        else:
            self.root = root
    
    cpdef void traverse( self, cnode current=None, bint fromRoot=True):
        ''' print elements in sorted "inorder" fashion '''
        if fromRoot == True:
            current = self.root
            fromRoot = False
        if current != None:
            self.traverse( current.prevNode, fromRoot )
            print(current.getVal())                        # should we use printf ??
            self.traverse( current.nextNode, fromRoot )
    
    
#     # search for a value
#     def search( self, value, current=None, fromRoot=True ):
#         if fromRoot == True:
#             current = self.root
#             fromRoot = False
        
#         # we made it all the way down the tree and ended up on the nullptr of the parent node, i.e. bottom-most node
#         if current == None:
#             print("no one by that name here")
            
#         elif value == current.getVal():
#             return current
        
#         elif value > current.getVal():
#             self.search( node, current.nextNode, fromRoot )
            
#         elif value < current.getVal():
#             self.search( node, current.prevNode, fromRoot )
        
        
    cdef void insert( self, cnode node, cnode current=None, cnode parent=None, bint fromRoot=True ):
        if fromRoot == True:
            current = self.root
            fromRoot = False
            parent = current

        if current == None:
            if parent == None:
                self.root = node
            else:
                if node.getVal() > parent.getVal():
                    parent.setNext( node )
                else:
                    parent.setPrev( node )
                    
        elif node.getVal() > current.getVal():
            parent = current
            self.insert(node, current.nextNode, parent, fromRoot)
        else:
            parent = current
            self.insert(node, current.prevNode, parent, fromRoot)    
        
    
#     def minimum( self, current=None, fromRoot=True ):
#         if fromRoot == True:
#             current = self.root
#             fromRoot = false
            
#         if current.getPrev() == None:
#             return current
#         else:
#             self.minimum( current, fromRoot )
            
            
#     def maximum( self, current=None, fromRoot=True ):
#         if fromRoot == True:
#             current = self.root
#             fromRoot = false
            
#         if current.getNext() == None:
#             return current
#         else:
#             self.minimum( current, fromRoot )
        
        
#     # Cormen says there's 4 cases; naively, we could just reinsert everything below the node to be deleted
#     # granted this is inefficient...
#     def delete( self, node, current=None, parent=None, fromRoot=True ):
#         if parent == node:
#             current = self.root
#             fromRoot = False
#             parent = current
            
            
        
