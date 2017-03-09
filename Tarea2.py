"""
Restricciones de las instancias:
    Al menos una subestación está disponible
    Un arco disponible une dos nodos(o subE) disponibles
    Solo existe un arco entre (i) y (j)
    Si existe el arco (i,j) también el retorno (j,i), ambos tienen las mismas propiedades
    Todos los nodos (o subE) disponibles son conexos
    
    
Pendientes:
    Asegurar cierta distancia entre los nodos, al menos que un nodo no se encuentre encima de otro
    Usar un porcentaje de nodos disponibles
    Revisar si todos los arcos se pintan, parece que algunos grises no
        
"""



from random import randint, choice, random,shuffle
from math import sqrt,ceil
import numpy as np
import itertools
import os 
from grafo2 import grafo,Nodo,Arco,SubE
from shapely.geometry import Point,Polygon
#
#def random_point_within(poly):
#    min_x, min_y, max_x, max_y = poly.bounds
#    random_point = Point([randint(int(min_x), int(max_x)), randint(int(min_y), int(max_y))])
#    if not random_point.within(poly):       
#        random_point_within(poly) 
#    return (int(random_point.coords[0][0]),int(random_point.coords[0][1]))
def random_points_within(poly, num_points):
    min_x, min_y, max_x, max_y = poly.bounds

    points = []

    while len(points) < num_points:
        random_point = Point([randint(int(min_x), int(max_x)), randint(int(min_y), int(max_y))])
        if (random_point.within(poly)):
            points.append(random_point)

    return points

nombre_instancia="instancia.txt"
n=20 #numero total de nodos (incluyendo subestaciones)
PORSubE=0.1 #'porcentaje de subestaciones respecto al total de nodos'
SIZE=20 #'tamaño de la cuadricula donde se encuentran los nodos y subE'
DLOW=20 #'cota inferior de demanda'
DUP=100 #'cota superior de demanda'
PLOW=800 #'cota inferior de potencia'
PUP=3000 #'cota superior de potencia'
DENARCOS=0.01  #densidad de arcos salientes de nodos
DENARCOSSUBE=0.02  #densidad de arcos salientes de subestaciones
LLOW=40 #'cota inferior de longitud'
LUP=200 #'cota superior de longitud'
MAPA="coordenadas.txt" #nombre del archivo que  contiene al mapa
CLOW=20
CUP=200

def genera_instancia(textFile):
    'generador de instancias'
    global PORSubE
    global SIZE
    global DLOW
    global DUP
    global DENARCOS
    global n
    global MAPA
    
    
#    leer poligono
    mex=open(MAPA,'r')
    coordenadas=[]
    for linea in mex:
        
        linea.strip()
        p=linea.split()
        if len(p)==0:
            break
        
        coordenadas.append(((float(p[0]),float(p[1]))))
    #print(coordenadas)
    mapa=Polygon(coordenadas)
    
   
    
    
    G=grafo()
    datos=open(textFile,"w")

    ID=0
    numSubE=int(PORSubE*n)
    X=[]
    Y=[]
    on=set()
    

#generar subestaciones
    puesto=[randint(0,1) for i in range(numSubE)]#asegura al menos una subestacion on
    if 1 not in puesto:
        puesto[0]=1
        shuffle(puesto)
    for i in range(numSubE):
        punto=random_points_within(mapa,1)
#        print(punto)
        X.append(int(punto[0].coords[0][0]))
        Y.append(int(punto[0].coords[0][1]))
        potencia=randint(PLOW,PUP)        
        G.agregaNodo(SubE([i,X[-1],Y[-1],puesto[i],potencia]))
        print("s:\t"+str(ID)+"\t"+str(X[-1])+"\t"+str(Y[-1])+"\t"+str(puesto[i])+'\t'+str(potencia),file=datos)
        ID+=1
        if puesto[i]==1:
            on.add(i)
        

#generar nodos   
    for i in range(int(PORSubE*n)+1,n+1):
        #n: ID  X   Y   puesto/posible(1/0) demanda
        punto=random_points_within(mapa,1)
        X.append(int(punto[0].coords[0][0]))
        Y.append(int(punto[0].coords[0][1]))
        puesto=randint(0,1)
        if puesto==1:
            on.add(ID)
        demanda=randint(DLOW,DUP)
        G.agregaNodo(Nodo([ID,X[-1],Y[-1],puesto,demanda]))
        ID+=1


#generar matriz distancias
    D=[]
    for i in range(0,n):        
        D.append([ceil(sqrt((X[i]-X[j])**2+(Y[i]-Y[j])**2)) for j in range(0,n)])
            
   

#generar arcos
    for inicio in range(n):
        final=np.array(D[inicio]).argsort() #ordena por los nodos mas cercanos
        final=list(final)
        final.remove(inicio) #para eliminar arco (i,i)
        final=[x for x in final if inicio not in G.lista[x]] #verifica que el arco (j,i) no exista antes de crear el (i,j)
        if inicio<numSubE:        
            final2=final[:int(DENARCOSSUBE*n)] #selecciona el porcentaje de arcos estipulado
        else:
            final2=final[:int(DENARCOS*n)] 

#asegurar conectividad con nodos activos
        if inicio in on:
            if on.isdisjoint(final2): #si de los selccionados no hay uno activo :              
                x=next(x for x in final if x in on and inicio not in G.lista[x])#agregar para asegurar conexidad                    
                final2.append(x)
    
#agregar arcos            
        for f in final2:           
            puesto=G.lista[inicio]['info'].on*G.lista[f]['info'].on            
            longitud=D[i][f]
            capacidad=randint(CLOW,CUP)
            G.agregaArco(Arco([inicio,f,puesto,longitud,capacidad]))
            G.agregaArco(Arco([f,inicio,puesto,longitud,capacidad]))


#imprimir
    for g in G.lista:
        if g.id<numSubE:            
            print("s:\t"+str(g),file=datos)
        else:            
            print("n:\t"+str(g),file=datos)
    for g in G.lista:
        for a in G.lista[g]:
            if a!='info':
                print("a:\t"+str(G.lista[g][a]),file=datos)
            
    datos.close()
    
    graficaInstancia(textFile)
            
    return G








def graficaInstancia(textFile):
    global n
    output=open(textFile[:-3]+'tex','w')
    print("\\documentclass{standalone}\n\\usepackage{tikz}\n\\usetikzlibrary{shapes,snakes}\n\\begin{document}\n\\begin{tikzpicture}[node distance = 0.5cm,inner sep = 2pt]\n\\tikzstyle{ann} = [fill=white,font=\scriptsize,inner sep=1pt] \n",file=output)

    
    #graficar mapa
    #print("\\draw",file=output)
    mapa=open(MAPA,'r')
    c=0    
    for linea in mapa:
        linea = linea.strip()
        if len(linea) == 0:
            break
        pedazo = linea.split()
       
        #agrega nodo
        print("\\draw (%f,%f) node (mark%d)  {};" %(float(pedazo[0]),float(pedazo[1]),c),file=output)
        c+=1
    print("\n\\draw\\foreach \\i [count=\\xi from 1] in {0,...,%d}{(mark\\i) edge (mark\\xi)};" %(c-2),file=output)
    #\draw \foreach \i [count=\xi from 1] in {0,...,289} {(mark\i) edge (mark\xi)};    
        
  #(mark-1) \foreach \i in {2,...,26}{ -- (mark-\i) } -- cycle;
    
      
    
    
    
    #leer instancia
    input=open(textFile,'r')
#    output=open(textFile[:-3]+'tex','w')
#    print("\\documentclass{standalone}\n\\usepackage{tikz}\n\\usetikzlibrary{shapes,snakes}\n\\begin{document}\n\\begin{tikzpicture}[node distance = 0.5cm,inner sep = 2pt]\n\\tikzstyle{ann} = [fill=white,font=\scriptsize,inner sep=1pt] \n",file=output)

    
    for linea in input:
        linea = linea.strip()
        if len(linea) == 0:
            break
        pedazo = linea.split()   
        if pedazo[0]=='s:': #subestaciones
            if pedazo[4]=='1':
                print("\\draw (%d,%d) node[fill=black,draw, minimum size=1pt,text=white] (n%d) {};" %(int(pedazo[2]),int(pedazo[3]),int(pedazo[1])),file=output)
#                print("\tnode (e%d) [above of=n%d] {{\scriptsize %d}};" %(int(pedazo[1]),int(pedazo[1]),int(pedazo[5])),file=output)
            else:
                print("\\draw (%d,%d) node[lightgray,fill=lightgray,draw, minimum size=1pt,text=black] (n%d) {};" %(int(pedazo[2]),int(pedazo[3]),int(pedazo[1])),file=output)
#                print("\tnode (e%d) [text=lightgray,above of=n%d] {{\scriptsize %d}};" %(int(pedazo[1]),int(pedazo[1]),int(pedazo[5])),file=output)
        elif pedazo[0] == 'n:': #nodos
            if pedazo[4]=='1':               
                print("\\draw (%d,%d) node[fill=black,circle,draw, minimum size=1pt] (n%d) {};" %(int(pedazo[2]),int(pedazo[3]),int(pedazo[1])),file=output)
#                print("\tnode (e%d) [above of=n%d] {{\scriptsize %d}};" %(int(pedazo[1]),int(pedazo[1]),int(pedazo[5])),file=output)
            else:
                print("\\draw (%d,%d) node[lightgray,fill=lightgray,dashed,circle,draw, minimum size=1pt] (n%d) {};" %(int(pedazo[2]),int(pedazo[3]),int(pedazo[1])),file=output)      
#                print("\tnode (e%d) [text=lightgray,above of=n%d] {{\scriptsize %d}};" %(int(pedazo[1]),int(pedazo[1]),int(pedazo[5])),file=output)
        elif pedazo[0] == 'a:': #arcos
            if pedazo[3]=='1':
                print("\\draw (n%d) edge  (n%d);" %(int(pedazo[1]),int(pedazo[2])),file=output)
            else:
                print("\\draw (n%d) edge[lightgray,dashed]  (n%d);" %(int(pedazo[1]),int(pedazo[2])),file=output)

 
    print("\\end{tikzpicture}\n\\end{document}",file=output)
    input.close()
    output.close()
      
    os.system("pdflatex "+textFile[:-3]+'tex')
    os.startfile(textFile[:-3]+"pdf")



print(genera_instancia(nombre_instancia))






