from genera_instancia_tripleSAT import genera_instancia_tripleSAT as instance

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


#Experimento para comprobar consistencia
inst=open("InstanciasTripleSAT/nombres_instancias.txt",'w')
asig=open("InstanciasTripleSAT/nombres_asignaciones.txt",'w')
for lin in range (10,1000,20):
    for var in range (lin//2,2*lin,20):
        for cnf in [True,False]:
            for valor in [True,False]:
                instance(lin,var,str(lin)+'-'+str(var),cnf,valor)
                if cnf: 
                    if tripleSAT("InstanciasTripleSAT/instancia_tripleSAT("+str(cnf)+","+str(valor)+")"+str(lin)+'-'+str(var)+".txt",cnf,asignacion("InstanciasTripleSAT/asignacion_tripleSAT("+str(cnf)+","+str(valor)+")"+str(lin)+'-'+str(var)+".txt"))==valor:
                        print("InstanciasTripleSAT/instancia_tripleSAT("+str(cnf)+","+str(valor)+")"+str(lin)+'-'+str(var)+".txt",file=inst)
                        print("InstanciasTripleSAT/asignacion_tripleSAT("+str(cnf)+","+str(valor)+")"+str(lin)+'-'+str(var)+".txt",file=asig)
                    else:
                        print("Error en instancia CNF: "+str(lin)+'-'+str(var))
                else: 
                    if tripleSAT("InstanciasTripleSAT/instancia_tripleSAT("+str(cnf)+","+str(valor)+")"+str(lin)+'-'+str(var)+".txt",cnf,asignacion("InstanciasTripleSAT/asignacion_tripleSAT("+str(cnf)+","+str(valor)+")"+str(lin)+'-'+str(var)+".txt"))==valor:
                        print("InstanciasTripleSAT/instancia_tripleSAT("+str(cnf)+","+str(valor)+")"+str(lin)+'-'+str(var)+".txt",file=inst)
                        print("InstanciasTripleSAT/asignacion_tripleSAT("+str(cnf)+","+str(valor)+")"+str(lin)+'-'+str(var)+".txt",file=asig)
                    else:
                        print("Error en instancia DNF: "+str(lin)+'-'+str(var))
inst.close()
asig.close()
                        

#print('CNF:',tripleSAT("instancia_tripleSAT2.txt", True, A))
#print('DNF:',tripleSAT("instancia_tripleSAT2.txt", False, A))
    

                
                
        
            
            
            
