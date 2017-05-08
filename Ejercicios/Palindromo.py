def palindromo_recursivo(word):    
    'determina si word es un palindromo'
    if len(word)<2:        
        return "True"
        

    elif not word[0]==word[-1]:
        return "False"
    
    else:
            word=word[1:-1]
            return palindromo_recursivo(word)
        
        
def palindromo_iterativo(word):
    if len(word)<2:
        print("Imprime true")
        return "True"
    else:
        
        for i in range(0,len(word)/2):            

            if word[i]!=word[-i-1]:
                return "False"
        return "True" #se llegó a la mitad de la palabra

import time
start = time.time()
print(palindromo_iterativo("saippnakanppias"))
elapsed = (time.time() - start)
print(elapsed)

#print(is_pal("saippnakanppiat"))
