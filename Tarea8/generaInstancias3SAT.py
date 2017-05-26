# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 11:24:33 2017
Generador de instancias para Triple Sat
@author: Eduardo
"""

from random import choice,sample,randint,random,shuffle
from time import time


def sample_wr(population, k):
    "Chooses k random elements (with replacement) from a population"
    return [choice(population) for i in range(k)]

#generación de clausulas, su valor de verdad depende de tautologias o de los valores de las variables en asign

def clausulaTrueCNF(numVariables, asign): #uuu
    x=[]
    if random()<0.5: #tautologia: x + !x + y
        n=str(randint(1,numVariables))        
        x+=['!x'+n+'\t','x'+n+'\t',choice(['','!'])+'x'+str(randint(1,numVariables))+'\t']  #(-x u x)        
    else: #en base a los valores: al menos una variable es verdadera   
        c=set(['x'+str(r) for r in range(1,numVariables+1)])       
        c=asign|set(['!'+item for item in c-asign])        
        x.append(choice(list(c))+'\t')            
        x+=[choice(['','!'])+'x'+str(randint(1,numVariables))+'\t' for i in [1,2]]
    shuffle(x)
    return ''.join(x)            


def clausulaFalseCNF(numVariables, asign): #uuu
    c=set(['x'+str(r) for r in range(1,numVariables+1)])       
    c=(c-asign)|set(['!'+item for item in asign])  #todas son  falsas
    return ''.join([v+'\t' for v in sample_wr(list(c),3)])

    
def clausulaTrueDNF(numVariables, asign): #^^^       
    #todas son verdaderas
    c=set(['x'+str(r) for r in range(1,numVariables+1)])       
    c=asign|set(['!'+item for item in c-asign])    
    return ''.join([v+'\t' for v in sample_wr(list(c),3)])


def clausulaAleatoria(numVariables):
    return ''.join([choice(['','!'])+'x'+str(randint(1,numVariables))+'\t' for v in range(3)])


def clausulaFalseDNF(numVariables, asign): #^^^ 
        x=[]
        if random()<0.5: #tautologia : !x + x + y
            n=str(randint(1,numVariables))
            x+=['!x'+n+'\t','x'+n+'\t',choice(['','!'])+'x'+str(randint(1,numVariables))+'\t']  #(-x ^ x)
        else: #asegurar una variable falsa        
            c=set(['x'+str(r) for r in range(1,numVariables+1)])       
            c=(c-asign)|set(['!'+item for item in asign])  #todas son clausulas falsas        
            x.append(choice(list(c))+'\t')
            x+=[choice(['','!'])+'x'+str(randint(1,numVariables))+'\t' for i in [1,2]]
        shuffle(x)
        return ''.join(x)


def genera_instancia_tripleSAT(numLineas,numVariables,nomInstancia,cnf,true):
    'genera una instancia para cnf(dnf) cuya respuesta es true (false)'
    'con numLineas clausulas y nuVariables variables distintas'
    assign=open("InstanciasTripleSAT/asignacion_tripleSAT("+str(cnf)+","+str(true)+")"+str(nomInstancia)+".txt",'w')    
    A=set(['x'+str(v) for v in sample(range(1,numVariables+1),randint(1,numVariables))])
    print('\n'.join(list(A)),file=assign)
    instance=open("InstanciasTripleSAT/instancia_tripleSAT("+str(cnf)+","+str(true)+")"+str(nomInstancia)+".txt",'w')
    if cnf and true: 
        clausulas=[clausulaTrueCNF(numVariables,A) for i in range(numLineas)]
    elif cnf and not true:
        n=randint(1,numLineas)
        clausulas=[clausulaAleatoria(numVariables) for i in range(n)]
        clausulas+=[clausulaFalseCNF(numVariables,A) for i in range(numLineas-n)]
    elif not cnf and true: 
        n=randint(1,numLineas)
        clausulas=[clausulaAleatoria(numVariables) for i in range(n)]
        clausulas+=[clausulaTrueDNF(numVariables,A) for i in range(numLineas-n)]
    elif not cnf and not true:  
        clausulas=[clausulaFalseDNF(numVariables,A) for i in range(numLineas)]
    else:
        clausulas=[clausulaAleatoria(numVariables) for i in range(numLineas)]
    print('\n'.join(clausulas),file=instance)
