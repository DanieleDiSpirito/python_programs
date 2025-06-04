from itertools import combinations

def to_binary(n, bits):
    return format(n, f'0{bits}b')

def count_ones(term):
    return term.count('1')

def combine_terms(term1, term2):
    diff = 0
    result = ''
    for a, b in zip(term1, term2):
        if a != b:
            diff += 1
            result += '-'
        else:
            result += a
    return result if diff == 1 else None

def get_prime_implicants(minterms, num_vars):
    groups = {}
    for m in minterms:
        b = to_binary(m, num_vars)
        groups.setdefault(count_ones(b), []).append((b, [m]))

    prime_implicants = set()
    while groups:
        next_groups = {}
        used = set()
        all_pairs = []
        keys = sorted(groups.keys())
        for i in range(len(keys)-1):
            g1 = groups[keys[i]]
            g2 = groups[keys[i+1]]
            for t1, list1 in g1:
                for t2, list2 in g2:
                    combined = combine_terms(t1, t2)
                    if combined:
                        used.add(t1)
                        used.add(t2)
                        next_groups.setdefault(count_ones(combined.replace('-', '')), []).append((combined, list1 + list2))
                        all_pairs.append(combined)

        for group in groups.values():
            for term, origin in group:
                if term not in used:
                    prime_implicants.add((term, tuple(sorted(set(origin)))))
        groups = {}
        for key, value in next_groups.items():
            unique = {}
            for v, orig in value:
                if v not in unique:
                    unique[v] = orig
            groups[key] = [(k, unique[k]) for k in unique]
    return prime_implicants

def print_implicants(implicants):
    for term, minterms in sorted(implicants):
        print(f"{term} --> {minterms}")

def show_expression(implicants, num_vars):
    exp = ""
    for term, minterms in implicants:
        for i, x in enumerate(term):
            if x == '1':
                exp += chr(ord('A') + i)
            elif x == '0':
                exp += chr(ord('A') + i) + "'"
        exp += " + "
    exp = exp[:-3]  # remove last " + "
    print(exp)
    return exp

minterms = [1, 3, 5, 7, 9, 12, 13, 19, 29]
num_vars = 5

prime_implicants = get_prime_implicants(minterms, num_vars)
print("Prime implicants founds:")
print_implicants(prime_implicants)
show_expression(prime_implicants, num_vars)
