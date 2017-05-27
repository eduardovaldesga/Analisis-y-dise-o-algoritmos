# -*- coding: utf-8 -*-
"""
Created on Mon May 22 12:57:41 2017
Transición de fase para MAX 3SAT
Instancias CNF
Se supone que cuando la razón clausulas/variables es 3.6 se hace el salto
@author: Eduardo
"""
import generaInstancias3SAT as instance
from GA import GA3SAT
from matplotlib import pyplot

tiempo={}
objetivo={}
for numClaus in range(10,2000,300):
    for numVar in range(10,2000,300):
#        print(numClaus,numVar)
        instance.genera_instancia_tripleSAT(numClaus,numVar,"%d-%d"%(numClaus,numVar),True,True)
        time,obj=GA3SAT("instancia_tripleSAT(True,True)%d-%d.txt"%(numClaus,numVar),numVar)   
#        print(numClaus,numVar,time,obj)
        temp1=tiempo.get("%.2f"%float(numClaus/numVar),[])
        if len(temp1)==0:
            tiempo["%.2f"%float(numClaus/numVar)]=[]
        temp2=objetivo.get("%.2f"%float(numClaus/numVar),[])
        if len(temp2)==0:
            objetivo["%.2f"%float(numClaus/numVar)]=[]
        tiempo["%.2f"%float(numClaus/numVar)].append(time)
        objetivo["%.2f"%float(numClaus/numVar)].append(obj)
#hacer promedios
razon=[]
tiempo_prom=[]
obj_prom=[]
for key in tiempo:
    razon.append(float(key))
    suma=0
    for t in tiempo[key]:
        suma+=t
    tiempo_prom.append((float(key),suma/len(tiempo[key])))
for key in objetivo:
    suma=0
    for t in objetivo[key]:
        suma+=t
    obj_prom.append((float(key),suma/len(objetivo[key])))

tiempo_prom.sort()
obj_prom.sort()
r=[]
t=[]
o=[]
for u in tiempo_prom:
    i,j=u
    r.append(i)
    t.append(j)
for u in obj_prom:
    i,j=u
#    r.append(i)
    o.append(j)
#print(r,t)
pyplot.plot(r,t)
pyplot.xlabel('Razon clausulas/variables')
pyplot.ylabel('tiempo ejecucion GA (s)')
pyplot.show()

pyplot.plot(r,o)
pyplot.xlabel('Razon clausulas/variables')
pyplot.ylabel('Porcentaje de clausulas satisfechas')
pyplot.show()
