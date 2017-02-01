def is_pal(word):
    
    
    if len(word)<2:        
        return "True"
        

    elif not word[0]==word[-1]:
        return "False"
    
    else:
            word=word[1:-1]
            return is_pal(word)

import time
start = time.time()
print(is_pal("saippnakanppias"))
elapsed = (time.time() - start)
print(elapsed)

#print(is_pal("saippnakanppiat"))
