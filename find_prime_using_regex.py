from re import match
from danidisp import clock
from sympy.ntheory import nextprime, isprime

IS_PRIME = r"^.?$|^(..+?)\1+$"

# how it works

'''
^ start of string
| or
. some character (wildcard)
? zero or one
+ one or more
\1 backreference
$ end of string

.? is '' or '1', 0 or 1 are not prime.

^(..+?)\1+$ is way difficult to understand so i asked Chat-GPT to help me.
That's the answer:

These regular expressions are used to match strings with repeated patterns, but they differ in how they match patterns and what types of repetition they allow.

Let's break down each regex:

### 1. `^(..+?)\1+$`

- Pattern: `(..+?)\1+`
  - `(..+?)` matches **any two characters or more**, as few times as possible (the `+?` is a lazy quantifier).
  - `\1+` matches one or more repetitions of the same pattern captured by `(..+?)`.
- **Full expression:** `^(..+?)\1+$`
  - This pattern checks if the entire string is made up of repeated segments of **any two characters or more**.
  
Example Matches:
- `"abab"`: Matches because `"ab"` is repeated twice.
- `"abcabcabc"`: Matches because `"abc"` is repeated three times.
- `"abcdabcdabcd"`: Matches because `"abcd"` is repeated three times.

Non-Matches:
- `"aa"`: Does not match because it requires at least two different characters in each repeated group.
- `"abcde"`: Does not match because it cannot be divided into repeating groups.

### 2. `^(..+?)+$`

- Pattern: `(..+?)+`
  - `(..+?)` again matches **any two characters or more** with as few repetitions as possible, but this time, it is followed by a `+` applied to the group.
- Full expression: `^(..+?)+$`
  - This pattern matches if the entire string is composed of multiple occurrences of patterns of **two or more characters**, but does not enforce that these patterns are identical in each repetition.
  
Example Matches:
- `"abcde"`: Matches because it allows different patterns to appear (`ab` and `cde` are allowed).
- `"abcdefgh"`: Matches because there's no requirement that `"abcd"` must repeat identically.
  
Non-Matches:
- This regex is less strict, so it will match many more cases, including those with non-repeating patterns.

### 3. `^(..)\1+$`

- Pattern: `(..)\1+`
  - `(..)` matches exactly **two characters**.
  - `\1+` requires these **exact two characters to repeat one or more times**.
- Full expression: `^(..)\1+$`
  - This pattern checks if the entire string is made of **exactly two characters** repeating throughout.
  
Example Matches:
- `"abab"`: Matches because `"ab"` repeats.
- `"cdcdcd"`: Matches because `"cd"` repeats three times.

Non-Matches:
- `"abcabc"`: Does not match because it's more than two characters in the repeating sequence.
- `"aabb"`: Does not match because `"a"` and `"b"` do not repeat in pairs.

### Summary

| Regex               | Description                                           | Example Match  | Example Non-Match |
|---------------------|-------------------------------------------------------|----------------|--------------------|
| `^(..+?)\1+$`       | Repeats a pattern of 2+ characters | `"abab"`         | `"abcde"`      |
| `^(..+?)+$`         | Allows different patterns of 2+ characters each       | `"abcde"`      | (matches nearly everything)|
| `^(..)\1+$`         | Matches exact 2-character repeating pattern           | `"abab"`       | `"abcabc"`        |



These regular expressions can be creatively used to identify if a string does **not** have a repeating pattern. This is a bit similar to checking if a number is **prime**: a prime number only has two divisors, 1 and itself, meaning it cannot be evenly divided into smaller repeated groups.

If you use these regexes with strings composed of repeated digits or characters, it can indicate whether a number of characters can form a repeating sequence (non-prime length) or not (prime length).

### Example

Let's take a character like `"a"` and repeat it a number of times, say 5 (`"aaaaa"`) or 6 (`"aaaaaa"`).

1. **Non-Prime Length (6)**:
   - A string of `"aaaaaa"` has a length of 6, which is non-prime.
   - Regexes like `^(..)\1+$` would match, because `aa` repeats 3 times.

2. **Prime Length (5)**:
   - A string of `"aaaaa"` has a prime length (5).
   - None of these regexes would match because there's no way to form a repeating substring for a prime length.

This means if the regex **does not match** for a string of repeated characters (like `"aaaaa"`), then the length is likely **prime**.

### In Practice

To test for prime numbers using these regex patterns, you can:
1. Choose a single character (e.g., `"a"`) and repeat it \( n \) times.
2. Apply the regex pattern.
3. If none of the regex patterns match, it suggests \( n \) is prime (no repeating structure).
4. If one of the regex patterns matches, \( n \) is non-prime (has a repeating structure).

**Example:**
```python
# For n = 7 (prime), "aaaaaaa" does not match.
# For n = 8 (non-prime), "aaaaaaaa" does match, e.g., `^(..)\1+$`.
```

This approach works because prime lengths cannot be decomposed into smaller repeated patterns.

'''

@clock
def is_prime_regex(n: int) -> bool:
    return not match(IS_PRIME, '1'*n)

@clock
def isprime_clock(n: int) -> bool:
    return isprime(n)

@clock
def nextprime_clock(n: int) -> bool:
    return nextprime(n)


# TESTING

time_nextprime = 0
time_is_prime = 0
time_is_prime_regex = 0

prime = 2
while prime <= 10**4:
    res = isprime_clock(prime)
    assert res[0]
    time_is_prime += res[1]
    res = is_prime_regex(prime)
    assert res[0]
    time_is_prime_regex += res[1]
    res = nextprime_clock(prime)
    prime = res[0]
    time_nextprime += res[1]

print(f'isprime()\t\t{time_is_prime:.8f}s')
print(f'is_prime_regex()\t{time_is_prime_regex:.8f}s')
print(f'nextprime()\t\t{time_nextprime:.8f}s')

# isprime()               0.00268237s
# is_prime_regex()        16.77599059s TOO EXPENSIVE
# nextprime()             0.01362603s
