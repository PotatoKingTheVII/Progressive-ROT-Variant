from tkinter import *
from tkinter import scrolledtext

####Define functions####
def cipherTXT_changed(*args):   #Update txt box after change
    UImlt = int(mltvar.get())
    UIshift = int(shiftvar.get())
    inputCipher = (ciphertextTXT.get("1.0",'end-1c'))
    plaintextTXT.delete(1.0, 'end-1c')
    plaintextTXT.insert('end-1c', CipherDec(inputCipher,UImlt,UIshift))


def plainTXT_changed(*args):    #Update txt box after change
    UImlt = int(mltvar.get())
    UIshift = int(shiftvar.get())
    inputCipher = (plaintextTXT.get("1.0",'end-1c'))
    ciphertextTXT.delete(1.0, 'end-1c')
    ciphertextTXT.insert('end-1c', CipherEnc(inputCipher,UImlt,UIshift))


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

            ROT = mlt*alph.find(cipher[i-1].lower())+shift  #Normal operation, 2 successive alph chars
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

            
        plain = ciphertext[0] + plain[1:len(plain)]   #Fix first letter          
        return plain

    except:
        return "Error"



####GUI Code####
####Initalise window####
window = Tk()
window.title("Digit Cipher")
window.geometry('725x300')

####Labels####
plaintextLBL = Label(window, text="Ciphertext")
plaintextLBL.grid(column=1, row=0)

ciphertextLBL = Label(window, text="Plaintext")
ciphertextLBL.grid(column=0, row=0)

mlttextLBL = Label(window, text="Multiple")
mlttextLBL.grid(column=0, row=2)

shifttextLBL = Label(window, text="Shift")
shifttextLBL.grid(column=1, row=2)
  
####Textboxes####
ciphertextTXT = scrolledtext.ScrolledText(window,width=40,height=10)
ciphertextTXT.grid(column=1,row=1, padx=10)
ciphertextTXT.bind('<KeyRelease>', cipherTXT_changed)

plaintextTXT = scrolledtext.ScrolledText(window,width=40,height=10)
plaintextTXT.grid(column=0,row=1, padx=10)
plaintextTXT.bind('<KeyRelease>', plainTXT_changed)


####Dropdown menus####
mltvar = StringVar(window)
shiftvar = StringVar(window)
shiftvar.set("1") # default value
mltvar.set("1") # default value

mlt = OptionMenu(window, mltvar,    "0","1","2","3","4","5","6","7","8","9","10",
                                    "11","12","13","14","15","16","17","18","19","20",
                                    "21","22","23","24","25","26")

shift = OptionMenu(window, shiftvar,  "0","1","2","3","4","5","6","7","8","9","10",
                                      "11","12","13","14","15","16","17","18","19","20",
                                      "21","22","23","24","25","26")
mlt.grid(column=0,row=3, padx=10)
shift.grid(column=1,row=3, padx=10)


####Buttons####
plainRfsh = Button(window, text="Refresh", command=cipherTXT_changed)
plainRfsh.grid(column=0,row=4, padx=10)

cipherRfsh = Button(window, text="Refresh", command=plainTXT_changed)
cipherRfsh.grid(column=1,row=4, padx=10)

####Main loop####
window.mainloop()
