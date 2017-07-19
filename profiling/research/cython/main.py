
import sys
from random import randint
from bst_cython import cnode, BST

if __name__ == "__main__":    
    
    # profile!

    if sys.argv[1] == "1":
        for i in range(10000):
            bst = BST( )

    elif sys.argv[1] == "2":
        args = []
        for i in range(100000):   # real	0m1.896s
            args.append(randint(0,i))

        bst = BST(args)

    elif sys.argv[1] == "3":
        for i in range(10000):
            n = cnode(i)
            
    elif sys.argv[1] == "4":
        for i in range(10000):
            n = cnode(i)
            m = n.getVal( )
            
    elif sys.argv[1] == "5":
        bst = BST([59,35,6,2,100,14,19,15,1])
        bst.traverse( )
