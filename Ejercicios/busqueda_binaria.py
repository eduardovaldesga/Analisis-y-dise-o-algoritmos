from random import randint, choice
TOPE = 100
P_2it=0
P_2rec=0
Pnorm=0
def ran(n):
    x=[randint(0,TOPE)]    
    for i in range(1,n):       
        x.append(x[-1]+randint(1,TOPE))
    return x

##def binaria_it(x,arreglo):
##    global P_2it
##    
##    n=len(arreglo)/2
##    while n > 1 :
##        if arreglo[n]==x:
##            P_2it+=1
##            return True
##        elif arreglo[n]<x:
##            P_2it+=1
##            n+=n/2
##        else:
##            P_2it+=1
##            n- = n/2
                
    return False

def binaria_rec(x,arreglo):
    global P_2rec
    n=len(arreglo)/2
    if n==0:
        P_2rec+=1
        return False      
    if arreglo[n]==x:
        P_2rec+=1
        return True      
    if arreglo[n] < x:
        P_2rec+=1
        return binaria_rec(x, arreglo[n+1:])
    else:
        P_2rec+=1
        return binaria_rec(x, arreglo[:n])
                
def normal(x,arreglo):
    global Pnorm
    for i in range(1,len(arreglo)):
        Pnorm+=1
        if arreglo[i]==x:
            
            return True                       
    return False

datos = open("binaria.txt", "w")

for n in [10,20,40,80,160]:
    for TOPE in [100,200,300]:
        P_2it=0
        P_2rec=0
        Pnorm=0
        x=ran(n)
        
        #binaria rec TRUE9
        print >>datos, "bin_rec\t"+str(n)+"\t"+str(TOPE)+"\t"+str(binaria_rec(choice(x),x))+"\t"+str(P_2rec)
        P_2rec=0
        #binaria rec
        print >>datos,"bin_rec\t"+str(n)+"\t"+str(TOPE)+"\t"+str(binaria_rec(randint(1,TOPE),x))+"\t"+str(P_2rec)


##        #binaria rec TRUE9
##        print "bin_rec\t"+str(n)+"\t"+str(TOPE)+"\t"+str(binaria_rec(x[randint(0,len(x))],x))+"\t"+str(P_2rec)
##        P_2it=0
##
##        #binaria rec
##        print "bin_rec\t"+str(n)+"'n"+str(TOPE)+"\t"+str(binaria_rec(randint(1,TOPE),x)+"\t"+str(P_2rec)
##        
##
##
##
        #normc TRUE9
        print >>datos,"norm\t"+str(n)+"\t"+str(TOPE)+"\t"+str(normal(choice(x),x))+"\t"+str(Pnorm)
        Pnorm=0
        #norm
        print >>datos,"norm\t"+str(n)+"\t"+str(TOPE)+"\t"+str(normal(randint(1,TOPE),x))+"\t"+str(Pnorm)


        
datos.close()
        
        
        


