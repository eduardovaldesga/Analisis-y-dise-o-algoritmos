import numpy as np

def str2number(s):
    'convierte un string s en numero, sea entero o flotante. Si s no es un número, permanece como string'
    if isinstance(s,(int,float,np.int64)):
        return s
    if len(s)>1 and not isinstance(s,str):
        return [str2number(cadena) for cadena in s]
    else:
    
        if not s.replace('.','',1).isdigit():
            return s
        else:        
            if '.' in s:
                ss=s.split('.')
                if int(ss[-1]) is 0:
                    return int (ss[0])
                else:
                    return float(s)
            else:
                return int(s)

class SubE:
    """Clase SubEstacion:\n
        id (int) : identificador de la subestación\n
        (x,y) (int ): coordenadas cartesianas de la posición \n
        on (bool): representa si la subE está disponible o no actualmente\n
        power (int): potencia de la subE\n
        """
    def __init__(self,info_subE):
        'info_subE=[id,x,y,on,power] en ese orden'
        [self.id,self.x,self.y,self.on]=[str2number(m) for m in info_subE]
    def __repr__(self):
        return "%s\t%s\t%s\t%s\t" %(self.id,self.x,self.y,self.on)
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return (self.id) == (other) 

class Nodo:
    """Clase Nodo:\n
        id (int) : identificador del nodo\n
        (x,y) (int ): coordenadas cartesianas de la posición \n
        on (bool): representa si el nodo está disponible o no actualmente\n
        demand (int): demanda del nodo\n
        """
    def __init__(self,info_nodo):
        'info_nodo=[id,x,y,on,demand] en ese orden'
        [self.id,self.x,self.y,self.on,self.demand]=[str2number(m) for m in info_nodo]
    def __repr__(self):
        return "%s\t%s\t%s\t%s\t%s\t" %(self.id,self.x,self.y,self.on, self.demand)
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return (self.id) == (other)    
        

class Arco:
    """Clase Arco:\n
        start (int) : nodo inicio del arco\n
        end (int ): nodo final del arco \n
        on (bool): representa si el arco está disponible o no actualmente\n
        length (int): longitud del arco\n
        capacity (int): capacidad del arco\n
        """
    def __init__(self,info_arco):
        'info_arco=[start,end,on,length,capacity] en ese orden'
        [self.start,self.end,self.on,self.length,self.topologia]=[str2number(m) for m in info_arco]
    def __repr__(self):
        return "%s\t%s\t%s\t%s\t%s\t" %(self.start,self.end,self.on,self.length,self.topologia)
       

    

    

class Grafo:
    """Clase Grafo:\n
    Contiene la información del grafo. Se llena con la información proporcionada en textFile.
    La instancia debe contener una lista de subestaciones, nodos y arcos cada uno en el formato respectivo:\n
    s: id    x    y    on    power\n
    n: id    x    y    on    demand\n
    s: start    end    on    length    capacity\n\n
    
    El grafo contiene:\n
    numSubE (int): numero de subestaciones\n
    numNodos (int): numero de nodos\n
    numArcos (int): numero de arcos\n
    una lista (lista) de tamaño numSubE+numNodos.\n
    Cada elemnto de la lista contiene la info de el nodo(subE) y  una lista de arcos. En total hay numArcos  arcos
    """
    #lista
    #nodo   /   info nodo   /               aristas
    #           demanda/etiqueta/etc     nodo final / info:arista
    'lista de nodos'
    lista=dict()
    

    def __init__(self,textFile=None):
        if textFile is not None:
                  
            #leer instancia
            input=open(textFile,'r')
            

            for linea in input:
                linea = linea.strip()
                if len(linea) == 0:
                    break
                pedazo = linea.split()
                
                if pedazo[0] == 's:':
                    self.agregaNodo(SubE(pedazo[1:]))
                elif pedazo[0] == 'n:':
                    #nodos.append(nodo(pedazo[1], int(pedazo[2])))
                    self.agregaNodo(Nodo(pedazo[1:]))
                    
                elif pedazo[0] == 'a:':
                    
#                    assert desde in self.lista.keys()
#                    assert hasta in self.lista.keys()
                    #arcos.append(arco(desde, pedazo[2], int(pedazo[3]), int(pedazo[4])))
                    self.agregaArco(Arco(pedazo[1:]))
            input.close()
            

    def __repr__(self):
        string=''
        for n in self.lista:
            string+=str(n)+'=> '
            for a in self.lista[n]:
                if a!='info':
                    string+=str(a)+' '
            string+='\n' 
        return string
#        return str(self.lista)
            


    def agregaNodo(self,nodo):
        'agrega el nodo n con su info a la lista'
        self.lista[nodo.id]={'info':nodo}
       

    
    def agregaArco(self,arco):
        'agrega la arista (inicio,fin) junto con su info'
        #ind=[item["nodo"].id for item in self.lista]       
        self.lista[arco.start][arco.end]=arco
        


        
     
  


    
def DFS(grafo,pila,visitados):
    if len(pila)==0:
        return 0
    
    
#    while(len(pila)>0):
    x=pila.pop()
    
    print(x)
    
    
    for a in grafo.lista[x]:
        if a!='info' and a not in visitados:            
            visitados.add(a)
            pila+=[a]
            print(visitados,pila)
            
    DFS(grafo,pila,visitados)
                    

def BFS(grafo,inicio):
    secuencia=[-2]*len(grafo.lista)
    l = 0
    nivel = {inicio: l}
    act = {inicio}
    secuencia[inicio]=-1
    while len(act) > 0:
        l += 1
        sig = set()
        for v in act:
            for w in grafo.lista[v]:
              if w != 'info' and w not in nivel: 
                  nivel[w] = l
                  sig.add(w)
                  secuencia[w]=v
        act = sig
    return secuencia
        
    

    


            
    
    


