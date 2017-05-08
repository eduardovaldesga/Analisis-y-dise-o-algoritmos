

#suponiendo que las aristas vienen ordenadas y que el grafo es conexo:
def arbolExpMin(textfile,numNodos):
    d = dict()
    costo=0
    with open(textfile, "r") as archivo:
        for linea in archivo:
            x, y, c= (linea.strip()).split()
            dx=d.get(x, {x})
            dy=d.get(y, {y})
            if dx is not dy:
                n = dx | dy
                for cuate in n:
                    d[cuate] = n                
                costo+=int(c)
                if len(n)==numNodos:
                    return costo
            
  
         
#print(reach('1','6',"aristas.txt"))
print("costo =",arbolExpMin("arbolexpmin.txt",6))
