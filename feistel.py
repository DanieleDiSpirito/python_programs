import matplotlib.pyplot as plt
from faker import Faker

f = Faker()

a = b = c = d = e = 0

non_linear = lambda x: (((x << a) ^ (x >> b)) - (x & c) + (x & d) + e)

CYCLE = 2

N_NON_LINEAR_FUN = CYCLE ** 5


def fn_round(p: list[int]) -> None:
    l = p[0]
    r = p[1]
    new_l = r
    new_r = l ^ non_linear(r)
    p[0] = new_l
    p[1] = new_r

def fn_deround(p: list[int]) -> None:
    l = p[0]
    r = p[1]
    old_r = l
    old_l = r ^ non_linear(l)
    p[0] = old_l
    p[1] = old_r

avg = lambda x: sum(x) / len(x)

def main():
    coords = [[0 for i in range(0x100)] for _ in range(N_NON_LINEAR_FUN)]
    cov = [0 for _ in range(N_NON_LINEAR_FUN)]
    for a in range(CYCLE):
        for b in range(CYCLE):
            for c in range(CYCLE):
                for d in range(CYCLE):
                    for e in range(CYCLE):
                        for x in range(0x100):  # da 0x00 a 0xff
                            n = x
                            # rappresenta n come due byte: [LSB, MSB]
                            p = [n & 0xff, (n >> 8) & 0xff]
                            fn_round(p)
                            # ricombina i due byte in un intero 16-bit
                            new_n = p[0] | (p[1] << 8)
                            fn_deround(p)
                            new_new_n = p[0] | (p[1] << 8)
                            assert new_new_n == n
                            i = a * CYCLE**4 + b * CYCLE**3 + c * CYCLE**2 + d * CYCLE + e
                            coords[i][x] = new_n
        
                        avg_y = avg(coords[i])
                        # covariance of x,y
                        for x in range(0x100):
                            cov[i] += (x - 127.5) * (coords[i][x] - avg_y)
                        cov[i] /= 0x100
                        cov[i] = abs(cov[i])


    plt.figure(figsize=(10, 4))
    plt.title("Output di fn_round su input 0x00 - 0xFF")
    plt.xlabel("Input (x)")
    plt.ylabel("Output (y)")
    plt.grid(True)
    plt.tight_layout()
    idx_max = cov.index(max(cov))
    print("The most randomic function is:")
    print(f"fn_round_{idx_max} with variance {cov[idx_max]}")
    plt.plot(range(256), coords[idx_max], linestyle='-', color=f.color(), label=f"fn_round_{idx_max} ({cov[idx_max]})")
    plt.legend(loc='upper left', bbox_to_anchor=(0, 1), fontsize='small')
    
    idx_min = cov.index(min(cov))
    print("The most linear function is:")
    print(f"fn_round_{idx_min} with variance {cov[idx_min]}")
    plt.plot(range(256), coords[idx_min], linestyle='-', color=f.color(), label=f"fn_round_{idx_min} ({cov[idx_min]})")
    plt.legend(loc='upper left', bbox_to_anchor=(0, 1), fontsize='small')

    plt.show()    
    
if __name__ == "__main__":
    main()
