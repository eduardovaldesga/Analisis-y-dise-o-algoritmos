"""Estructura para grafo"""

class SubE:
    def __init__(self,info_subE):
        [self.id,self.x,self.y,self.on,self.power]=[int(m) for m in info_subE]
    def __repr__(self):
        return "%d\t%d\t%d\t%d\t%d\t" %(self.id,self.x,self.y,self.on, self.power)
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return (self.id) == (other) 

class Nodo:
    def __init__(self,info_nodo):
        [self.id,self.x,self.y,self.on,self.demand]=[int(m) for m in info_nodo]
    def __repr__(self):
        return "%d\t%d\t%d\t%d\t%d\t" %(self.id,self.x,self.y,self.on, self.demand)
    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return (self.id) == (other)    
        

class Arco:
    def __init__(self,info_arco):
        [self.start,self.end,self.on,self.length,self.capacity]=[int(m) for m in info_arco]
    def __repr__(self):
        return "%d\t%d\t%d\t%d\t%d\t" %(self.start,self.end,self.on,self.length,self.capacity)
       

    

    

class grafo:

    #lista
    #nodo   /   info nodo   /               aristas
    #           demanda/etiqueta/etc     nodo final / info:arista
    lista=dict()
    

    def __init__(self,textFile=None):
        if textFile is not None:
                  
            #leer instancia
            input=open(textFile,'r')
            
#input = open("C:\Users\Eduardo\Google Drive\Doctorado\Analisis y diseño de algoritmos\Programas\lol.txt", 'r')		
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
            string+=str(n.id)+'=> '
            for a in self.lista[n]:
                if a!='info':
                    string+=str(a)+' '
            string+='\n' 
        return string
#        return str(self.lista)
            


    def agregaNodo(self,nodo):
        'agrega el nodo n con su info a la lista'
        self.lista[nodo]={'info':nodo}
       

    
    def agregaArco(self,arco):
        'agrega la arista (inicio,fin) junto con su info'
        #ind=[item["nodo"].id for item in self.lista]       
        self.lista[arco.start][arco.end]=arco
        

#class Pila:
#    def __init__(self,x):
#        p=x
#    def inserta(self,x):
#        p=[x]+p
#    def elimina(self):
#        p=p[1:]
    
        
     
  


    
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
                    
            
        
    
#G=grafo("instanciaDFS.txt")
##print(G)
#visitados=set([0])
#pila=[0]    
#   
#DFS(G,pila,visitados)
    


            
    
    


