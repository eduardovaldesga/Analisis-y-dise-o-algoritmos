from random import randint, choice, random,sample,shuffle


def sample_wr(population, k):
    "Chooses k random elements (with replacement) from a population"
    return [choice(population) for i in range(k)]


def clausulaTrueCNF(numVariables, asign): #uuu
    x=[]
    if random()<0.5: #tautologia
        n=str(randint(1,numVariables))        
        x+=['!x'+n+'\t','x'+n+'\t',choice(['','!'])+'x'+str(randint(1,numVariables))+'\t']  #(-x u x)        
    else: #asegurar una clausula verdadera        
        c=set(['x'+str(r) for r in range(1,numVariables+1)])       
        c=asign|set(['!'+item for item in c-asign])        
        x.append(choice(list(c))+'\t')            
        x+=[choice(['','!'])+'x'+str(randint(1,numVariables))+'\t' for i in [1,2]]
    shuffle(x)
    return ''.join(x)            


def clausulaFalseCNF(numVariables, asign): #uuu
    c=set(['x'+str(r) for r in range(1,numVariables+1)])       
    c=(c-asign)|set(['!'+item for item in asign])  #todas son clausulas falsas
    return ''.join([v+'\t' for v in sample_wr(list(c),3)])

    
def clausulaTrueDNF(numVariables, asign): #^^^       
    #todas son clausulas verdaderas
    c=set(['x'+str(r) for r in range(1,numVariables+1)])       
    c=asign|set(['!'+item for item in c-asign])    
    return ''.join([v+'\t' for v in sample_wr(list(c),3)])


def clausulaAleatoria(numVariables):
    return ''.join([choice(['','!'])+'x'+str(randint(1,numVariables))+'\t' for v in range(3)])


def clausulaFalseDNF(numVariables, asign): #^^^ 
        x=[]
        if random()<0.5: #tautologia
            n=str(randint(1,numVariables))
            x+=['!x'+n+'\t','x'+n+'\t',choice(['','!'])+'x'+str(randint(1,numVariables))+'\t']  #(-x ^ x)
        else: #asegurar una clausula falsa        
            c=set(['x'+str(r) for r in range(1,numVariables+1)])       
            c=(c-asign)|set(['!'+item for item in asign])  #todas son clausulas falsas        
            x.append(choice(list(c))+'\t')
            x+=[choice(['','!'])+'x'+str(randint(1,numVariables))+'\t' for i in [1,2]]
        shuffle(x)
        return ''.join(x)


def genera_instancia_tripleSAT(numLineas,numVariables,numInstancia,cnf,true):
    'genera una instancia para cnf(o no) cuya respuesta es true (o no)'
    'con numLineas clausulas y nuVariables variables distintas'
    assign=open("asignacion_tripleSAT"+str(numInstancia)+".txt",'w')    
    A=set(['x'+str(v) for v in sample(range(1,numVariables+1),randint(1,numVariables))])
    print('\n'.join(list(A)),file=assign)    
    instance=open("instancia_tripleSAT"+str(numInstancia)+".txt",'w')
    if cnf and true: #todas las clausulas deben ser verdaderas
        clausulas=[clausulaTrueCNF(numVariables,A) for i in range(numLineas)]
    elif cnf and not true:#al menos una clausula es falsa
        n=randint(1,numLineas)
        clausulas=[clausulaAleatoria(numVariables) for i in range(n)]
        clausulas+=[clausulaFalseCNF(numVariables,A) for i in range(numLineas-n)]
    elif not cnf and true: #al menos una clausula es verdadera
        n=randint(1,numLineas)
        clausulas=[clausulaAleatoria(numVariables) for i in range(n)]
        clausulas+=[clausulaTrueDNF(numVariables,A) for i in range(numLineas-n)]
    elif not cnf and not true:  #todas las clausulas deben ser falsas
        clausulas=[clausulaFalseDNF(numVariables,A) for i in range(numLineas)]
    else:
        clausulas=[clausulaAleatoria(numVariables) for i in range(numLineas)]
    print('\n'.join(clausulas),file=instance)


genera_instancia_tripleSAT(20,8,2,False,False)

        
            
        
        
    
