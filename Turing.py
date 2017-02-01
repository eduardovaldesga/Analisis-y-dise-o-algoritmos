# inicio: 'i'
# espacio en blanco: 'b'
#izquierda: 'l'
#derecha: 'r'
#sin direccion: 'n'
 
TM=dict()
TM['s','i']=('s','i','r')
TM['s','0']=('s','0','r')
TM['s','1']=('s','1','r')
TM['s','b']=('t','b','l')
TM['t','1']=('t','0','l')
TM['t','0']=('alto','1','n')
TM['t','i']=('u','i','r')
TM['u','0']=('w','1','r')
TM['w','0']=('w','0','r')
TM['w','1']=('w','1','r')
TM['w','b']=('alto','0','r')

#"i010010b"

def Turing(cinta):
	estado='s'
	pos=0
	while("True"):
		c=list(TM[estado,cinta[pos]])
		
		estado=c[0]
		
		#cinta[pos]=c[1]
		new=list(cinta)
		new[pos]=c[1]
		cinta=''.join(new)
		

		

		if c[2]=='l':
			pos=pos-1
		elif c[2]=='r':
			pos=pos+1
		#print(pos)

		if(pos==len(cinta)):
			cinta+='b'

		if estado in ['alto', 'si', 'no']: 
			break

	return cinta

print(Turing("i1111b"))
		




