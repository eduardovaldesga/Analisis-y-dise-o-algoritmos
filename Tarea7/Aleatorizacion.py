'''Esta aleatoización corresponde a un algoritmo constructivo para un problema que estoy estudiando.
Se desea detrminar la red de distribución electrica que minimice costo, perdidas de energía y probabilidad de fallos
Se tienen subestaciones, centros de transformación y lineas de distribucion. Las subestaciones y CT se consideran nodos 
de un grafo y las lineas de distribución como arcos. Se cuenta con una infraestructura actual y otra futura. Se debe satisfacer
la demanda de todos los centros de transformación
Se busca determinar redes radiales siendo la solución al problema un bosque donde las subestaciones son las raices
Por el momento el constructivo, solo considera la longitud total de la red. A partir de subestaciones seleccionadas al azar
se construye un bosque usando el algoritmo Dijkstra. En el punto en que Dijkstra elige el nodo mas cercano para comenzar ramificar,
se permite elegir dentro de un grupo de los mas cercanos, pudiendo generar multiples soluciones.
El costo de instalación depende de la longitud de la red y de otros factores; por el momento costo=longitud
Se puede cambiar, el criterio de aspiración en la construcción favoreciendo otras cualidades de la red, que tienen mas que ver
con la carga de los nodos.
La solución se presenta como una lista de predecesores donde :
    -1 : subestación utilizada
    -2: subestación no utilizada
'''

from Grafo import Grafo
from random import choice,random, randint
from math import inf
from PriorityQueueDict import PQDict
A=4
            
            
class Solucion:
    """Clase Solucion:\n
        pred (list): contiene los predecesores de cada nodo, de aqui se extrae el bosque solución\n
        costo (int): costo de la implementación\n
        fiabilidad (int): \n
        perdidas(int);
        """
    def __init__(self,G):
        
        self.pred=[-2]*(G.N) #lista de predecesores (representación 1 del bosque)
        self.ady=dict([(i,[]) for i in range(G.N)]) #lista de adyacencia (representación 2 del bosque)
        self.tipoSubE={} #tipos de subestaciones
        self.tipoLineas={} #tipos de lineas
        self.cargaNodos=[0]*G.N #carga de los nodos (demanda)
        for i in G.lista:
            if i>=G.numSubE:
                self.cargaNodos[i]=G.lista[i]['info'].demanda
        self.cargaAcumNodos=[0]*G.N #carga acumulada de los nodos (intensidad de las lineas en la solucion)
        self.distancia=[0]*G.N #distancia recorrida hasta llegar al i-ésimo nodo
        #objetivos
        self.costo=inf
        self.fiabilidad=inf
        self.perdidas=inf
        #para NSGA2
        self.rank=None
        self.numDominados=None
        
    def __hash__(self):
        return hash((self.costo,self.fiabilidad,self.perdidas))
        
        
    def __repr__(self):
        s=''
#        for i in range(len (self.pred)):
#            if self.pred[i]>=0:
#                s+="(%d,%d) "%(self.pred[i],i)
        return s+"\n%s costo=%.2f fiabilidad=%.2f perdidas=%.2f"%(self.pred,self.costo,self.fiabilidad,self.perdidas)    
    
    def __eq__(self,other):
        return (self.costo,self.fiabilidad,self.perdidas)==(other.costo,other.fiabilidad,other.perdidas)
    def __le__(self,other):
        return (self.costo,self.fiabilidad,self.perdidas)<=(other.costo,other.fiabilidad,other.perdidas) and self is not other
        
    

        
    def calculaCosto(self,G):
        'calcula la longitud de la solución'       
        
        self.costo=0
        for i in range(G.N):
            if self.pred[i]>=0:
                self.costo+=G.lista[self.pred[i]][i].longitud
    
                  
            

    def pesoArco(self,i,j,G,metrica=None):
        """Regresa el peso del arco (i,j) en dependencia de la metrica seleccionada:\n
        Caso 1:MinimaLongitud\n
        Caso 2: MinimaCarga\n
        Caso 3: MinimaCargaAcumulada\n
        Caso 4: MaximaCargaAcumulada\n
        """
        if metrica is None:
            metrica='longitud'
            
        if metrica in ['MinimaLongitud','longitud','l',1]:
            return G.lista[i][j].longitud
        if metrica in ['MinimaCarga','carga','c',2]:
            return self.cargaNodos[j]
        if metrica in ['MinimaCargaAcumulada','cargaAcumulada','cA',3]:
            return self.cargaAcumNodos[i]+self.cargaNodos[j]

    """"            :         Fase 1: Selección de subestaciones		               """

#Caso1
    def SeleccionarSubE(self,G):
        'Seleccionar todas las subestaciones existentes mas algunas propuestas aleatoreamente'
        for i in [i for i in range(G.numSubE) if G.lista[i]['info'].on or (not G.lista[i]['info'].on and random()<0.5)]:
            if G.lista[i]['info'].on or (not G.lista[i]['info'].on and random()<0.5):
                self.pred[i]=-1 #-1 significa que la subestación sera raiz del arbol
                
        
                
#Caso 2
    def SeleccionarSubEAleatoriamente(self,G):
        'Seleccionar aleatoriamente  las subestaciones, existentes o propuestas'
        for i in range(G.numSubE):
            if G.lista[i]['info'].on  and random()<0.5:
                self.pred[i]=-1 #-1 significa que la subestación sera raiz del arbol
        if -1 not in self.pred: #Asegurar que una subestacion es seleccionada
            self.pred[choice([i for i in range(G.numSubE) if G.lista[i]['info'].on])]=-1
            
            
            
    def Dijkstra(self,G,lineas=None,dist=None,permanente=None,metrica=None):
        """Encuentra el camino mas corto de los nodos hacia las subestaciones. 
        Modifica el arbol de predecesores (pred).
        La distancia entre nodos puede interpretarse dependiendo del objetivo\n
        Caso 1:MinimaLongitud\n
        Caso 2: MinimaCarga\n
       """
        #dist: distancia desde las raices(subestaciones)
        #permanente: conjunto de nodos etiquetados permanentemente
        
        if lineas is None:
            lineas=[]
        if dist is None:
            dist={}
        if permanente is None:
            permanente=set()
        if metrica is None:
            metrica='longitud'
        if len(dist)==0:
            #fijar todas las distancias en infinito excepto las raices      
        
            for i in range(G.numSubE):
                if self.pred[i]==-1:
                    dist[i]=0
            for i in range(G.numSubE,G.numNodos+G.numSubE):
                dist[i]=inf
        
        temp=PQDict([(key,value) for key,value in dist.items() if key not in permanente])
  
        global A
        #mientras existan nodos temporales
        while len(temp)>0:
            
            #seleccionar un nodo de entre los A primeros de menor distancia que no este etiquetado            
            s=[] #lista de mejores candidatos
            for i in temp._heap:  
                if i.pkey==inf:
                    break
                s.append(i.dkey)
            if len(s) is 0: #solo hay infinitos en temp, puede pasar en MutacionFinal
                s.append(temp._heap[0].dkey)
            x=s[randint(0,min([A,len(s)])-1)  ]
            #actualizar distancias de nodos adyacentes
            for a in G.lista[x]:
#                print(x,a)
                if a!='info':
                    
                    if (dist[x]+self.pesoArco(x,a,G,metrica)<dist[a] and a not in permanente):
#                        print(x,a, self.distancia[x],G.lista[x][a].longitud)
                        dist[a]=dist[x]+self.pesoArco(x,a,G,metrica) #G.lista[x][a].obj(metrica)
                        temp[a]=dist[a]
                        self.pred[a]=x
                        
                        self.distancia[a]=self.distancia[x]+G.lista[x][a].longitud
            temp.__delitem__(x)
            
            permanente.add(x)
        #actualizar ady:  
        for i in range(G.numSubE,G.numSubE+G.numNodos):
            self.ady[self.pred[i]]+=[i]
        self.calculaCosto(G)
        
        
G=Grafo("instancia.txt") 
for i in range(5):      
    X=Solucion(G)
    X.SeleccionarSubEAleatoriamente(G)
    X.Dijkstra(G)
    print(X)