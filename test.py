import nltk
import re
import math

train = open("test-tweets-given.txt", encoding="utf8")
train = [l for l in (line.strip() for line in train) if l]
test = open("training-tweets.txt", encoding="utf8")
p = open("test.txt", encoding="utf8")

V = 0
n = 1
s = 0.5
wrong = 0
good = 0

def Unigram(V, n, s):
    
    global wrong, good
    F = {}
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    # 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
    total = 0
    for lines in test:
        S = lines.split("\t")
        if S[2] not in F:
            F[S[2]] = {}
        for elem in list(S[3]):
            if elem.lower() in alphabet:
                total+=1
                
    for key in F.keys(): 
        for i in range(len(alphabet)):
            F[key][alphabet[i]] = 1
            
    test.seek(0)
    for lines in test:
        S = lines.split("\t")
        for elem in list(S[3]):
            if elem.lower() in alphabet:
                F[S[2]][elem.lower()] += 1
                
    for key in F.keys(): 
        for i in range(len(alphabet)):
            F[key][alphabet[i]] /= total
            
    for lines in train:
        S = lines.split("\t")
        result = {}
    
        for key in F.keys():
            result[key] = 0
        for elem in list(S[3]):
            if elem.lower() in alphabet:
                for key in F.keys():
                    result[key] += math.log10(F[key][elem.lower()])
                    
        if S[2] == max(result, key=result.get):
            good += 1
        else:
            wrong += 1
    
    print( (good/(wrong+good)) * 100)
    return F
    
def Bigram(V, n, s):
    
    global wrong, good
    F = {}
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    # 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
    count = {}

        
    for lines in test:
        S = lines.split("\t")
        if S[2] not in F:
            F[S[2]] = {}
            count[S[2]] = {}
        
    for key in F.keys(): 
        for i in range(len(alphabet)):
            F[key][alphabet[i]] = {}
        for key2 in F[key].keys():
            for i in range(len(alphabet)):
                F[key][key2][alphabet[i]] = 0
                
    for key in F.keys():        
        for i in range(len(alphabet)):
            count[key][alphabet[i]] = 0
    
    test.seek(0)
    
    for lines in test:
        S = lines.split("\t")
        for elem in list(S[3]):
            if elem.lower() in alphabet:
                count[S[2]][elem.lower()] += 1
                
    test.seek(0)
    for lines in test:
        S = lines.split("\t")
        L = re.split('[^a-zA-Z]', S[3])
        NL = list(filter(None,L))
        
        for elem in NL:
            bigrams = list(nltk.bigrams(elem))
            for l in bigrams:
                F[S[2]][l[0].lower()][l[1].lower()] += 1
                
    for key in F.keys(): 
        for key2 in F[key].keys():
            for i in range(len(alphabet)):
                F[key][key2][alphabet[i]] /= (count[key][key2]+1)
                
    for lines in train:
        S = lines.split("\t")
        L = re.split('[^a-zA-Z]', S[3])
        NL = list(filter(None,L))
        result = {}
        
        for key in F.keys():
            result[key] = 0
            
        for elem in NL:
            bigrams = list(nltk.bigrams(elem))
            for l in bigrams:
                for key in F.keys():
                    result[key] += math.log10(F[key][l[0].lower()][l[1].lower()])
                    
        if S[2] == max(result, key=result.get):
            good += 1
        else:
            wrong += 1
            
    print( (good/(wrong+good)) * 100)
    return F
    
def Trigram(V, n, s):
    
    global wrong, good
    
    F = {}
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    # 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
    count = {}
    
    
    for lines in test:
        S = lines.split("\t")
        if S[2] not in F:
            F[S[2]] = {}
            count[S[2]] = {}
            
    for key in F.keys(): 
        for i in range(len(alphabet)):
            F[key][alphabet[i]] = {}
        for key2 in F[key].keys():
            for i in range(len(alphabet)):
                F[key][key2][alphabet[i]] = {}
            for key3 in F[key][key2].keys():
                for i in range(len(alphabet)):
                    F[key][key2][key3][alphabet[i]] = 1
                    
    for key in F.keys():        
        for i in range(len(alphabet)):
            count[key][alphabet[i]] = 1   
            
    test.seek(0)
    
    for lines in test:
        S = lines.split("\t")
        for elem in list(S[3]):
            if elem.lower() in alphabet:
                count[S[2]][elem.lower()] += 1
        
        
    test.seek(0)
    
    for lines in test:
        S = lines.split("\t")
        L = re.split('[^a-zA-Z]', S[3])
        NL = list(filter(None,L))
        
        for elem in NL:
            trigrams = list(nltk.trigrams(elem))
            for l in trigrams:
                F[S[2]][l[0].lower()][l[1].lower()][l[2].lower()] += 1
                # if S[2] == "en":
                #     word = l[0].lower()+l[1].lower()+l[2].lower()
                #     if word == "ing":
                #         F[S[2]][l[0].lower()][l[1].lower()][l[2].lower()] += 1
                
    for key in F.keys(): 
        for key2 in F[key].keys():
            for key3 in F[key][key2].keys():
                for i in range(len(alphabet)):
                    num = F[key][key2][key3][alphabet[i]] + 1
                    num /= (count[key][key2]+len(alphabet))
                    
    for lines in train:
        S = lines.split("\t")
        L = re.split('[^a-zA-Z]', S[3])
        NL = list(filter(None,L))
        result = {}
    
        for key in F.keys():
            result[key] = 0
        
        for elem in NL:
            trigrams = list(nltk.trigrams(elem))
            for l in trigrams:
                for key in F.keys():
                    result[key] += math.log10( F[key][l[0].lower()][l[1].lower()][l[2].lower()] ) 
                    
        if S[2] == max(result, key=result.get):
            print("%s  %s  %.3g  %s  %s" % (S[0],max(result, key=result.get),result[max(result, key=result.get)],S[2], "good" ))
            good += 1
        else:
            print("%s  %s  %.3g  %s  %s" % (S[0],max(result, key=result.get),result[max(result, key=result.get)],S[2], "wrong" ))
            wrong += 1        
                
    # print(F["en"]["i"]["n"]["g"])
    # print(F["es"]["i"]["n"]["g"])
    # print(F["eu"]["i"]["n"]["g"])
    
    print( (good/(wrong+good)) * 100)
    
    return F




# NBC = Unigram(V,n,s)

# NBC = Bigram(V,n,s)

NBC = Trigram(V,n,s)



