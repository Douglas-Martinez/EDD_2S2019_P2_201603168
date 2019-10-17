import hashlib

class Bloque(object):
    def __init__(self, i=None, t=None, c=None, d=None, p=None):
        self.INDEX = i
        self.TIMESTAMP = t
        self.CLASS = c
        self.DATA = d
        self.PREVIOUSHASH = p
        self.HASH = self.func_Hash()
        self.anterior = None
        self.siguiente = None

    def func_Hash(self):
        return hashlib.sha256(str(self.INDEX).encode() + str(self.TIMESTAMP).encode() + str(self.CLASS).encode() + str(self.DATA).encode() + str(self.PREVIOUSHASH).encode()).hexdigest()

class NodoPila(object):
    def __init__(self,block=None):
        self.b = block
        self.sig = None

class NodoAVL(object):
    def __init__(self, c=0, n=''):
        self.carne = c
        self.name = n
        self.height = 1
        self.fe = 0
        
        self.right = None
        self.left = None