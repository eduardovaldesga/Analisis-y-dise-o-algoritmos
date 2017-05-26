# -*- coding: utf-8 -*-
"""
Created on Tue May 23 16:08:25 2017
Ramificar y acotar-problema de la mochila.
El algoritmo está basado en:
    Kolesar, P. J. (1967). A branch and bound algorithm for the knapsack problem. Management science, 13(9), 723-735.
@author: Eduardo
"""
from random import expovariate as exp
from random import randint
import os
def instancia(numItems,fileName):
    out=open(fileName,'w')
    #capacidad
    W=int(exp(1/3000))
    print(W, file=out)
    for i in range(numItems):
        print("%d %d %d"%(i,randint(1,W),exp(1/100)),file=out)
    out.close()

class item:
    def __init__(self,i,w,p):
        self.id=i
        self.peso=w
        self.valor=p
    def __repr__(self):
        return "%d %d %d"%(self.id,self.peso,self.valor)
    def __lt__(self,other):
        return self.valor/self.peso>other.valor/other.peso
    
class nodo:
    def __init__(self,c,peso,inc,exc):
        self.izq=None
        self.der=None
        self.cota=c
        self.peso_acum=peso
        self.incluidos=inc
        self.excluidos=exc
    def __repr__(self):
        s=''
        for i in self.incluidos:
            s+="%d "%i.id
        for e in self.excluidos:
            s+="%d* "%e.id
        return s
    def tikz(self):
        'regresa una cadena para hacer texto multilinea'
        s=''
        t=1
        for i in self.incluidos:
            s+="%d "%i.id
            t+=1
            if t%3==0:
                s+="\\\\"
        
        for e in self.excluidos:
            s+="%d* "%e.id
            t+=1
            if t%3==0:
                s+="\\\\"
        return s
def branchNbound(instancia):
    
    #leer instancia
    data=open(instancia,'r')
    objetos=[]
    W=int(data.readline())
    suma=0
    for linea in data:
        linea.strip()
        if len(linea) == 0:
            break
        parte=linea.split()
        objetos.append(item(int(parte[0]),int(parte[1]),int(parte[2])))
        suma+=objetos[-1].peso        
    n=len(objetos) 
    
    #para visualizar arbol
    output=open(instancia[:-3]+'tex','w')
    print("\\documentclass{standalone}\n\\usepackage{tikz}\n\\usetikzlibrary{positioning}\n\\usetikzlibrary{shapes.multipart}\n\\usetikzlibrary{decorations.pathmorphing}\n\\begin{document}\n\\begin{tikzpicture}[node distance = %.2fcm,inner sep = 2pt,every text node part/.style={align=center}]\n\\tikzstyle{ann} = [fill=white,font=\scriptsize,inner sep=1pt]\n \draw\n" %(0.5*n),file=output)
    idx=0
    
    #Revisar solución trivial
    if suma<=W:
        return set(range(n))
    
    #ordenar objetos por razon valor/peso
    objetos.sort()
    
    #seleccionar nodo con mejor cota hasta que todos los objetos hayan sido clasificados
    current=nodo(0,0,set(),set()) 
    print("node[draw,circle] (n%d) {$\emptyset$}"%(idx),file=output)
    print("node[right = 0.1cm of n%d] (c%d) {\small cota=%.2f}"%(idx,idx,0),file=output)
    while len(current.incluidos)+len(current.excluidos) < n:
        print("actual: {%s}  cota=%.2f"%(current,current.cota))
        
        #usar como pivote el objeto no clasificado de mayor razón v/w
        i=objetos.pop(0)
        
        #hijo izquierdo
        cota=sum([temp.valor for temp in current.incluidos])
        peso=sum([temp.peso for temp in current.incluidos])
#        print(cota,peso)
        for o in objetos:
#            print(o)
            if peso+o.peso<=W:
                cota+=o.valor
                peso+=o.peso
            else:
                cota+=(W-peso)/o.peso*o.valor
                break
        current.izq=nodo(cota,current.peso_acum,current.incluidos,current.excluidos|{i})
        
        #hijo derecho
        cota=sum([temp.valor for temp in current.incluidos])+i.valor
        peso=sum([temp.peso for temp in current.incluidos])+i.peso
#        print(cota,peso)
        for o in objetos:
#            print(o)
            if peso+o.peso<=W:
                cota+=o.valor
                peso+=o.peso
            else:
#                print(cota,(W-peso)/o.peso*o.valor)
                cota+=(W-peso)/o.peso*o.valor
                break
        #verificar factibilidad         
        if current.peso_acum+i.peso<=W:            
            current.der=nodo(cota,current.peso_acum+i.peso,current.incluidos|{i},current.excluidos)
        else:
            current.der=nodo(-999,current.peso_acum+i.peso,current.incluidos|{i},current.excluidos)
        
        print("izquierdo: {%s}   cota=%.2f"%(current.izq,current.izq.cota))
        print("node[draw,circle,below left of=n%d] (n%d) {%s}"%(idx,idx+1,current.izq.tikz()),file=output)
        print("node[right = 0.1cm of n%d] (c%d) {\small cota=%.2f}"%(idx+1,idx+1,current.izq.cota),file=output)
        print("(n%d) edge (n%d)"%(idx,idx+1),file=output)
        if current.der.cota>=0:            
             print("derecho: {%s}   cota=%.2f\n"%(current.der,current.der.cota))
             print("node[draw,circle,below right of=n%d] (n%d) {%s}"%(idx,idx+2,current.der.tikz()),file=output)
             print("node[right = 0.1cm of n%d] (c%d) {\small cota=%.2f}"%(idx+2,idx+2,current.der.cota),file=output)
             print("(n%d) edge (n%d)"%(idx,idx+2),file=output)
        else:
             print("derecho: {%s} ---> infactible\n"%current.der)
             print("node[draw,circle,below right of=n%d] (n%d) {%s}"%(idx,idx+2,current.der.tikz()),file=output)
             print("node[right = 0.1cm of n%d] (c%d) {\small infactible}"%(idx+2,idx+2),file=output)
             print("(n%d) edge (n%d)"%(idx,idx+2),file=output)
        #Actualizar current
        if current.der.cota>=current.izq.cota:
            current=current.der
            idx+=2
        else:
            current=current.izq
            idx+=1
    
    print("node[below left = 0.1cm of n%d] (o%d) {\small \\textcolor{red}{solucion optima}}"%(idx,idx),file=output)    
    print("(o%d) edge [->] (n%d)"%(idx,idx),file=output)
    print(";\n\\end{tikzpicture}\n\\end{document}",file=output)
    
    output.close() 
    os.system("pdflatex "+instancia[:-3]+'tex')
    os.startfile(instancia[:-3]+"pdf")
    #solución óptima encontrada
    return set([x.id for x in current.incluidos])
            
instancia(10,"instancia.txt")  
print("Solución óptima: %s"%branchNbound("instancia.txt"))