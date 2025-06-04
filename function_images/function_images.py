from PIL import Image
import colorsys
import math
import os
from tqdm import tqdm
from Crypto.Util.number import isPrime

#frame parameters
width = 100
height = 100

img = Image.new('RGB', (width, height), color = 'white')
pixels = img.load()
e = math.e

for row in tqdm(range(height)):
    for col in range(width):
        pixels[col,row] = (
            abs(row**2+col**2) * 255 // 20000, # row % 0xff,
            0xff,
            0xff
        )

name = os.urandom(16).hex()

img.save(f'{name}.png')
os.system(f'fim {name}.png')