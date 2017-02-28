import collections


class grafo:

    #lista
    #nodo   /   info nodo   /               aristas
    #           demanda/etiqueta/etc     nodo final / info:arista
    lista=collections.OrderedDict()
    

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
                if pedazo[0] == 'n:':
                    
                    #nodos.append(nodo(pedazo[1], int(pedazo[2])))
                    self.agregaNodo(pedazo[1],{"X":int(pedazo[2]),"Y":int(pedazo[3]),"disponible":int(pedazo[4]),"demanda":int(pedazo[5])})
                elif pedazo[0] == 'a:':
                    desde = pedazo[1]
                    hasta = pedazo[2]
##                    assert desde in self.lista.keys()
##                    assert hasta in self.lista.keys()
                    #arcos.append(arco(desde, pedazo[2], int(pedazo[3]), int(pedazo[4])))
                    self.agregaArista(desde,{'fin':hasta,'costo':int(pedazo[3]),'longitud': int(pedazo[4])})
            input.close()
            
            

    def __repr__(self):
        string=''
        for n in self.lista:
            string+=str(n)+'=>'
            if 'arco' in self.lista[n]:
                for a in self.lista[n]['arco']:
                    string+=str(a['fin'])+' '
            string+='\n'

        
            
        
        return string
            


    def agregaNodo(self,n,info_n):
        'agrega el nodo n con su info a la lista'
        self.lista[n]= info_n
        #self.lista[n]['arco']=None
       

    
    def agregaArista(self,inicio,info_arista):
        'agrega la arista (inicio,fin) junto con su info'
        self.lista[inicio].setdefault('arco',[]).append(info_arista)
        


    
    def getAtrrNodo(self,atributo,n):
        'regresa el "atributo" del nodo n'
        n=str(n)
        assert n in self.lista #el nodo esta en la lista?       
        assert atributo in self.lista[n] #el nodo tiene este atributo?       
        return self.lista[n][atributo]
            

    def getAtrrArista(self,atributo,inicio,final):
        'regresa el "atributo" del arco (inicio,fin)'
        inicio=str(inicio)
        final=str(final)
        assert inicio in self.lista #hay un arco con este inicio?
        assert final in [a['fin'] for a in self.lista[inicio]['arco']] #hay un arco con este final?
        r=[a for a in self.lista[inicio]['arco'] if a['fin']==final]
        assert atributo in r[0] #el arco tiene este atributo?      
        return  r[0][atributo]
               
                




F=grafo("instancia.txt")
print (F)
print (F.getAtrrNodo('disponible',3))
print (F.getAtrrArista('costo',3,28))
        


            
    
    


