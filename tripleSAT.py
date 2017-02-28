

#leer asiganciones
A = set()
with open("asignacion_tripleSAT2.txt",'r') as asig:
    for var in asig:
        var = var.strip()
        if len(var)==0:
            break
        A.add(var)
        
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

print('CNF:',tripleSAT("instancia_tripleSAT2.txt", True, A))
print('DNF:',tripleSAT("instancia_tripleSAT2.txt", False, A))
    

                
                
        
            
            
            
