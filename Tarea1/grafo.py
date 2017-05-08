# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 12:52:28 2017
Estructura de representación y alamacenamiento de un grafo
@author: Eduardo
"""


class Arco:
    def __init__(self,i,j,c,res=None):
        self.inicio=i
        self.final=j
        self.capacidad=c
        self.capacidad_original=c
        self.residual=res        
    def __lt__(self,other):
        return self.capacidad<other.capacidad
    def __repr__(self):
        return "(%d,%d)"%(self.inicio,self.final)
    
    
  
   
class GrafoSimple:
    def __init__(self,textFile=None):
        self.ady={}        
        if textFile is not None:                  
            #leer instancia
            input=open(textFile,'r')   
            for linea in input:
                linea = linea.strip()
                if len(linea) == 0:
                    break
                pedazo = linea.split()                
                if pedazo[0] == 'n:':                    
                    self.AgregaNodo(int(pedazo[1]))                    
                elif pedazo[0] == 'a:':
                    self.AgregaArco(int(pedazo[1]),int(pedazo[2]),int(pedazo[3]))
            input.close()
            
    def __repr__(self):
        string=''
        for n in self.ady:
            string+="%d => "%n
            for a in self.ady[n]:                
                string+="%d(%d) "%(a.final ,a.capacidad) 
            string+='\n' 
        return string
        
    def AgregaNodo(self,nodo):
        self.ady[nodo]=[]
        
    def AgregaArco(self,i,j,c=0):
        assert i is not j
        assert i in self.ady
        assert j in self.ady
        ij=Arco(i,j,c)
        ji=Arco(j,i,0,ij)
        ij.residual=ji
        self.ady[i].append(ij)
        self.ady[j].append(ji)
        
        
    def BuscaCamino(self,s,t,camino):
        if s is t:
            return camino
        for a in self.ady[s]:
            if a.capacidad>0 and not a in camino and not a.residual in camino:
                temp= self.BuscaCamino(a.final,t,camino+[a])
                if temp is not None:
                    return temp
           
     