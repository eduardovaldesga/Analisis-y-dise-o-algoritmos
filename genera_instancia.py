from random import randint, choice, random
PORSubE=0.09 #'porcentaje de subestaciones respecto al total de nodos'
SIZE=100 #'tamaño de la cuadricula donde se encuentran los nodos y subE'
DLOW=20 #'cota inferior de demanda'
DUP=100 #'cota superior de demanda'
DENARCOS=0.1  #densidad de arcos
LLOW=40 #'cota inferior de longitud'
LUP=200 #'cota superior de longitud'
CLOW=40 #'cota inferior de costo'
CUP=200 #'cota superior de costo'

def genera_instancia(n):
    global PORSubE
    global SIZE
    global DLOW
    global DUP
    global DENARCOS

    datos=open("instancia.txt","w")

    ID=0

    #generar subestaciones
##    for i in range(1,int(PORSubE*n)+1):
##        #s: ID  X   Y   puesto/posible(1/0)
##        X=randint(0,SIZE)
##        Y=randint(0,SIZE)
##        puesto=randint(0,1)
##        print("s:\t"+str(ID)+"\t"+str(X)+"\t"+str(Y)+"\t"+str(puesto),file=datos)
##        ID+=1
        

    #generar nodos
    for i in range(1,n+1):
##    for i in range(int(PORSubE*n)+1,n+1):
        #n: ID  X   Y   puesto/posible(1/0) demanda
        X=randint(0,SIZE)
        Y=randint(0,SIZE)
        puesto=randint(0,1)
        demanda=randint(DLOW,DUP)
        print("n:\t"+str(ID)+"\t"+str(X)+"\t"+str(Y)+"\t"+str(puesto) +"\t"+str(demanda),file=datos)
        ID+=1

    #generar arcos
    for i in range(1,int(DENARCOS*n**2)):
        inicio=randint(0,n-1)
        final=randint(0,n-1)
        longitud=randint(LLOW,LUP)
        costo=randint(CLOW,CUP)
        print("a:\t%d\t%d\t%d\t%d" %(inicio,final,longitud,costo),file=datos)
        


genera_instancia(30)
