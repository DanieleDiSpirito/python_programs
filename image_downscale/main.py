from PIL import Image
import os
from sys import argv

file_name = "original/img.png"

try:
    if len(argv) >= 2:
        file_name = argv[1]
except:
    pass

img = Image.open(f"{file_name}")

DOWNSCALE_FACTOR = 4 # 2**DF (downscale factor)
try:
    if len(argv) == 3:
        DOWNSCALE_FACTOR = int(argv[2])
except:
    pass

downscale = 2 ** DOWNSCALE_FACTOR

WIDTH, HEIGHT = img.size

new_img = Image.new("RGB", (WIDTH // downscale, HEIGHT // downscale))

pixels = new_img.load()

for i in range(0, WIDTH - downscale + 2, downscale):
    for j in range(0, HEIGHT - downscale + 2, downscale):
        sumR = sumG = sumB = 0
        for k in range(downscale):
            sumR += img.getpixel((i + k, j))[0]
            sumR += img.getpixel((i, j + k))[0]
            sumG += img.getpixel((i + k, j))[1]
            sumG += img.getpixel((i, j + k))[1]
            sumB += img.getpixel((i + k, j))[2]
            sumB += img.getpixel((i, j + k))[2]
        pixels[i // downscale, j // downscale] = (sumR // (downscale * 2), sumG // (downscale * 2), sumB // (downscale * 2))

file_name = file_name.split("/")[-1]

new_img.save(f"downscaled/{file_name}")
os.system(f"fim downscaled/{file_name}")
