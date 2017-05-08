# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 11:24:33 2017
Analiza la complejidad amortizada del algoritmo Ford-Fulkerson para grafos sparse. El tamaño de la instancia se distribuye exponencialmente

Ford-Fulkerson --- Sparse --- Exponencial
@author: Eduardo
"""
from random import expovariate, sample,random,choice
from math import sqrt,ceil
import os
from time import time
import matplotlib.pyplot as plt
operaciones=0
puntos=[]

def componentes_conexas(G):
    'Encuentra las componentes conexas de G'
    grupos={}
    for i in G.ady:
        for j in G.ady[i]:
            union=grupos.get(i,{i})|grupos.get(j.final,{j.final})
            for nodo in union:
                grupos[nodo]=union
    #crear componentes conexas
    
    return set([frozenset(grupos[i]) for i in grupos])

def genera_instancia_flujo(numNodos,mediaDensidadArcos,textFile=None,coord=None):
    ''''genera un grafo de numNodos nodos,
        el numero de arcos incipientes de cada nodo se distribuye exponencialmente con media mediaDensidadArcos,
        se supone la capacidad de los arcos proporcional a la longitud '''
        
    global puntos
    
    if coord is not None:
        puntos = sample(puntos,numNodos)
    else:
        puntos=[(20*random(),20*random()) for i in range(numNodos)] #aqui no hay seguridad de la lejania de los puntos
    
    #calcular distancias
    D=[]
    for x1,y1 in puntos:
        temp=[]
        for x2,y2 in puntos:
            temp.append(int(sqrt((x1-x2)**2+(y1-y2)**2)))
        D.append(temp)
    
    #crear grafo
    G=GrafoSimple()
    nodos=range(numNodos)
    for n in nodos:
        G.AgregaNodo(n)
#        print(G.ady)
    for n in nodos:
        arcos=sample(nodos,ceil(expovariate(1/mediaDensidadArcos)*numNodos))
        try:
            arcos.remove(n)
        except:
            pass
        if len(arcos) == 0 and n == 0:            
            arco=choice([x for x in range(1,numNodos)])
            
            G.AgregaArco(0,arco,10*D[n][arco])
        for arco in arcos:
            G.AgregaArco(n,arco,10*D[n][arco])
    #Asegurar conexidad
    grupos=componentes_conexas(G)
#    print(grupos)
    if len(grupos)>1:#hay que agregar algunos arcos para unir las componentes
        grupo=grupos.pop()
        for g in grupos:
            numArcos=ceil(expovariate(1/2*mediaDensidadArcos)*numNodos)
            if numArcos>len(grupos) or  numArcos>len(g):
                numArcos=1
           
            inicio=sample(list(grupo),numArcos)
            fin=sample(list(g),numArcos)
            
        
            for i in range(numArcos):
                x,y=inicio[i],fin[i]
                G.AgregaArco(x,y,10*int(sqrt((puntos[x][0]-puntos[y][0])**2+(puntos[x][1]-puntos[y][1])**2)))
    
    return G
    
def graficaGrafoResidual(G, puntos, texFile=None, append=False):
    ''''genera un archivo .tex con la imagen del grafo G, 
        si un arco tiene capacidad 0 no será dibujado'''
    if texFile is None:
        texFile="default"
    
    
    if not append:
        output=open(texFile+'.tex','w')
        print("\\documentclass{standalone}\n\\usepackage{tikz}\n\\usetikzlibrary{decorations.pathmorphing}\n\\begin{document}\n\\begin{tikzpicture}[node distance = 0.5cm,inner sep = 2pt]\n\\tikzstyle{ann} = [fill=white,font=\scriptsize,inner sep=1pt] \n",file=output)    
    else:
        output=open(texFile+'.tex','a')
        print("\\begin{tikzpicture}[node distance = 0.5cm,inner sep = 2pt]\n\\tikzstyle{ann} = [fill=white,font=\scriptsize,inner sep=1pt] \n",file=output) 
        
    print("%c//////////////////////    dibuja grafo     ////////////////////////\n" %('\u0025'),file=output)
    #dibuja nodos
    for nodo in G.ady:
        print("\\draw (%.2f,%.2f) node[circle,draw, minimum size=6pt] (n%d) {%d};  %cnodo %d" %(puntos[nodo][0],puntos[nodo][1],nodo,nodo,'\u0025',nodo),file=output)
    #dibuja arcos
    for nodo in G.ady:
        for arco in G.ady[nodo]:
            if arco.capacidad != 0 and arco.inicio!=arco.final:
                print("\\draw (n%d) edge[->]  (n%d); %carco (%d,%d)" %(arco.inicio,arco.final,'\u0025',arco.inicio,arco.final),file=output)
    
    if not append:
        print("\\end{tikzpicture}\n\\end{document}",file=output)    
        output.close()      
        os.system("pdflatex "+texFile)
        os.startfile(texFile+".pdf")
    else:
        print("\\end{tikzpicture}\n\n\n",file=output)    
        output.close() 
        
        
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
        ji=Arco(j,i,0,ij)
        ij.residual=ji
        self.ady[i].append(ij)
        self.ady[j].append(ji)
        
        
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
           
            
                
                 
    def Ford_Fulkerson(self,s,t): 
        'Determina el flujo máximo que puede fluir desde s hacai t'
        global operaciones
        #buscar camnio entre s y t
        camino=self.BuscaCamino(s,t,[])
#        print("Camino: %s"%camino)
        operaciones+=1
        if camino is None or len(camino) is 0:
            flujo=0
            for arco in self.ady[s]:
                operaciones+=1
                flujo+=arco.residual.capacidad
            return flujo
        
        #Empujar delta unidades de flujo por el camino        
        delta=min(camino).capacidad
        operaciones+=len(camino)
#        print("delta=%d"%delta)
        
        for arco in camino:
            operaciones+=2
            arco.capacidad=arco.capacidad-delta
            arco.residual.capacidad=arco.residual.capacidad+delta
        
        return self.Ford_Fulkerson(s,t)

      
def experimento(num_trat,num_rep,media_tamGrafo,media_densidad):
    '''realiza un experimento de num_trat trataminetos cada uno con num_rep replicas.
    El tamaño de las instancias que se generan se distribuye exponencialmente con media media_tamGrafo
    La cantidad de arcos salientes de cada nodo se distribuye exponencialmente con media media_densidad.
    Para representar un grafo sparse, esta media debe ser pequeña (estimo menor a 0.2)
    Se muestran las comparaciones de la implementaci´pon con la complejidad eórica y el tiempo de ejecución'''
    
    global operaciones
    op=[0]*num_trat
    tiempo=[0]*num_trat
    complejidad=[0]*num_trat
    tamanio=[]
    for trat in range(num_trat):
        print("tratamiento: %d"%(trat+1))
        n=int(expovariate(1/media_tamGrafo) )
        while n<5:
            n=int(expovariate(1/media_tamGrafo) )
        tamanio.append(n)
        for rep in range(num_rep):
            print("replica: %d"%(rep+1))
            G=genera_instancia_flujo(n,media_densidad)
            operaciones=0
            start=time()
            M=0 #calcular numero de arcos
            U=0
            for nodo in G.ady:
                for a in G.ady[nodo]:
                    M+=1
                    if U<a.capacidad:
                        U=a.capacidad            
                        M/=2 #porque se consideraron arcos residuales
    
            G.Ford_Fulkerson(0,n-1)
            op[trat]+=operaciones
            tiempo[trat]+=time()-start
            complejidad[trat]+=M*n*U
        op[trat]/=num_rep
        tiempo[trat]/=num_rep
        complejidad[trat]/=num_rep
    
    #hacer graficas
    todo=[(tamanio[i],op[i],tiempo[i],complejidad[i]) for i in range(len(tamanio))]
    todo.sort()
    tamanio,op,tiempo,complejidad=[],[],[],[]      
    for r in todo:
        tamanio.append(r[0])
        op.append(r[1])
        tiempo.append(r[2])
        complejidad.append(r[3])
        
    #normalizar datos
    min_tiempo,max_tiempo=min(tiempo),max(tiempo)
    norm_tiempo=[(x-min_tiempo)/(max_tiempo-min_tiempo) for x in tiempo]
    min_op,max_op=min(op),max(op)
    norm_op=[(x-min_op)/(max_op-min_op) for x in op]
    
    plt.plot(tamanio,op,label="algoritmo implementado")
    plt.plot(tamanio,complejidad,label="complejidad teorica")
    plt.legend(loc='upper left', frameon=False)
    plt.xlabel("tamaño instancia")
    plt.ylabel("número de operaciones")
    plt.title("Complejidad Asintotica($O(nmU)$) vs Complejidad Amortizada")
    plt.show()
    
    plt.plot(tamanio,op,label="total operaciones")
    plt.legend(loc='upper left', frameon=False)
    plt.xlabel("tamaño instancia")
    plt.ylabel("número de operaciones")
    plt.title("Complejidad amortizada")
    plt.show()
    
    plt.plot(tamanio,norm_tiempo,label="tiempo normalizado")
    plt.plot(tamanio,norm_op,label="total operaciones normalizado")
    plt.legend(loc='upper left', frameon=False)
    plt.xlabel("tamaño instancia")    
    plt.title("Tiempo de ejecución y total de operaciones")
experimento(50,5,20,0.01)
#G=genera_instancia_flujo(100,0.01)
#graficaGrafoResidual(G,puntos,"grafica")
##print(componentes_conexas(G))
#print(G.Ford_Fulkerson(0,49)) 
#print(operaciones)

