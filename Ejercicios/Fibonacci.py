def fibonacci_iterativo(n):
    'dtermina el n-ésimo término de la sucesión de Fibonacci'
    if n<2:
        return n
    
    else:
        n0=0
        n1=1
        
        for i in range(n-1):
            f=n0+n1
            n0=n1
            n1=f
        return f

       
        
def fibonacci_recursivo(n):
        if n<2:
                return n
	
        else:
                return fibonacci_recursivo(n-2)+fibonacci_recursivo(n-1)

import time
start = time.time()
print(fibonacci_recursivo(30))
elapsed = (time.time() - start)
print(elapsed)

  
    
