from PIL import Image, ImageDraw, ImageFont
import math

def is_prime(n):
    """Controlla se un numero è primo."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    sqrt_n = int(math.sqrt(n)) + 1
    for i in range(3, sqrt_n, 2):
        if n % i == 0:
            return False
    return True

def genera_spirale_ulam(dimensione, pixel_per_punto=20):
    """Genera un'immagine della spirale di Ulam con numeri scritti."""
    larghezza = altezza = dimensione * pixel_per_punto
    img = Image.new("RGB", (larghezza, altezza), "black")
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", pixel_per_punto // 2)
    except:
        font = ImageFont.load_default()

    x = y = dimensione // 2
    dx, dy = 1, 0
    lunghezza_passi = 1
    numero = 1

    while x < dimensione and y < dimensione:
        for _ in range(2):
            for _ in range(lunghezza_passi):
                if 0 <= x < dimensione and 0 <= y < dimensione:
                    px = x * pixel_per_punto
                    py = y * pixel_per_punto
                    if is_prime(numero):
                        draw.rectangle(
                            [(px, py), (px + pixel_per_punto - 1, py + pixel_per_punto - 1)],
                            fill="white"
                        )
                        text_color = "black"
                    else:
                        draw.rectangle(
                            [(px, py), (px + pixel_per_punto - 1, py + pixel_per_punto - 1)],
                            fill="gray"
                        )
                        text_color = "white"

                    # Centra il testo nel quadrato
                    testo = str(numero)
                    text_bbox = draw.textbbox((0, 0), testo, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                    tx = px + (pixel_per_punto - text_width) // 2
                    ty = py + (pixel_per_punto - text_height) // 2
                    draw.text((tx, ty), testo, fill=text_color, font=font)

                numero += 1
                x += dx
                y += dy
            dx, dy = dy, -dx  # Ruota a sinistra
        lunghezza_passi += 1

    return img

# Esempio d'uso
dimensione = 31  # attenzione: troppe celle rendono l'immagine pesante con testi
img = genera_spirale_ulam(dimensione, pixel_per_punto=30)
img.save("spirale_ulam_con_numeri.png")
img.show()
