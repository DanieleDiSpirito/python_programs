import gpu

MAX    = 1000  # maximum Mandelbrot iterations
N      = 4096  # width and height of image
pixels = [0 for _ in range(N * N)]

def scale(x, a, b):
    return a + (x/N)*(b - a)

@gpu.kernel
def mandelbrot(pixels):
    idx = (gpu.block.x * gpu.block.dim.x) + gpu.thread.x
    i, j = divmod(idx, N)
    c = complex(scale(j, -2.00, 0.47), scale(i, -1.12, 1.12))
    z = 0j
    iteration = 0

    while abs(z) <= 2 and iteration < MAX:
        z = z**2 + c
        iteration += 1

    pixels[idx] = int(255 * iteration/MAX)

mandelbrot(pixels, grid=(N*N)//1024, block=1024)