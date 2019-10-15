from Nodos import *

from PIL import Image
import os

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


class AVL(object):
    def __init__(self):
        self.root = None
        self.grafo = ""
        self.cadPRE = ""
        self.cadIN = ""
        self.cadPOST = ""
        self.printPRE = ""
        self.printIN = ""
        self.printPOST = ""

    def insert(self,c,n):
        self.root = self.insert2(self.root,c,n)
        self.Niveles(self.root,1)
        
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
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def Niveles(self,nodo,n):
        if nodo != None:
            nodo.nivel = n+1
            self.Niveles(nodo.left,nodo.nivel)
            self.Niveles(nodo.right,nodo.nivel)

    def auxGraficar(self,nodo):
        if nodo != None:
            self.grafo += "n"+str(nodo.carne)+" [ label = \"<C0>|Carne: "+str(nodo.carne)+"\\nNombre: "+str(nodo.name)+"\\nAltura: "+str(nodo.height)+"\\nFE: "+str(nodo.fe)+"|<C1>\" ];\n"
            self.auxGraficar(nodo.left)
            self.auxGraficar(nodo.right)

    def auxConectar(self,nodo):
        if nodo != None:
            if nodo.left != None:
                self.grafo += "n"+str(nodo.carne)+":C0->n"+str(nodo.left.carne)+";\n"
            if nodo.right != None:
                self.grafo += "n"+str(nodo.carne)+":C1->n"+str(nodo.right.carne)+";\n"
            self.auxConectar(nodo.left)
            self.auxConectar(nodo.right)

    def graficar(self):
        self.grafo = 'digraph AVL {\n'
        self.grafo += 'graph[splines = ortho, nodesep = 0.5];\n'
        self.grafo += 'node[shape = record, style = filled, fillcolor = seashell2];\n'
        
        if self.root == None:
            self.grafo += '\"Arbol Vacio\"'
        else:
            self.auxGraficar(self.root)
            self.grafo += "\n\n"
            self.auxConectar(self.root)
        
        self.grafo += '}'
        f = open('AVL.dot','w+')
        f.write(self.grafo)
        f.close()

        os.system('dot -Tjpg AVL.dot -o AVL.jpg')
        im = Image.open('AVL.jpg')
        im.show()

    def auxPre(self,nodo):
        if nodo != None:
            self.cadPRE += 'n'+str(nodo.carne)+"[label=\""+str(nodo.carne)+"\\n"+str(nodo.name)+"\"];\n"
            self.auxPre(nodo.left)
            self.auxPre(nodo.right)

    def auxConectarPre(self,nodo):
        if nodo != None:
            if nodo != self.root:
                self.cadPRE += ' -> n'+str(nodo.carne)
                self.printPRE += ' -> ' + str(nodo.carne) + "-" + str(nodo.name)
            self.auxConectarPre(nodo.left)
            self.auxConectarPre(nodo.right)

    def graficarPRE(self):
        self.cadPRE = ''
        self.printPRE = ''

        self.cadPRE += 'digraph AVL_PRE {\n'
        self.cadPRE += 'node[shape=record];\n'
        self.cadPRE += 'graph[pencolor=transparent];\n'
        self.cadPRE += 'rankdir=LR;\n'
        print('== PRE ORDEN ==')
        if self.root is None:
            print('ARBOL VACIO')
            self.cadPRE += '\"Arbol Vacio\"'
        else:
            self.auxPre(self.root)
            self.printPRE += str(self.root.carne) + "-" + str(self.root.name)
            self.cadPRE += 'n'+str(self.root.carne)
            self.auxConectarPre(self.root)

        print('Inicio -> ' + self.printPRE + ' -> FIN')

        self.cadPRE += ';\nlabel=\"Pre Orden\";\n'
        self.cadPRE += '}'

        f = open('TrasPRE.dot','w+')
        f.write(self.cadPRE)
        f.close()

        os.system('dot -Tjpg TrasPRE.dot -o TrasPRE.jpg')
        im = Image.open('TrasPRE.jpg')
        im.show()

    def auxIn(self,nodo):
        if nodo != None:
            self.auxIn(nodo.left)
            self.cadIN += 'n'+str(nodo.carne)+"[label=\""+str(nodo.carne)+"\\n"+str(nodo.name)+"\"];\n"
            self.auxIn(nodo.right)

    def auxConectarIn(self,nodo):
        if nodo != None:
            self.auxConectarIn(nodo.left)
            self.cadIN += 'n'+str(nodo.carne) + '->'
            self.printIN += str(nodo.carne) + "-" + str(nodo.name) + " -> "
            self.auxConectarIn(nodo.right)

    def graficarIN(self):
        self.cadIN = ''
        self.printIN = ''

        self.cadIN += 'digraph AVL_IN {\n'
        self.cadIN += 'node[shape=record];\n'
        self.cadIN += 'graph[pencolor=transparent];\n'
        self.cadIN += 'rankdir=LR;\n'
        print('== IN ORDEN ==')
        if self.root is None:
            print('ARBOL VACIO')
            self.cadIN += '\"Arbol Vacio\"'
        else:
            self.auxIn(self.root)
            self.auxConectarIn(self.root)

        temp = len(self.cadIN)
        cadena1 = self.cadIN[:temp - 2]
        self.cadIN = cadena1
                
        print('Inicio -> ' + self.printIN + 'FIN')

        self.cadIN += ';\nlabel=\"In Orden\";\n'
        self.cadIN += '}'

        f = open('TrasIN.dot','w+')
        f.write(self.cadIN)
        f.close()

        os.system('dot -Tjpg TrasIN.dot -o TrasIN.jpg')
        im = Image.open('TrasIN.jpg')
        im.show()

    def auxPost(self,nodo):
        if nodo != None:
            self.auxPost(nodo.left)
            self.auxPost(nodo.right)
            self.cadPOST += 'n'+str(nodo.carne)+"[label=\""+str(nodo.carne)+"\\n"+str(nodo.name)+"\"];\n"

    def auxConectarPost(self,nodo):
        if nodo != None:
            self.auxConectarPost(nodo.left)
            self.auxConectarPost(nodo.right)
            self.cadPOST += 'n'+str(nodo.carne) + '->'
            self.printPOST += str(nodo.carne) + "-" + str(nodo.name) + " -> "

    def graficarPOST(self):
        self.cadPOST = ''
        self.printPOST = ''

        self.cadPOST += 'digraph AVL_POST {\n'
        self.cadPOST += 'node[shape=record];\n'
        self.cadPOST += 'graph[pencolor=transparent];\n'
        self.cadPOST += 'rankdir=LR;\n'
        print('== POST ORDEN ==')
        if self.root is None:
            print('ARBOL VACIO')
            self.cadPOST += '\"Arbol Vacio\"'
        else:
            self.auxPost(self.root)
            self.auxConectarPost(self.root)

        temp = len(self.cadPOST)
        cadena1 = self.cadPOST[:temp - 2]
        self.cadPOST = cadena1
                
        print('Inicio -> ' + self.printPOST + 'FIN')

        self.cadPOST += ';\nlabel=\"Post Orden\";\n'
        self.cadPOST += '}'

        f = open('TrasPOST.dot','w+')
        f.write(self.cadPOST)
        f.close()

        os.system('dot -Tjpg TrasPOST.dot -o TrasPOST.jpg')
        im = Image.open('TrasPOST.jpg')
        im.show()
