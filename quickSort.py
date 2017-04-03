# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 12:24:42 2017

@author: Eduardo
"""
from random import randint
costo=0
rec=0
def quickSort(lista):
#    print(lista)
    global costo
    global rec
    #elegir pivote
    n=len(lista)    
    rec+=1
    
    if n<=1:        
        costo+=1
        return lista
    if n==2:
        if lista[0]<=lista[1]:
            costo+=2
            return lista
        else:
            costo+=2
            return [lista[1],lista[0]]
        
    
    p_idx=randint(0,n-1)
    pivote=lista[p_idx]
    costo+=1     
    l_izq=[]
    l_der=[]
    idx_izq=0
    idx_der=-1
    
    #verificar duplicados    
    temp=p_idx+1
    if temp<n-1:
        while pivote==lista[temp]:
            temp+=1
            if temp==n-1:
                return lista
        
        
            
    
    while idx_der >-(n-idx_izq): #hasta que los indices se crucen            
        #comparar elemento de indice izquierdo
        if lista[idx_izq]<=pivote:
            l_izq.append(lista[idx_izq])
        else:
            l_der.append(lista[idx_izq])
        #comparar elemento de indice derecho
        if lista[idx_der]<=pivote:
            l_izq.append(lista[idx_der])
        else:
            l_der.append(lista[idx_der])
        costo+=3
        #actualizar indices
        idx_izq+=1
        idx_der-=1
    #para el caso de que n sea impar, los indices cambian de orden
    if idx_der ==-(n-idx_izq):
        costo+=1
        l_izq.append(lista[idx_izq])
    
    return quickSort(l_izq)+quickSort(l_der)

#print(quickSort([randint(0,100) for i in range(30)])) 
#print(rec) 

def experimento(num_var,num_rep,max_number=100):
    global costo
    data=open("valores_quicksort.txt",'w')
    print("tamano\treplica\tcosto",file=data)
    for tam in [2**j for j in range(num_var)]:
        for rep in range(num_rep):
            lista=[randint(0,max_number) for i in range(tam)]
            costo=0
            quickSort(lista)
            print("%d\t%d\t%d" %(tam,rep+1,costo),file=data)
            
    data.close()
    
experimento(15,10)