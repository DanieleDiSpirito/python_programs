import random
import tkinter


# VARIABLES
word = ''
random.seed()


# FUNCTIONS
def colori(attemp, word):
    global parola
    global yellow
    global parole
    for i in range(len(attemp)):
        if attemp[i] == word[i]:
            # green
            parola[i] = attemp[i]
            if attemp[i] not in yellow:
                yellow.append(attemp[i])
                yellow.sort()
        elif attemp[i] in word:
            # yellow
            if attemp[i] not in yellow:
                yellow.append(attemp[i])
                yellow.sort()
        else:
            # red
            if attemp[i] in parole:
                parole = "".join([
                    parole[:parole.index(attemp[i])],
                    parole[parole.index(attemp[i])+1:]
                ])


# MAIN
with open('five_char_words.italian.txt') as file_:
    for _ in range(random.randint(0, 2740)):
        file_.readline()
    word = file_.readline()[:-1]
    # print("Parola: " + word)
    file_.close()


parola = ['-', '-', '-', '-', '-']
yellow = []
parole = 'abcdefghilmnopqrstuvyz'
indovinata = False
totattemp = 6
nattemp = 0
while nattemp != totattemp:
    print(" ".join(list(parole)))
    attemp = input("Inserisci la parola: ").lower()
    if attemp == word:
        print("Parola indovinata")
        indovinata = True
        break
    else:
        if len(attemp) == 5:
            with open('five_char_words.italian.txt') as file_:
                esiste = False
                while not esiste:
                    rigo = file_.readline()[:-1]
                    if attemp == rigo:
                        esiste = True
                    elif rigo == '':
                        break
                if not esiste:
                    print("La parola non esiste")
                    nattemp -= 1
                else:
                    colori(attemp, word)
                file_.close()
        else:
            print("La parola non esiste")
            nattemp -= 1
    nattemp += 1
    print('Tentativi rimasti: ', 6 - nattemp)
    print(''.join(parola))
    print(' '.join(yellow))
    

if not indovinata:
    print("La parola era " + word)




