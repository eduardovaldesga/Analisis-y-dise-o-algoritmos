# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 12:09:23 2017

@author: Eduardo,Juan,Missael
"""
from random import random
import os 
from heapq import heappush,heappop,heapify
from bintrees import AVLTree
def genera_segmentos():
    num_seg=input("Introduce numero de segmentos: ")
    try:
        num_seg=int(num_seg)
    except:
        print("Error al recibir numero de segmentos, por default se generan 100")
        num_seg=100
            
    textFile=input("Introduce nombre de archivo: ")
    try:
        output=open(textFile,'w')
    except:
        print("Error al abrir el archivo %s. Por default se abrira segmentos_default.txt" %textFile)
        output=open("segmentos_default.txt",'w')
        
    for i in range(num_seg):
        print("%f\t%f\t%f\t%f"%(random(),random(),random(),random()) ,file=output)
    output.close()


def grafica_segmentos(textFile):
    datos=open(textFile,'r')
    tex=open("grafica.tex",'w')
    print("\\documentclass{standalone}\n\\usepackage{tikz}\n\\usetikzlibrary{shapes,snakes}\n\\begin{document}\n\\begin{tikzpicture}[node distance = 0.5cm,inner sep = 2pt,scale=5] \n",file=tex)
    print("\draw[step=0.1,lightgray] (0,0) grid (1,1);\n",file=tex)
    i=1
    for linea in datos:
        linea.strip()
        if len(linea) is 0:
            break
        p=linea.split()
        print("\\draw (%s,%s) node (p1%d) {};\n\\draw (%s,%s) node (p2%d) {};\n " %(p[0],p[1],i,p[2],p[3],i)  ,file=tex     )
        print("\\draw\n(p1%d) edge (p2%d);\n" %(i,i),file=tex)
        i+=1
    print("\\end{tikzpicture}\n\\end{document}",file=tex)
    
    datos.close()
    tex.close()
    os.system("pdflatex grafica")
    os.startfile("grafica.pdf")

def pendiente(s):
    ((x1,y1),(x2,y2))=s
    try:
        return (y2-y1)/(x2-x1)
    except:
        return None
    
def interseccion(s1,s2):
    m1=pendiente(s1)
    m2=pendiente(s2)
    div=m1-m2
    (x,y)=s1[0]
    (xp,yp)=s2[0]
    try:
        x_calc=(y-m1*x-yp+m2*xp)/div
        return (x_calc,m1*(x_calc)+y-m1*x)
    except:
        return (None,None)
        
        
    
    
#genera_segmentos()
#grafica_segmentos("segmentos.txt")

def barrer(textFile):
    pos = 0
    inst=open(textFile,'r')
    salida=open("salida.txt",'w')
    S=[]
    for linea in inst:
        linea.strip()
        if len(linea) is 0:
            break
        p=linea.split()
        S.append(((float(p[0]),float(p[1])),(float(p[2]),float(p[3]))))
        
    M=[]
    for i in range(len(S)):
        ((x1,y1),(x2,y2))=S[i]
        if x1>x2:
            x1,y1,x2,y2=x2,y2,x1,y1
        heappush(M,((x1,y1),'C',i,None))
        heappush(M,((x2,y2),'F',i,None))
#    print(len(M))
    B=AVLTree()
    D={}
    while len(M)>0:
        ((x,y),tipo,i,j)=heappop(M)
        if x < pos:
            print("descartando", x,y,tipo)
            continue
        pos = x
        print(x,y,tipo,len(M))
        if tipo == 'C':
            B[y]=i
            D[i]=y
            v_izq=None
            try:
                v_izq=B.prev_key(y)
            except:
                pass
            if v_izq is not None:
                l = B[v_izq]
                (xp,yp)=interseccion(S[i],S[l])
                if xp is not None and xp>x:
                    heappush(M,((xp,yp),'I',l,i))
            print("izq: ",v_izq) 
            v_der=None
            try:
                v_der=B.succ_key(y)
            except:
                pass
            if v_der is not None:
                r = B[v_der]
                (xp,yp)=interseccion(S[i],S[r])
                if xp is not None and xp>x:
                    heappush(M,((xp,yp),'I',i,r))
            print("der: ",v_der)       
        elif tipo == 'F':
            l=None
            r=None
            try:
                v_izq=B.prev_key(y)
                l = B[v_izq]
                v_der=B.succ_key(y)
                r=B[v_der]
                
            except:
                pass
            print("izq: ",v_izq)
            print("der: ",v_der) 
            B.discard(y)
            del D[i]
            if l is not None and r is not None:
                (xp,yp)=interseccion(S[l],S[r])
                if xp is not None and xp>x:
                    heappush(M,((xp,yp),'I',l,r))
        elif tipo== 'I':
            if i not in D or j not in D:
                continue
            assert B[D[i]] == i
            assert B[D[j]] == j
#            print("antes",B,D,i,j)
            B[D[i]],B[D[j]]=B[D[j]],B[D[i]]
            D[i],D[j]=D[j],D[i]
#            print("despues",B,D,i,j)
            v_izq=None
            try:
                v_izq=B.prev_key(y)
            except:
                pass
            if v_izq is not None:
                l = B[v_izq]
                (xp,yp)=interseccion(S[j],S[l])
                if xp is not None and xp>x:
                    heappush(M,((xp,yp),'I',j,l))
            v_der=None
            try:
                v_der=B.succ_key(y)
            except:
                pass
            if v_der is not None:
                r = B[v_der]
                (xp,yp)=interseccion(S[i],S[r])
                if xp is not None and xp>x:
                    heappush(M,((xp,yp),'I',i,r))
            print("izq: ",v_izq)
            print("der: ",v_der)
            print("%f %f"%(x,y),file=salida)
        else:
            print(tipo)
        
    salida.close()
            
            
            
barrer("segmentos.txt")
                
        
                    
                
                
        
            
        
        
    
        
            
    
    
    

         