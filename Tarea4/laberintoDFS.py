# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 12:09:33 2017
Genera una istancia de un laberinto rectangular o circular

La aplicación de BF es determinar las componentes conexas de un grafo, esto fue implementado como parte de la tarea 5
@author: Eduardo
"""


from random import sample,randint,seed,choice
from math import log

def shuffle(lista):
    'emula el shuffle de random'
    temp=lista[:]
    nuevo=[]    
    while len(temp)>0:
        
        x=choice(temp)
        nuevo.append(x)
        temp.remove(x)
    lista=nuevo[:]

def DFS(grafo,inicio):
    'búsqueda por profundidad del grafo a partir del nodo inicio'
    visitados=set([inicio])
    pila=[inicio]
    secuencia=[-1]*len(grafo)
    while(len(pila)>0):    
        x=pila.pop()  
        temp=grafo[x]
        for a in temp:
            if a not in visitados:            
                visitados.add(a)
                pila+=[a]
                secuencia[a]=x            
    return secuencia

def DFS_tuple(grafo,inicio):
    'DFS para una tupla, esta sirve para el caso del laberinto circular'
    visitados=set([inicio])
    pila=[inicio]
    secuencia=dict()
    for i in grafo:
        secuencia[i]=[]
    while(len(pila)>0):
        x=pila.pop()        
#        print(x)
        temp=grafo[x]
        shuffle(temp)
        for a in temp:
            if a not in visitados:            
                visitados.add(a)
                pila+=[a]
                secuencia[a]=x
            
    return secuencia

def genera_laberinto_cuadricula(ancho,largo):
    'genera un laberinto en una cuadricula de ancho*largo'
    
    #genera grafo en la cuadricula, un grafo esta representado como una lista de adyacencia
    grafo=[]
    for i in range(ancho*largo):
        aux = []        
        #nodo de abajo
        if i>=largo:
            aux.append(i-largo)
        # nodo de arriba
        if i<(ancho-1)*largo:
            aux.append(i+largo)
        #nodo de la izquierda
        if i%largo!=0:
            aux.append(i-1)        
        #nodo de la derecha
        if i%largo!=largo-1:
            aux.append(i+1)
        #mezclar los nodos adyacentes para que el laberinto no presente peines
        shuffle(aux)
        grafo.append(aux)
    #hacer DFS para asegurar un camino de inicio a final    
    secuencia=DFS(grafo,randint(0,largo*ancho))
        
    #graficar laberinto
    tex=open("laberinto.tex",'w')
    print("\\documentclass[border=12pt]{standalone}\n\\usepackage{tikz}\n\\usetikzlibrary{shapes,snakes}\n\\begin{document}\n\\begin{tikzpicture}[minimum size=0pt,inner sep = 0pt] \n",file=tex)
    
    #dibuja marco
    print("\draw[line width=3pt] \n\t (1,0) edge (%d,0) \n\t (%d,0) edge (%d,%d) \n\t (0,0) edge (0,%d) \n\t (0,%d) edge (%d,%d);" %(largo,largo,largo,ancho,ancho,ancho,largo-1,ancho),file=tex)
    
    # dibuja nodos (cada nodo es un cuadradito)  
    c=0
    for i in range (ancho+1):
        for j in range (largo+1):
            print("\\draw (%d,%d) node (n%d)  {};" %(i,j,c),file=tex)
            c=c+1
    #dibuja paredes
    print("\\draw[line width=1.5pt] " ,file=tex)
    for i in range(ancho*largo):
        for j in grafo[i]:
            if j!=secuencia[i] and secuencia[j]!=i and i<j: #graficar pared
                
                if j==i+1:
                    print("(n%d) edge (n%d)" %(i+i//largo+1,i+i//largo+largo+2),file=tex)
                if j==i-1:
                    print("(n%d) edge (n%d)" %(i+i//largo,i+i//largo+largo+1),file=tex)
                if j==i-largo:
                    print("(n%d) edge (n%d)" %(i+i//largo,i+i//largo+1),file=tex)
                if j==i+largo:
                    print("(n%d) edge (n%d)" %(i+i//largo+largo+1,i+i//largo+largo+2),file=tex)
                    
    print(";\n",file=tex)
    
    #dibuja el arbol del DFS (esto debe ser omitido)
    c=0
    for i in range (ancho):
        for j in range (largo):
            print("\\draw (%f,%f) node (s%d)  {};" %(i+0.5,j+0.5,c),file=tex) 
            c+=1
    print("\n\draw",file=tex)
    for i in range(ancho*largo):
        if secuencia[i]!=-1:
            print("(s%d) edge[green] (s%d)" %(i,secuencia[i]),file=tex) 
    print(";\n",file=tex)
    
    print("\n\\end{tikzpicture}\n\\end{document}",file=tex)
    tex.close()
    
    import os 
    os.system("pdflatex laberinto.tex")
    os.startfile("laberinto.pdf")      
     
    
    
def genera_laberinto_circular2(R,p):
    'genera un laberinto circular de radio R con p particiones'
    '''Se utiliza un grafo en el que se conoce por nodo su id y el nivel en que se encuentra        (id,nivel). En el nivel k hay p*2**int(log(k,2)) nodos'''
    
    #genera grafo en la cuadricula
    grafo=dict()
   
    
    for k in range(1,R+1):
        n= p*2**int(log(k,2))
        for i in range(n):
            #agrega nodos izquierda y derecha
            grafo[(i,k)]=([((i+1)%n,k),((i-1+n)%n,k)])
            #agrega nodo(s) de arriba
            if k<R:
                #el nivel de arriba tiene la misma cantidad de nodos, asi que solo hay un nodo encima
                if int(log(k,2))==int(log(k+1,2)):
                    grafo[(i,k)]+=[(i,k+1)]            
                else: #en el sig nivel hay el doble de nodos, este nodo tiene dos encima
                    grafo[(i,k)]+=[(2*i,k+1),(2*i+1,k+1)]
            #agrega nodo de abajo
            if k>1:
                #el nivel anterior tiene la misma cantidad de nodos
                if int(log(k,2))==int(log(k-1,2)):
                    grafo[(i,k)]+=[(i,k-1)]            
                else: #el nivel de abajo tiene la mitad de nodos
                    grafo[(i,k)]+=[(i//2,k-1)]
    
#    hacer DFS para asegurar un camino de inicio a final    
    secuencia=DFS_tuple(grafo,(0,1))
    
     #graficar laberinto
    tex=open("laberinto.tex",'w')
    print("\\documentclass[border=12pt]{standalone}\n\\usepackage{tikz}\n\\usetikzlibrary{shapes,snakes}\n\\begin{document}\n\\begin{tikzpicture}[minimum size=0pt,inner sep = 0pt] \n",file=tex)
    
    #dibuja las paredes, se utilizan coordenadas polares
    print("\\draw[line width=1.5pt] " ,file=tex)
    for i in grafo:        
        for j in grafo[i]:
            if j!= secuencia[i] and secuencia[j]!=i and i<j: #graficar pared
                n= p*2**int(log(i[1],2))
                if j[1]==i[1]: #ambos en el mismo nivel
                    n= p*2**int(log(i[1],2))
                    if j[0]==i[0]-1:
                        print("(%d:%d) edge (%d:%d) %c(%d,%d) => (%d,%d)" %(360/n*i[0],i[1],360/n*i[0],i[1]-1,'\u0025',i[0],i[1],j[0],j[1]),file=tex)
                    else:
                        print("(%d:%d) edge (%d:%d) %c(%d,%d) => (%d,%d)" %(360/n*(i[0]+1),i[1],360/n*(i[0]+1),i[1]-1,'\u0025',i[0],i[1],j[0],j[1]),file=tex)
                    
                elif j[1]==i[1]+1: #j esta en el nivel de arriba
                    n= p*2**int(log(j[1],2))                    
                    print("(%d:%d) arc (%d:%d:%d)  %c(%d,%d) => (%d,%d)" %(360/n*(j[0]),i[1],360/n*(j[0]),360/n*(j[0]+1),i[1],'\u0025',i[0],i[1],j[0],j[1]),file=tex)
                else:
                     print("(%d:%d) arc (%d:%d:%d)  %c(%d,%d) => (%d,%d)" %(360/n*(i[0]),i[1],360/n*(i[0]),360/n*(i[0]+1),i[1],'\u0025',i[0],i[1],j[0],j[1]),file=tex)
     
    #dibuja borde                 
    print(";\n\\draw[line width=5pt]\n",file=tex)
    n= p*2**int(log(R,2))
    for i in grafo:
        
        if i[1]==R and i[0]!=n//8: 
            print("(%d:%d) arc (%d:%d:%d)  %c(%d,%d) " %(360/n*(i[0]),i[1],360/n*(i[0]),360/n*(i[0]+1),i[1],'\u0025',i[0],i[1]),file=tex)
            
    print(";\n\\end{tikzpicture}\n\\end{document}",file=tex)
    tex.close()
    
    import os 
    os.system("pdflatex laberinto.tex")
    os.startfile("laberinto.pdf")
    



seed("nan")           
genera_laberinto_circular2(20,20)  
#genera_laberinto_cuadricula(20,20)
    
        
    

    


            
    
    


