import math
import numpy as np

#Define functions
def fitness(text):  #Calc with chi squared monogram comparison
    text = (text.replace(" ","")).lower()
    alph = "abcdefghijklmnopqrstuvwxyz"
    ocrr = np.zeros(26)
    freq = []
    for i in text:  #Add each letter to a total count array
        if(alph.find(i)!=-1):
            ocrr[alph.find(i)]+=1
    total = sum(ocrr)
    for i in range(0,len(ocrr)):    #Calculate letter percentages
        freq.append(ocrr[int(i)]/total)

    #####CHI SQUARED#####
    expected = [8.13,1.49,2.71,4.32,12.02,2.30,2.03,5.92,7.31,0.10,0.69
                ,3.98,2.61,6.95,7.68,1.82,0.11,6.02,6.28,9.10,2.88,1.11
                ,2.09,0.17,2.11,0.07]
    expected = np.divide(expected,100)
    chi = 0
    for i in range(0,len(freq)):
        chitop = (freq[i]-expected[i])**2
        chibottom= expected[i]
        
        chi+=(chitop/chibottom)
    return chi


    
def CipherEnc(plaintext, mlt, shift):
    if(plaintext==""):  #Avoid passing blank strings
        return ""
    plain = plaintext.lower()   #Only use lower, add case back throughout
    alph = "abcdefghijklmnopqrstuvwxyz"
    cipher = plaintext[0]
    ROT = 0

    try:
        for i in range(1,len(plain)):  #Iterate over plaintext
            if(alph.find(plain[i])==-1):   #Current char is non alph char, skip cipher and add to plain
                cipher+=plain[i]
                
                if(alph.find(plain[i-1])==-1): #Both current and prev char is non alph, don't change ROT
                    continue
                
                ROT = mlt*(alph.find(cipher[i-1].lower()))+shift   #Prev char is valid, set ROT to it
                continue
                
            if(alph.find(plain[i-1])==-1):#Non alph char was before, don't update ROT before cipher
                currentLetterPos = alph.find(plain[i])
                if(plaintext[i].isupper()):
                    cipher+=alph[(currentLetterPos+ROT)%26].upper() #Return case
                else:
                    cipher+=alph[(currentLetterPos+ROT)%26]
                    
                
                continue

            ROT = mlt*alph.find(cipher[i-1].lower())+shift  #Normal operation, 2 successive
            currentLetterPos = alph.find(plain[i])
            if(plaintext[i].isupper()):
                cipher+=(alph[(currentLetterPos+ROT)%26]).upper()   #Return case
            else:
                cipher+=alph[(currentLetterPos+ROT)%26]

        return cipher
    except:
        return "Error"

def CipherDec(ciphertext, mlt, shift):

    try:
        cipher = ciphertext.lower() #Again only deal with lower and add upper back later
        alph = "abcdefghijklmnopqrstuvwxyz"
        plain = ""
        ROT = 0


        for i in range(0,len(cipher)):  #Iterate over cipher
            if(alph.find(cipher[i])==-1):   #Current char is non alph char, skip cipher and add to plain
                plain+=cipher[i]
                
                if(alph.find(cipher[i-1])==-1): #Both current and prev char is non alph, don't change ROT
                    continue
                
                ROT = mlt*alph.find(cipher[i-1])+shift    #Prev char is valid, set ROT to it
                continue
                
            if(alph.find(cipher[i-1])==-1):#Non alph char was before, don't update ROT before cipher
                currentLetterPos = alph.find(cipher[i])
                if(ciphertext[i].isupper()):
                    plain+=alph[(currentLetterPos-ROT)%26].upper()  #Add case back
                else:
                    plain+=alph[(currentLetterPos-ROT)%26]
                continue

            ROT = mlt*alph.find(cipher[i-1])+shift  #Normal operation, 2 successive alph chars
            currentLetterPos = alph.find(cipher[i])

            if(ciphertext[i].isupper()):
                plain+=alph[(currentLetterPos-ROT)%26].upper()  #Add case back
            else:
                plain+=alph[(currentLetterPos-ROT)%26]

            
        plain = ciphertext[0] + plain[1:len(plain)] #Fix first letter   
        return plain

    except:
        return "Error"


####Brute force each possibility####
A=26    #Values to check through A is mlt, B is shift
B=26
a = 1   #Current a and b values
b = 1
combolist = []
cipher = input("Enter cipher: ")


for i in range(A*B):    #Work out each possibility and add to list
    plain = CipherDec(cipher, a, b)
    combolist.append(plain)
    a+=1
    b=(math.floor(a/26))+1
orderedlist = []

for i in range(A*B):    #Add chi values to each possibility
    orderedlist.append([combolist[i],fitness(combolist[i].lower())])
    
orderedlist = sorted(orderedlist, key=lambda chi: chi[1])   #Sort list for lowest chi score

####Output results to shell and file####
print("\nTop 10:")
for i in range(0,10):
    print(orderedlist[i][0])

with open("Output.csv", "w") as fout:
    for i in range(0,len(orderedlist)):
        fout.write(orderedlist[i][0]+","+str(orderedlist[i][1])+"\n")
