# -*- coding: utf-8 -*-
"""
Created on Mon May  8 12:19:55 2017

@author: Eduardo Juan
"""
from random import random,choice,shuffle
from math import sqrt,ceil

def TSP(seq,G):
    costo=G.getArco(seq[-1],seq[0]).capacidad
    act = seq.pop(0)
    while len(seq) > 0:
        sig = seq.pop(0)
        costo += G.getArco(act, sig).capacidad
        act = sig
    return costo
        

def DFS(grafo):
    'búsqueda por profundidad del grafo a partir del nodo inicio'
    inicio=choice([x for x in G.ady])
    pila=[inicio]
    secuencia=[]
    while(len(pila)>0): 
#        print(pila)
        x=pila.pop()  
#        print(x)
        if x not in secuencia:
            secuencia.append(x)  
#        print(visitados)
        temp=grafo.ady[x]
        shuffle(temp)
        for a in temp:
            if a.final not in secuencia:            
                pila+=[a.final]
                          
    return secuencia



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
        return "(%d,%d):%d"%(self.inicio,self.final,self.capacidad)
    
class Nodo:
    def __init__(self,i,x,y):
        self.id=i
        self.x=x
        self.y=y
    def __repr__(self):
        return "Nodo: %d"%(self.id)
#    def __hash__(self):
#        return hash(self.id)
  
   
class GrafoSimple:
    ady={}
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
            string+="%s => "%n
            for a in self.ady[n]:                
                string+="%d(%d) "%(a.final ,a.capacidad) 
            string+='\n' 
        return string
        
    def AgregaNodo(self,nodo):
        self.ady[nodo]=[]
        
    def AgregaArco(self,i,j,c=0):
        assert i is not j
#        assert i in self.ady
#        assert j in self.ady
        ij=Arco(i,j,c)
#        ji=Arco(j,i,0,ij)
#        ij.residual=ji
        self.ady[i].append(ij)
#        self.ady[j].append(ji)
        
    def getArco(self,i,j):
        for a in self.ady[i]:
            if a.final == j:
                return a
    def BuscaCamino(self,s,t,camino):
        'Encuentra un camino desde s a t'
        global operaciones
        operaciones+=1
        if s is t:            
            return camino
        try:
            for a in self.ady[s]:
                operaciones+=3
                if a.capacidad>0 and not a in camino and not a.residual in camino:
                    temp= self.BuscaCamino(a.final,t,camino+[a])
                    if temp is not None:
                        return temp
        except:
            print(G)
            input()
           
            
            
            
def genera_instancia(numNodos,textFile=None):
    ''''genera un grafo de numNodos nodos,
        el numero de arcos incipientes de cada nodo se distribuye exponencialmente con media mediaDensidadArcos,
        se supone la capacidad de los arcos proporcional a la longitud '''
        
    global puntos
    
    
    
    puntos=[(20*random(),20*random()) for i in range(numNodos)] #aqui no hay seguridad de la lejania de los puntos
    
    #calcular distancias
    D=[]
    for x1,y1 in puntos:
        temp=[]
        for x2,y2 in puntos:
            temp.append(ceil(sqrt((x1-x2)**2+(y1-y2)**2)))
        D.append(temp)
    
    #crear grafo
    G=GrafoSimple()
    nodos=range(numNodos)
    for n in nodos:
        G.AgregaNodo(n)
#        print(G.ady)
    for n in nodos:
        arcos=[x for x in nodos if x != n]
        
        for arco in arcos:
            G.AgregaArco(n,arco,D[n][arco])
#    #Asegurar conexidad
#    grupos=componentes_conexas(G)
##    print(grupos)
#    if len(grupos)>1:#hay que agregar algunos arcos para unir las componentes
#        grupo=grupos.pop()
#        for g in grupos:
#            numArcos=ceil(expovariate(1/2*mediaDensidadArcos)*numNodos)
#            if numArcos>len(grupos) or  numArcos>len(g):
#                numArcos=1
#           
#            inicio=sample(list(grupo),numArcos)
#            fin=sample(list(g),numArcos)
#            
#        
#            for i in range(numArcos):
#                x,y=inicio[i],fin[i]
#                G.AgregaArco(x,y,10*int(sqrt((puntos[x][0]-puntos[y][0])**2+(puntos[x][1]-puntos[y][1])**2)))
    
    return G


def MST(G):
    arbol=GrafoSimple()
    Arcos=[]
    for n in G.ady:
        arbol.AgregaNodo(n)
        Arcos+=G.ady[n]
    Arcos.sort()
    
#    arbol = set()
    peso = 0
    comp = dict()
    
    for arista in Arcos:   
        u,v=arista.inicio,arista.final
        c = comp.get(v, {v})
        if u not in c:
            arbol.AgregaArco(u,v,arista.capacidad)
            arbol.AgregaArco(v,u,arista.capacidad)
            peso += arista.capacidad
            nuevo = c.union(comp.get(u, {u}))
            for w in nuevo:
                comp[w] = nuevo
                    
#    #hacer grafo no dirigido
#    for n in arbol.ady:
#        for arco in arbol.ady[n]:
#            arbol.AgregaArco(arco.final,arco)
    
    return arbol
    

    
        
            

    
G=genera_instancia(5)
print(G)
arbol=MST(G)
print(arbol)
for k in range(5):
    seq=DFS(arbol)
    print(seq, TSP(list(seq),G))
#print(DFS(arbol))