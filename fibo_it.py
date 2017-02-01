def fibo(n):
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

import time
start = time.time()
print(fibo(30))
elapsed = (time.time() - start)
print(elapsed)
        
        
    
    
