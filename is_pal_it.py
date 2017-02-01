
def is_pal(word):
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
print(is_pal("saippnakanppias"))
elapsed = (time.time() - start)
print(elapsed)

#print(is_pal("saippnakanppiat"))
