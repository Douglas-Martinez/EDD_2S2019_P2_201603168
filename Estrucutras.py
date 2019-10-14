from Nodos import *

from PIL import Image
import os

class AVL(object):
    def __init__(self):
        self.root = None

    def insert(self,c,n):
        self.root = self.insert2(self.root,c,n)

    def insert2(self,root,c,n):
        #No. 1
        if not root:
            return NodoAVL(c,n)
        elif c < root.carne:
            root.left = self.insert2(root.left,c,n)
        elif c > root.carne:
            root.right = self.insert2(root.right,c,n)
        elif c == root.carne:
            print('El Estudiante con Carne: {}, ya existe'.format(c))
            return root
        
        #No. 2
        root.height = 1 + max(self.getHeight(root.left),self.getHeight(root.right))

        #No. 3
        balance = self.getBalance(root)

        #No. 4
        # Left - Left
        if balance > 1 and c < root.left.carne:
            return self.rightRotate(root)

        # Right - Right
        if balance < -1 and c > root.right.carne:
            return self.leftRotate(root)

        # Left - Right
        if balance > 1 and c > root.left.carne:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        # Right - Left
        if balance < -1 and c < root.right.carne:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def leftRotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.getHeight(z.left),self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),self.getHeight(y.right))

        return y

    def rightRotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.getHeight(z.left),self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),self.getHeight(y.right))

        return y

    def getHeight(self, root):
        if not root:
            return 0

        return root.height

    def getBalance(self, root):
        if not root:
            root.fe = 0
            return 0

        root.fe = self.getHeight(root.left) - self.getHeight(root.right)
        return root.fe

    def preOrder(self, r):
        if not r:
            return 

        print("({} - {}) H:{} Fe:{}".format(r.carne,r.name,r.height,r.fe))
        self.preOrder(r.left)
        self.preOrder(r.right)

class BlockChain(object):
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def insert(self,tst,classe,data):
        if self.primero is None and self.ultimo is None:
            block = Bloque(0,tst,classe,data,'0000')
            self.primero = block
            self.ultimo = block
        else:
            block = Bloque(self.ultimo.INDEX+1,tst,classe,data,self.ultimo.HASH)
            block.anterior = self.ultimo
            self.ultimo.siguiente = block
            self.ultimo = block
    
    def graficar(self):
        grafo = "digraph BlockChain {\n"
        grafo += "node[shape=record];\n"
        grafo += "graph[pencolor=transparent];\n"
        grafo += "rankdir=TB;\n"
        
        aux = self.primero
        if aux == None:
            grafo += "\"BlockChain Vacia\""
        else:
            while aux != None:
                grafo += str(id(aux)) + "[label=\"CLASS="+aux.CLASS+"\\nTIMESTAMP="+aux.TIMESTAMP+"\\nPHASH="+aux.PREVIOUSHASH+"\\nHASH="+aux.HASH+"\"];\n"
                aux = aux.siguiente
        
        aux = self.primero
        grafo += str(id(aux))
        while aux != None:
            if aux.siguiente != None:
                grafo += "->" + str(id(aux.siguiente))
            aux = aux.siguiente
        grafo += "\n[dir=\"both\"];"
        grafo += "\nlabel = \"BlockChain\";\n"
        grafo += "}"

        f = open("BlockChain.dot","w+")
        f.write(grafo)
        f.close()

        os.system("dot -Tjpg BlockChain.dot -o BlockChain.jpg")
        im  = Image.open('BlockChain.jpg')
        im.show()
    
    def recorrer(self):
        aux = self.primero
        while aux is not None:
            print()
            print('Index: {}\nTimeStamp: {}\nClass: {}\nData: {}\nPreviousHash: {}\nHash: {}'.format(aux.INDEX,aux.TIMESTAMP,aux.CLASS,aux.DATA,aux.PREVIOUSHASH,aux.HASH))
            aux = aux.siguiente