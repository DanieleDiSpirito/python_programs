import numpy as np
import cv2
import os

delimiter = "#####"
def messageToBinary(message):
    t = type(message)
    if t == str:
        return ''.join([format(ord(i), "08b") for i in message])
        '''
        08b -> b = binary -> 8 bits, 1 byte
        ord(i) transform i in the Unicode code point
        '''
    elif t == bytes or t == np.ndarray:
        return [format(i, "08b") for i in message]
    elif t == int or t == np.uint8:
        return format(message, "08b")
    else:
        raise TypeError("Input type not supported") 

def showData(image):
    binary_data = ""
    for values in image:
        for pixel in values: #pixel are 250'000 (500x500)
            r, g, b = messageToBinary(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    #split by 8-bits
    all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
    #convert from bits to char
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == delimiter: #check if we have reached the delimiter
            break
    return decoded_data[:-5] #remove the delimiter

os.chdir('C:\\Users\\danie\\Desktop\\python_programs\\steganography')
image = cv2.imread(input("Enter the name of steganographed image you want to decode (with extension): "))
text = showData(image)
print(text)