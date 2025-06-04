from PIL import Image
import colorsys
import math
import os
from tqdm import tqdm
from Crypto.Util.number import isPrime

#frame parameters
width = 1000
height = 1000

img = Image.new('RGB', (width, height), color = 'black')
pixels = img.load()

BLACK = (0x00, 0x00, 0x00)
WHITE = (0xff, 0xff, 0xff)
GREEN = (0x00, 0xff, 0x00)

for row in tqdm(range(height)):
    for col in range(width):
        if isPrime(col + row*width):
            pixels[col,row] = GREEN

img.save(f'primes{width*height}.png')
os.system(f'fim primes{width*height}.png')