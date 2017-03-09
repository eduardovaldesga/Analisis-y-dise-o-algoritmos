
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


def genera_instancia_tripleSAT(numLineas,numVariables,nomInstancia,cnf,true):
    'genera una instancia para cnf(o no) cuya respuesta es true (o no)'
    'con numLineas clausulas y nuVariables variables distintas'
    assign=open("InstanciasTripleSAT/asignacion_tripleSAT("+str(cnf)+","+str(true)+")"+str(nomInstancia)+".txt",'w')    
    A=set(['x'+str(v) for v in sample(range(1,numVariables+1),randint(1,numVariables))])
    print('\n'.join(list(A)),file=assign)
    instance=open("InstanciasTripleSAT/instancia_tripleSAT("+str(cnf)+","+str(true)+")"+str(nomInstancia)+".txt",'w')
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





#leer asiganciones
def asignacion(assign):
    A = set()
    with open(assign,'r') as asig:
        for var in asig:
            var = var.strip()
            if len(var)==0:
                break
            A.add(var)
    return A
        
        
##print(A)
    
def tripleSAT(instance, cnf, assign):
    with open(instance, "r") as clausulas:
        for c in clausulas:
            c = c.strip()
            if len(c) == 0:
                break
            literals = c.split()
            sat = []
            for l in literals:
                neg = '!' in l
                var = l[neg:]
                ok = ((var in assign and not neg) or (not var in assign and neg))
##                print(var, neg, ok)
                sat.append(ok)
                if ok:
                    if cnf:
                        break
                else:
                    if not cnf:
                        break
##            print(sat)
            if cnf and not (True in sat):
                return False
            if not cnf and not (False in sat):
                return True
    return cnf 


##Experimento para comprobar consistencia
#inst=open("InstanciasTripleSAT/nombres_instancias.txt",'w')
#asig=open("InstanciasTripleSAT/nombres_asignaciones.txt",'w')
#for lin in range (10,1000,20):
#    for var in range (lin//2,2*lin,20):
#        for cnf in [True,False]:
#            for valor in [True,False]:
#                instance(lin,var,str(lin)+'-'+str(var),cnf,valor)
#                if cnf: 
#                    if tripleSAT("InstanciasTripleSAT/instancia_tripleSAT("+str(cnf)+","+str(valor)+")"+str(lin)+'-'+str(var)+".txt",cnf,asignacion("InstanciasTripleSAT/asignacion_tripleSAT("+str(cnf)+","+str(valor)+")"+str(lin)+'-'+str(var)+".txt"))==valor:
#                        print("InstanciasTripleSAT/instancia_tripleSAT("+str(cnf)+","+str(valor)+")"+str(lin)+'-'+str(var)+".txt",file=inst)
#                        print("InstanciasTripleSAT/asignacion_tripleSAT("+str(cnf)+","+str(valor)+")"+str(lin)+'-'+str(var)+".txt",file=asig)
#                    else:
#                        print("Error en instancia CNF: "+str(lin)+'-'+str(var))
#                else: 
#                    if tripleSAT("InstanciasTripleSAT/instancia_tripleSAT("+str(cnf)+","+str(valor)+")"+str(lin)+'-'+str(var)+".txt",cnf,asignacion("InstanciasTripleSAT/asignacion_tripleSAT("+str(cnf)+","+str(valor)+")"+str(lin)+'-'+str(var)+".txt"))==valor:
#                        print("InstanciasTripleSAT/instancia_tripleSAT("+str(cnf)+","+str(valor)+")"+str(lin)+'-'+str(var)+".txt",file=inst)
#                        print("InstanciasTripleSAT/asignacion_tripleSAT("+str(cnf)+","+str(valor)+")"+str(lin)+'-'+str(var)+".txt",file=asig)
#                    else:
#                        print("Error en instancia DNF: "+str(lin)+'-'+str(var))
#inst.close()
#asig.close()
                        


"""Genetico"""


clausulas=[]
class solucion:
    def __init__(self,x):
        self.x=x
        self.f=fitness(x)
    def __repr__(self):
        return repr(self.x)+repr(self.f)
    def __lt__(self,other):
        return self.f<other.f
    def __le__(self,other):
        return self.f<=other.f

def fitness(assign):
    'calcula fitness para cnf'
    global clausulas
    numC=0
    for literals in clausulas:
        sat = []
        for l in literals:
            neg = '!' in l
            var = int(l[neg+1:])
            ok = ((assign[var-1] and not neg) or (not assign[var-1] and neg))
            sat.append(ok)
            if ok:             
                numC+=1
                break
    return 100*numC/len(clausulas)

def cruza(P1,P2):
    c=randint(0,len(P1.x)-1)
    return [solucion(P1.x[:c]+P2.x[c:]),solucion(P2.x[:c]+P1.x[c:])]

def GA3SAT(instancia,n,N=100,G=20,Pc=0.5,Pm=0.1):
    #indicadores de calidad
    start =time()
    out=open("mejor_soln.txt",'w')

    #leer instancia
    global clausulas
    with open(instancia, "r") as instance:
        clausulas=[]
        for c in instance:
            c = c.strip()
            if len(c) == 0:
                break
            clausulas.append(c.split())
        
        #generar población inicial
        P=[solucion([choice([0,1]) for i in range(n)]) for x in range(N)]
        
        P.sort()
        print(0,P[-1].f,P[-1].x,file=out )
        
        
        #repetir por G generaciones
        for g in range(G):
            H=[]
            #Generar progenie
            while len(H)<N:
                #Elegir individuos para cruzarse torneo binario            
                [P1,P2]=[max(sample(P,2)), max(sample(P,2))]
                
                #Aplicar cruzamiento
                if random()<Pc:
                    Hijos=cruza(P1,P2)
                    
                    #aplicar mutacion
                    for h in Hijos:
                        if random()<Pm:
                            x= randint(0,n-1)                       
                            h.x[x]=(h.x[x]+1)%2
                        # se encontró el óptimo
                        if h.f==100:
                            print(g+1,h.f,h.x,file=out )
                            elapsed = (time() - start)
                            print("elapsed time: %fs" %elapsed)
                            return h
                    H+=Hijos
                
            #reemplazar padres por hijos
            P=H
            P.sort()
            print(g+1,P[-1].f,P[-1].x,file=out )
    elapsed = (time() - start)
    print("elapsed time: %fs" %elapsed)
    return P
                    
                
                
            
        
       

                
                
        
            
            
            
