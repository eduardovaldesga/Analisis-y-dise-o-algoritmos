def fibo(n):
        if n<2:
                return n
	
        else:
                return fibo(n-2)+fibo(n-1)

import time
start = time.time()
print(fibo(30))
elapsed = (time.time() - start)
print(elapsed)

