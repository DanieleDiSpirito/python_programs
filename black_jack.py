import random as rand
import time
from time import sleep

#funzioni:

def asso(card):
    for position, item in enumerate(card):
        if item == 1:
            del(card[position])
            card.insert(position, 'asso')

def calcolo(card):
    tot = 0
    for position, item in enumerate(card):
        if item == 1 or item == 'asso':
            if tot <= 10: tot += 11
            else: tot += 1
        else:
            if tot + item <= 21: tot += item
            else:
                print("Hai superato il 21, hai perso")
                return None
    return tot

def domanda(domanda):
    while True:
        risposta = str(input(domanda))
        if risposta == 'si' or risposta == 'no': break
        else: print("Risposta non valida")
    return risposta

#codice principale:

print('Ciao, benvenuto in Black Jack! ♦♣♥♠')

n_partita = 1
soldi = 500

while True:

    print("------------ GAME " + str(n_partita) + " ------------")
    print("Hai", soldi, "$")
    
    #variabili:
    totcpu = 0
    finish = False
    carte = [rand.randint(1,10), rand.randint(1,10)]
    cpu = [rand.randint(1,10), rand.randint(1,10)]
    
    #utente:

    while True:
        puntata = int(input("Inserire la puntata: "))
        if 0 <= puntata <= soldi: break
        else: print("Puntata superiore ai soldi totali")
    
    while True:
        asso(carte)
        print("Le tue carte sono", carte)
        if calcolo(carte) != None: print("Il punteggio è", calcolo(carte))
        else:
            finish = True
            soldi -= puntata
            print("I soldi rimanenti sono", soldi, "$")
            break
        if domanda("Vuoi un'altra carta? ") == 'si':
            sleep(1)
            carte.append(rand.randint(1,10))
        else: break

    # cpu:

    while not finish:
        asso(cpu)
        print("Le carte della CPU sono", cpu)
        totcpu = 0
        for position, item in enumerate(cpu):
            if item == 'asso':
                if totcpu <= 10: totcpu += 11
                elif totcpu <= 20: totcpu += 1
                else:
                    print("Vittoria, la CPU ha superato 21")
                    finish = True
                    soldi += puntata
            else:
                if totcpu + item <= 21: totcpu += item
                else:
                    print("Vittoria, la CPU ha superato 21")
                    finish = True
                    soldi += puntata
        if finish: print("I soldi rimanenti sono", soldi, "$"); break
        else: print("Il punteggio della CPU è", totcpu)
        if totcpu < 17: sleep(2); cpu.append(rand.randint(1,10))
        elif totcpu >= calcolo(carte):
            print("Sconfitta, la CPU ha vinto")
            finish = True
            soldi -= puntata
            print("I soldi rimanenti sono", soldi, "$")
        else:
            print("Vittoria, hai vinto")
            finish = True
            soldi += puntata


    if domanda("Ricominciare a giocare? ") == 'no': break
    else: n_partita += 1; sleep(1)
    
input() # per far rimanere in piedi l'eseguibile