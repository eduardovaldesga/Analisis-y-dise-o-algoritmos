# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 12:22:42 2017

@author: Eduardo
"""
from random import randint

class nodo:
    def __init__(self,id):
        self.id=id
        self.izq=None
        self.der=None
        
    def agrega(self,n):
        if n==self.id:
            return False
        elif n<self.id:
            if self.izq is None:
                self.izq=nodo(n)
                return True
            else:
                return self.izq.agrega(n)
        else:
            if self.der is None:
                self.der=nodo(n)
                return True
            else:
                return self.der.agrega(n)
    
    def encuentra(self,n):
        if n==self.id:
            return True
        elif n<self.id:
            if self.izq is None:                
                return False
            else:
                return self.izq.encuentra(n)
        else:
            if self.der is None:
                return False
            else:
                return self.der.encuentra(n)
            
    def __str__(self):
        s=""
        if self.izq is not None:
            s+=self.izq.__str__()
        s += str(self.id)+" "
        if self.der is not None:
            s+=self.der.__str__()
        return s
            

raiz=nodo(randint(0,100))
for i in range(20):
    raiz.agrega(randint(0,100))
print(raiz)