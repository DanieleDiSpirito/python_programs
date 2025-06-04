from Crypto.Util.number import isPrime
import matplotlib.pyplot as plt
import numpy as np

LEN = 100_000

nprimi = [0] * LEN

for i in range(1, LEN):
    nprimi[i] = int(nprimi[i-1] + isPrime(i))

nprimi = np.array(nprimi)

def ψ(x):
    return nprimi[x]

def f(x):
    return [a*.1 for a in x]

# PIANO CARTESIANO

# variabili
ax = plt.gca()
ax.set_xlim(0, LEN)
ax.set_ylim(0, LEN // 5)
x = range(LEN) # np.linspace(0, 10000, 10_000)

# parametri: inizio grafico, fine grafico, punti tracciati
# == 'x = np.arange(0, TWOPI, 0.001)' # 0.001 = 1000^(-1)
y1 = ψ(x)
y2 = f(x) # x/10

# IMMAGINE
plt.plot(x, y1, marker="", color='blue', label=r'$y=ψ(x)$')
plt.plot(x, y2, marker="", color='red', label=r'$y=x/10$')
# marker può essere 'x', 'o', '.' o '' ed indica
# il simbolo per indicare i punti tracciati
plt.title("Numero di primi")
plt.grid()  # fa apparire la griglia
plt.xlabel("numeri")
plt.ylabel("primi")
plt.legend(loc=0)  # 0 = in basso a sinistra, 1 in alto a destra etc.
plt.savefig('piano_cartesiano.pdf')
plt.show()
