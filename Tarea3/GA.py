# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 14:24:33 2017
Algoritmo Genetico para Triple SAT
@author: Eduardo
"""

from random import choice,sample,randint,random,shuffle
from time import time
from matplotlib import pyplot

clausulas=[]
class solucion:
    def __init__(self,x):
        self.x=x
        self.f=fitness(x)
    def __repr__(self):
        return repr(self.x)+repr(self.f)
    def __lt__(self,other):
        return self.f<other.f
    def __le__(self,other):
        return self.f<=other.f

def fitness(assign):
    'calcula fitness para cnf: porcentaje de clausulas satisfechas'
    global clausulas
    numC=0
    for literals in clausulas:
        sat = []
        for l in literals:
            neg = '!' in l
            var = int(l[neg+1:])
            ok = ((assign[var-1] and not neg) or (not assign[var-1] and neg))
            sat.append(ok)
            if ok:             
                numC+=1
                break
    return 100*numC/len(clausulas)

def cruza(P1,P2):
    'cruzamiento por un punto, se obtienen dos hijos'
    c=randint(0,len(P1.x)-1)
    return [solucion(P1.x[:c]+P2.x[c:]),solucion(P2.x[:c]+P1.x[c:])]

def GA3SAT(instancia,n,N=100,G=20,Pc=0.5,Pm=0.1):
    #indicadores de calidad tiempo y fitness
    start =time()
    out=open("mejor_soln.txt",'w')
    gen=[]
    soln=[]
    #leer instancia
    global clausulas
    with open(instancia, "r") as instance:
        clausulas=[]
        for c in instance:
            c = c.strip()
            if len(c) == 0:
                break
            clausulas.append(c.split())
        
        #generar población inicial
        P=[solucion([choice([0,1]) for i in range(n)]) for x in range(N)]
        
        P.sort()
        print(0,P[-1].f,P[-1].x,file=out )
        
        
        #repetir por G generaciones
        for g in range(G):
            H=[]
            #Generar progenie
            while len(H)<N:
                #Elegir individuos para cruzarse torneo binario            
                [P1,P2]=[max(sample(P,2)), max(sample(P,2))]
                
                #Aplicar cruzamiento
                if random()<Pc:
                    Hijos=cruza(P1,P2)
                    
                    #aplicar mutacion
                    for h in Hijos:
                        if random()<Pm:
                            x= randint(0,n-1)                       
                            h.x[x]=(h.x[x]+1)%2
                        # verificar si se encontró el óptimo
                        if h.f==100:#caso afirmativo para el algoritmo
                            print(g+1,h.f,h.x,file=out )
                            elapsed = (time() - start)
                            print("elapsed time: %fs" %elapsed)
                            return h
                    H+=Hijos
                
            #reemplazar padres por hijos
            P=H
            #opcional grafica d eficienci
            P.sort()
            print(g+1,P[-1].f,P[-1].x,file=out )            
            gen.append(g+1)
            soln.append(P[-1].f)
    elapsed = (time() - start)
    print("elapsed time: %fs" %elapsed)
    pyplot.plot(gen,soln)
    pyplot.show()
    return P
                    
                
                
            
        
       


GA3SAT("instancia_tripleSAT(False,False)990-1175.txt",1175,300,100)
