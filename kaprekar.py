# https://it.wikipedia.org/wiki/Costante_di_Kaprekar

def main():
    npc = [0 for _ in range(7)] #numeri per cicli
    for n in range(10**4):
        n = fill(n) #n become str
        if insertion(n):
            num = n
            for i in range(7):
                num = sorting(num, reverse = True) - sorting(num)
                if int(num) == 6174:
                    print('TEOREMA VERIFICATO PER ', int(n), f' AL PASSAGGIO N. {i+1}', sep = '')
                    npc[i] += 1
                    break
                if i == 6 and int(num) != 6174:
                    print('TEOREMA NON VERIFICATO PER ', int(n), sep = '')
                    pass
    for i in range(7):
        print(f"NUMERI CHE ARRIVANO ALLA COSTANTE DI KAPREKAR AL {i+1}° CICLO: ", npc[i])

#9 becomes 0009, 102 becomes 0102 ect.            
def fill(n):
    n = str(n)
    if len(n) != 4:
        if int(n) < 1000:
            if int(n) < 100:
                if int(n) < 10:
                    n = '000' + n
                else:
                    n = '00' + n
            else:
                n = '0' + n
    return n

#4 equal digits numbers are not allowed
def insertion(n):
    for i in range(len(n)-1):
        if n[i] != n[i+1]:
            return True
    return False


def sorting(n, reverse = False):
    n = list(fill(n))
    n.sort(reverse = reverse)
    return int(''.join(n))


if __name__ == '__main__':
    try:
        main()
    except BaseException as e:
        print("Error: " + str(e))
