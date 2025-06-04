from PIL import Image
import colorsys
import math
import os
from tqdm import tqdm
from Crypto.Util.number import isPrime

#frame parameters
width = 1000
height = 1000

img = Image.new('1', (width, height), color = 'black')
pixels = img.load()

BLACK = 0
WHITE = 1

for row in tqdm(range(height)):
    for col in range(width):
        if isPrime(col + row*width):
            pixels[col,row] = WHITE

img.save(f'primes{width*height}.png')
os.system(f'fim primes{width*height}.png')