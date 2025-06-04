from PIL import Image
import os

img = Image.open("img.png")

DOWNSCALE_FACTOR = 4 # 2**DF (downscale factor)

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

new_img.save("new_img.png")
os.system("fim new_img.png")
