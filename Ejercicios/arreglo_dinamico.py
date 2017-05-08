# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 14:41:15 2017
Para simular comportamiento de arreglos dinamicos
@author: Eduardo
"""


from random import choice,randint,random

def genera_grupos(tam):
    temp=0
    grupos=[]
    while temp<tam:
        n=randint(0,tam-temp)
        if random()<0.5:
            grupos+=['agrega']*n
        else:
            grupos+=['eliminar']*n
        temp+=n
    return grupos

umbral_menor=0.4
umbral_mayor=0.6

def procesa(seq):
    tam_inicial=2
    max_tamano=20
    tamano=0
    costo=0
    for orden in seq:
        if orden=='agrega':
            tamano+=1
            if tamano/max_tamano>umbral_mayor:
                max_tamano*=2
                costo+=tamano
        else:
            if tamano>0:
                tamano-=1
            
            if tamano/max_tamano<umbral_menor and tamano>tam_inicial:
                max_tamano//=2
                costo+=tamano
    return costo,max_tamano

#print(procesa([choice(['agrega','elimina']) for i in range(20)]))
#print(procesa(genera_grupos(20)))

def experimento(num_umbrales,num_seq,num_rep,grupos):
    data=open("valores_arreglo_dinamico.txt",'w')
    print("umbral_menor\tumbral_mayor\ttam_seq\tnum_rep\tcosto\tmaximo_tamano",file=data)
    for umbral_menor,umbral_mayor in [[random(), random()] for i in range(num_umbrales)]:
        if umbral_mayor<umbral_menor:
            umbral_mayor,umbral_menor=umbral_menor,umbral_mayor
#            temp=umbral_menor
#            umbral_menor=umbral_mayor
#            umbral_mayor=temp
        for tamano in [2**j for j in range(3,num_seq)]:
            for rep in range(num_rep):
                if grupos:
                    costo,max_tam=procesa(genera_grupos(tamano))
                else:
                    costo,max_tam=procesa([choice(['agrega','elimina']) for i in range(tamano)])
                print("%.2f\t%.2f\t%d\t%d\t%d\t%d"%(umbral_menor,umbral_mayor,tamano,rep+1,costo,max_tam),file=data)
                
experimento(10,10,5,1)
            
            