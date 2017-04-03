# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 14:41:15 2017

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
print(procesa(genera_grupos(20)))
            