"""
Descripciรณn:
    Estas instancias son para un problema que busca encontrar una red de distribuciรณn electrica a menor costo. Se disponen de datos reales, las instancias basicamente deben representar un grafo no dirigido.
    
    Se disponen de subestaciones (subE) y centros de distribuciรณn(a quienes llamo nodos).
    Existen nodos y subE instaladas (a esto me refiero como disponibles) o que estan planteadas a futuro (no disponibles)
    Hay diferentes tipos de subestaciones, diferenciandolas basicamente su potencia maxima. Estos tipos de subestaciones se obtienen de datos reales
    Los centros de transformaciรณn tienen una demanda especifica. La distribuciรณn de la demanda es algo que aun no estudio, aqui la supongo como uniforme y acotada entre [DLOW,DUP] 
    Hay lineas de distribuciรณn (arcos) que transportan la energia de las subestaciones a los centros de transformaciรณn, pero no necesariamente directo; es decir, puedo conectar un nodo a traves de otros. Estos arcos tienen capacidades maximas, longitud, topologia y otras caracteristicas. La longitud es calculada como la distancia euclideana entre sus puntas. La topologรญa hace referencia al tipo de transporte, esta puede ser Aerea o suvterranea. Por ahora esto  es calculado de forma aleatroia pero desde luego debe considerarse una conexiรณn mรกs logica, como caminos de arcos de un solo tipo. Las caracteristicas restantes diferencian a las lineas en clases; esta informacion se obtiene de datos reales.
    Es importante a futuro que los nodos y subE se encuentren dentro de una rtegion determinada, como ejemplo ahora los coloco dentro del mapa de Mexico. Aqui selecciono al azar la posiciรณn de los nodos y tambien si estan disponibles o no.
    Debe existir una cantidad proporcional de subestaciones respecto a los nodos. Se esta manejando como PorSubE. Esto aun es un parametro que falta analizar mas a fondo
    La densidad del grafo la controlo con parametros que reflejan el numero de arcos que salen de cada nodo o subE (esto por separado)
    Puesto que se supone que la red (ya instalada o planificada) tiene cierto razonamiento, solo nodos cercanos pueden ser conectados pues la longitud impacta en el costo
    El parametro n describe la cantidad total de nodos y SubE que tiene la red

Restricciones de las instancias:
    Al menos una subestaciรณn estรก disponible
    Un arco disponible une dos nodos(o subE) disponibles
    Solo existe un arco de (i) a (j)
    Si existe el arco (i,j) tambiรฉn el retorno (j,i), ambos tienen las mismas propiedades
    Todos los nodos (o subE) disponibles son conexos
    
Grafica de instancias:
    La grafica hasta ahora muestra el mapa y el grafo.
    Las subestaciones son cuadrados y los nodos circulos
    El color negro denota la parte de la red ya instalada, el gris lo planificado
    Quiero manejar diferencia también entre lineas aereas o subterraneas
    
Pendientes:    
    Usar un porcentaje de nodos disponibles
    Asegurar que los nodos disponibles estan conectados a alguna SubE disponible (aun hay inconsistencias)
    Alejar subestaciones entre ellas 
    Los arcos que salen de la regiรณn deberรญan de ser mas reales y si no dibujarlos, aumentar su distancia en la instancia. Esto o verificar si es posible agregar una topologia de linea como 'marina'
"""



from random import randint, choice, random,shuffle,sample
from math import sqrt,ceil,inf
import numpy as np
import os 
from grafo import Grafo,Nodo,Arco,SubE
from shapely.geometry import Point,Polygon



nombre_instancia="instancia.txt"
n=120 #numero total de nodos (incluyendo subestaciones)
PORSubE=0.1 #'porcentaje de subestaciones respecto al total de nodos'
DLOW=20 #'cota inferior de demanda'
DUP=100 #'cota superior de demanda'
DENARCOS=0.05  #densidad de arcos salientes de nodos
DENARCOSSUBE=0.1  #densidad de arcos salientes de subestaciones
MAPA="coordenadas.txt" #nombre del archivo que  contiene al mapa

def random_points_within(poly, num_points,sep=0):
    'regresa n puntos dentro de la regiรณn poly'
    min_x, min_y, max_x, max_y = poly.bounds
#    points = []
    posibles=[]
    #identificar enteros dentro del poligono
    for x in np.arange(min_x,max_x,0.5):
        for y in np.arange(min_y,max_y,0.5): 
            if Point(x,y).within(poly):                
                posibles.append(Point(x,y))
            
                
    try:
        return sample(posibles,n)
    except:
        raise
        return posibles

def genera_instancia(textFile):    
    
#    leer poligono
    mex=open(MAPA,'r')
    coordenadas=[]
    for linea in mex:
        
        linea.strip()
        p=linea.split()
        if len(p)==0:
            break
        
        coordenadas.append(((float(p[0]),float(p[1]))))
    mapa=Polygon(coordenadas)
    
    
    G=Grafo()
    datos=open(textFile,"w")

    ID=0
    numSubE=int(PORSubE*n)
    X=[]
    Y=[]
    on=set()
    
    
    puntos=random_points_within(mapa,n)
    
    
    
#generar subestaciones
    puesto=[randint(0,1) for i in range(numSubE)]#asegura al menos una subestacion on
    if 1 not in puesto:
        puesto[0]=1
        shuffle(puesto)
    for i in range(numSubE):
#        punto=random_points_within(mapa,1,1)
#        print(punto)
        X.append(puntos[i].coords[0][0])
        Y.append(puntos[i].coords[0][1])   
        G.agregaNodo(SubE([i,"%.2f"%X[-1],"%.2f"%Y[-1],puesto[i]]))
        #print("s:\t"+str(ID)+"\t"+str(X[-1])+"\t"+str(Y[-1])+"\t"+str(puesto[i])+'\t'+str(potencia),file=datos)
        ID+=1
        if puesto[i]==1:
            on.add(i)
        

#generar nodos   
    for i in range(numSubE,n):
        #n: ID  X   Y   puesto/posible(1/0) demanda
#        punto=random_points_within(mapa,1)
        X.append(puntos[i].coords[0][0])
        Y.append(puntos[i].coords[0][1])
        puesto=choice([0,1])
        if puesto==1:
            on.add(ID)
        demanda=randint(DLOW,DUP)
        G.agregaNodo(Nodo([ID,"%.2f"%X[-1],"%.2f"%Y[-1],puesto,demanda]))
        ID+=1
        
    

#generar matriz distancias
    D=[]
    for i in range(0,n):        
        D.append([sqrt((X[i]-X[j])**2+(Y[i]-Y[j])**2) for j in range(0,n)])
            
   

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
            topologia=choice(['Aerea','Subterranea'])
            G.agregaArco(Arco([inicio,f,puesto,"%.2f"%longitud,topologia]))
            G.agregaArco(Arco([f,inicio,puesto,"%.2f"%longitud,topologia]))
    
    #agrupar grupos desconexos de nodos activos
    
    grupos_ok={}
    grupos_mal=[]
    revisados=set()
    subestaciones=set([x for x in range(int(DENARCOSSUBE*n)) if x in on])
    
    for inicio in on:
        if inicio not in revisados: #subestacion activa... buscar nodos conexos
            revisados.add(inicio)
            cola=[inicio]
            grupo=[]
            while len(cola)>0:
#                print(cola,revisados)
#                input()
                x=cola.pop(0)
                
                for final in G.lista[x]:
                    if final in on and final is not inicio and final not in grupo:
                        grupo.append(final)
                        cola.append(final)
                        revisados.add(final)
            interseccion=subestaciones.intersection(set(grupo))
            try:
                grupos_ok[interseccion.pop()]=grupo
            except:
                grupos_mal.append(grupo)
    print(grupos_ok,grupos_mal)
    
#    if len(grupos_ok)<len(subestaciones):
#        falt=0
#        for c in grupos_ok:
#            falt+=len(subestaciones.intersection(grupos_ok[c])) #hay varias subestaciones conectadas
#        if falt<len(subestaciones):#hay subestaciones que no se agregaron
            
            
        
    for grupo in grupos_mal:
        #buscar el grupo mas cercano
        distancia=inf       
        for cjto in grupos_ok:
            for x in grupo:
                for y in grupos_ok[cjto]:
                    if D[x][y]<distancia:
                        inicio,final,distancia=x,y,D[x][y]
        
        #agregar arco inicio--final
        G.agregaArco(Arco([inicio,final,1,"%.2f"%distancia,choice(['Aerea','Subterranea'])]))
        print("se agrego el arco %d -- %d"%(inicio,final))
    
#imprimir instancia
    for g in G.lista:
        if g<numSubE:            
            print("s:\t"+str(G.lista[g]['info']),file=datos)
        else:            
            print("n:\t"+str(G.lista[g]['info']),file=datos)
    for g in G.lista:
        for a in G.lista[g]:
            if a!='info':
                print("a:\t"+str(G.lista[g][a]),file=datos)
            
    datos.close()
    
    graficaInstancia(textFile)
            
    return G








def graficaInstancia(textFile):
    'grafica una instancia, tanto el mapa como el grafo'
    output=open(textFile[:-3]+'tex','w')
    print("\\documentclass{standalone}\n\\usepackage{tikz}\n\\usetikzlibrary{decorations.pathmorphing}\n\\begin{document}\n\\begin{tikzpicture}[node distance = 0.5cm,inner sep = 2pt]\n\\tikzstyle{ann} = [fill=white,font=\scriptsize,inner sep=1pt] \n",file=output)

    
    #graficar mapa
    mapa=open(MAPA,'r')
    c=0   
    print("%c//////////////////////    dibuja mapa     ////////////////////////\n" %('\u0025'),file=output)
    for linea in mapa:
        linea = linea.strip()
        if len(linea) == 0:
            break
        pedazo = linea.split()
       
        #agrega nodo
        print("\\draw (%f,%f) node (mark%d)  {};" %(float(pedazo[0]),float(pedazo[1]),c),file=output)
        c+=1
    print("\n\\draw\\foreach \\i [count=\\xi from 1] in {0,...,%d}{(mark\\i) edge (mark\\xi)};\n" %(c-2),file=output)
    
      
    
    
    print("%c//////////////////////    dibuja grafo     ////////////////////////\n" %('\u0025'),file=output)
    #leer instancia
    input=open(textFile,'r')


    
    for linea in input:
        linea = linea.strip()
        if len(linea) == 0:
            break
        pedazo = linea.split()   
        if pedazo[0]=='s:': #subestaciones
            if pedazo[4]=='1':
                print("\\draw (%.2f,%.2f) node[fill=black,draw, minimum size=6pt,text=white] (n%d) {};  %csubestacion" %(float(pedazo[2]),float(pedazo[3]),int(pedazo[1]),'\u0025'),file=output)
#                print("\tnode (e%d) [above of=n%d] {{\scriptsize %d}};" %(int(pedazo[1]),int(pedazo[1]),int(pedazo[5])),file=output)
            else:
                print("\\draw (%.2f,%.2f) node[lightgray,fill=lightgray,draw, minimum size=6pt,text=black] (n%d) {};  %csubestacion" %(float(pedazo[2]),float(pedazo[3]),int(pedazo[1]),'\u0025'),file=output)
#                print("\tnode (e%d) [text=lightgray,above of=n%d] {{\scriptsize %d}};" %(int(pedazo[1]),int(pedazo[1]),int(pedazo[5])),file=output)
        elif pedazo[0] == 'n:': #nodos
            if pedazo[4]=='1':               
                print("\\draw (%.2f,%.2f) node[fill=black,circle,draw, minimum size=1pt] (n%d) {};  %cnodo" %(float(pedazo[2]),float(pedazo[3]),int(pedazo[1]),'\u0025'),file=output)
#                print("\tnode (e%d) [above of=n%d] {{\scriptsize %d}};" %(int(pedazo[1]),int(pedazo[1]),int(pedazo[5])),file=output)
            else:
                print("\\draw (%.2f,%.2f) node[lightgray,fill=lightgray,dashed,circle,draw, minimum size=1pt] (n%d) {};  %cnodo" %(float(pedazo[2]),float(pedazo[3]),int(pedazo[1]),'\u0025'),file=output)      
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






