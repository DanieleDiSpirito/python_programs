from PIL import Image
import colorsys
import math
import os
from tqdm import tqdm
from Crypto.Util.number import isPrime

#frame parameters
width = 100
height = 100

img = Image.new('1', (width, height), color = 'black')
pixels = img.load()

BLACK = 0
WHITE = 1

for row in tqdm(range(height)):
    for col in range(width):
        n = col + row*width
        if isPrime(n) and (isPrime(n-2) or isPrime(n+2)):
            pixels[col,row] = WHITE

img.save(f'twin_primes{width*height}.png')
os.system(f'fim twin_primes{width*height}.png')