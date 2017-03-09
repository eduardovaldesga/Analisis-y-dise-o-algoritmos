"""laberintoDFS"""


from random import shuffle,sample
from math import log
    
def DFS(grafo,inicio):
    visitados=set([inicio])
    pila=[inicio]
    secuencia=[-1]*len(grafo)
#    secuencia[inicio]=-1
  
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
#                print(visitados,pila)
            
    return secuencia

def DFS_tuple(grafo,inicio):
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
#                print(visitados,pila)
            
    return secuencia

def genera_laberinto_cuadricula(ancho,largo):
    'genera un laberinto en una cuadricula de ancho*largo'
    
    #genera grafo en la cuadricula
    grafo=[]
    for i in range(ancho*largo):
        grafo.append([])
        if i>=largo:
            grafo[i]+=[i-largo]
        if i<(ancho-1)*largo:
            grafo[i]+=[i+largo]
        if i%largo!=0:
            grafo[i]+=[i-1]
        if i%largo!=largo-1:
            grafo[i]+=[i+1]
    
    #hacer DFS para asegurar un camino de inicio a final    
    secuencia=DFS(grafo,ancho//2*largo+largo//2)
    
#    for i in range(ancho*largo):
#        print(i,secuencia[i],grafo[i])
        
    #graficar laberinto
    tex=open("laberinto.tex",'w')
    print("\\documentclass[border=12pt]{standalone}\n\\usepackage{tikz}\n\\usetikzlibrary{shapes,snakes}\n\\begin{document}\n\\begin{tikzpicture}[minimum size=0pt,inner sep = 0pt] \n",file=tex)
    #dibuja marco
    print("\draw[line width=3pt] \n\t (1,0) edge (%d,0) \n\t (%d,0) edge (%d,%d) \n\t (0,0) edge (0,%d) \n\t (0,%d) edge (%d,%d);" %(largo,largo,largo,ancho,ancho,ancho,largo-1,ancho),file=tex)
    
    #dibuja nodos dummy para acrecentar imagen en 1
    print("\\draw (-1,-1) node (k1)  {} \n (-1,%d) node (k2) {} \n (%d,-1) node (k3) {} \n (%d,%d) node (k4) {};" %(ancho+1,largo+1,ancho+1,largo+1),file=tex)
    
    c=0
    for i in range (ancho+1):
        for j in range (largo+1):
            print("\\draw (%d,%d) node (n%d)  {};" %(i,j,c),file=tex)
            c=c+1
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
                    
                    
                
    
    print(";\n\\end{tikzpicture}\n\\end{document}",file=tex)
    tex.close()
    
    import os 
    os.system("pdflatex laberinto.tex")
    os.startfile("laberinto.pdf")
            
    
    
    
     
    
    
def genera_laberinto_circular2(R,p):
    'genera un laberinto circular de radio R con p particiones'
    '''Se utiliza un grafo en el que se conoce por nodo su id y el nivel en que se encuentra'''
    
    #genera grafo en la cuadricula
    grafo=dict()
   
    
    for k in range(1,R+1):
        n= p*2**int(log(k,2))
        for i in range(n):
            grafo[(i,k)]=([((i+1)%n,k),((i-1+n)%n,k)])
            if k<R:
                if int(log(k,2))==int(log(k+1,2)):
                    grafo[(i,k)]+=[(i,k+1)]            
                else:
                    grafo[(i,k)]+=[(2*i,k+1),(2*i+1,k+1)]
            if k>1:
                if int(log(k,2))==int(log(k-1,2)):
                    grafo[(i,k)]+=[(i,k-1)]            
                else:
                    grafo[(i,k)]+=[(i//2,k-1)]
    
#    hacer DFS para asegurar un camino de inicio a final    
    secuencia=DFS_tuple(grafo,(0,1))
#    for i in grafo:        
#        print(i,grafo[i])
#    for i in secuencia:
#        print(secuencia[i], '=> ',i)
        
     #graficar laberinto
    tex=open("laberinto.tex",'w')
    print("\\documentclass[border=12pt]{standalone}\n\\usepackage{tikz}\n\\usetikzlibrary{shapes,snakes}\n\\begin{document}\n\\begin{tikzpicture}[minimum size=0pt,inner sep = 0pt] \n",file=tex)
    #dibuja marco
#    print("\draw[line width=3pt] \n\t (1,0) edge (%d,0) \n\t (%d,0) edge (%d,%d) \n\t (0,0) edge (0,%d) \n\t (0,%d) edge (%d,%d);" %(largo,largo,largo,ancho,ancho,ancho,largo-1,ancho),file=tex)
    
#    dibuja nodos dummy para acrecentar imagen en 1
    print("\\draw (45:%d) node (k1)  {} \n (135:%d) node (k2) {}\n (225:%d) node (k3) {} \n (-45:%d) node (k4) {};" %(R+2,R+2,R+2,R+2),file=tex)
    
#    c=0
#    for i in range (ancho+1):
#        for j in range (largo+1):
#            print("\\draw (%d,%d) node (n%d)  {};" %(i,j,c),file=tex)
#            c=c+1
    print("\\draw[line width=1.5pt] " ,file=tex)
    for i in grafo:        
        for j in grafo[i]:
            if j!= secuencia[i] and secuencia[j]!=i and i<j: #graficar pared
            
#                print(i,j,secuencia[i],secuencia[j])         
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
#           else:
#               if
#               if secuencia[i]!=j:
               
                    
    print(";\n\\draw[line width=5pt]\n",file=tex)
    n= p*2**int(log(R,2))
    for i in grafo:
        
        if i[1]==R and i[0]!=n//8: 
            print("(%d:%d) arc (%d:%d:%d)  %c(%d,%d) " %(360/n*(i[0]),i[1],360/n*(i[0]),360/n*(i[0]+1),i[1],'\u0025',i[0],i[1]),file=tex)
#            
                    
                    
                
    
    print(";\n\\end{tikzpicture}\n\\end{document}",file=tex)
    tex.close()
    
    import os 
    os.system("pdflatex laberinto.tex")
    os.startfile("laberinto.pdf")
    

            
genera_laberinto_circular2(65,4)  
    
        
    

    


            
    
    


