# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 14:15:20 2017

@author: Eduardo
"""


def reach(inicio,fin,textfile):
    d = dict()
    with open(textfile, "r") as archivo:
        for linea in archivo:
            x, y = (linea.strip()).split()
            n = d.get(x, {x}) | d.get(y, {y})
            if inicio in n and fin in n:
                return True
            for cuate in n:
                d[cuate] = n
    return False

#suponiendo que las aristas vienen ordenadas y que el grafo es conexo:
def arbolExpMin(textfile,numNodos):
    d = dict()
    costo=0
    with open(textfile, "r") as archivo:
        for linea in archivo:
            x, y, c= (linea.strip()).split()
            dx=d.get(x, {x})
            dy=d.get(y, {y})
            if dx is not dy:
                n = dx | dy
                for cuate in n:
                    d[cuate] = n                
                costo+=int(c)
                if len(n)==numNodos:
                    return costo
            
  
         
#print(reach('1','6',"aristas.txt"))
print("costo =",arbolExpMin("arbolexpmin.txt",6))
