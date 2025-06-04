import cv2
import numpy as np
import types
import os
#from google.colab.patches import cv2_imshow #utilizzabile solo su Google Colaboraty

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
    
def hideData(image, secret_message):
    #calculate the maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("Maximum bytes to encode:", n_bytes)
    
    #check if number of bytes to encode is less than maximum image bytes
    if len(secret_message) > n_bytes:
        raise ValueError("Error encounted insufficient bytes, need bigger image or smaller secret message")
    
    secret_message += delimiter

    data_index = 0
    #convert input data to binary format using messageToBinary() function
    binary_secret_msg = messageToBinary(secret_message)
    
    data_len = len(binary_secret_msg)
    for values in image:
        for pixel in values:
            #convert RGB values into binary format
            r, g, b = messageToBinary(pixel)

            #modify the LSB only if there is data to store
            if data_index < data_len: #red
                pixel[0] = int(r[:-1] + binary_secret_msg[data_index], 2) #2 is the base
                data_index += 1
            if data_index < data_len: #green
                pixel[1] = int(g[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
            if data_index < data_len: #blue
                pixel[2] = int(b[:-1] + binary_secret_msg[data_index], 2)
                data_index += 1
            if data_index >= data_len: break

    return image

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

def encode_text():
    image_name = input("Enter image (with extension): ")
    if image_name == '': image_name = 'pikachu.png'
    image = cv2.imread(image_name) #read the input image using OpenCV-Python

    #print("The shape of the image is: ", image.shape)
    data = input("Enter data to be encoded: ")
    if len(data) == 0:
        raise ValueError('Data is empty')

#   os.chdir('C:\\Users\\Asus\\Desktop\\python_programs\\steganography\\encoded_image')
    filename = input("Enter the name of new encoded image (with extension): ")
    encoded_image = hideData(image, data)
    cv2.imwrite(filename, encoded_image)
    print("Opening the image... ")
    resized_image = cv2.resize(image, (500, 500))
    cv2.imshow('Encoded image: ' + image_name, resized_image)

def decode_text():
    #read the image with hidden image
    #os.chdir('C:\\Users\\danie\\Desktop\\python_programs\\steganography')
    image_name = input("Enter the name of steganographed image you want to decode (with extension): ")
    image = cv2.imread(image_name)

    resized_image = cv2.resize(image, (500, 500))
    #print("Opening the image... ")
    cv2.imshow('Decoded image: ' + image_name, resized_image)

    text = showData(image)
    return text

def main():
    a = input("\n".join([
        "Image steganografy",
        "1. Encode the data",
        "2. Decode the data",
        ""]) + "Your input is: ")
    userinput = int(a)

    if userinput == 1:
        print("\nEncoding...")
        encode_text()
    elif userinput == 2:
        print("\nDecoding...")
        print("Decoded message is \'", decode_text(), "\'", sep = '')
        '''
        with open("a.txt", 'w') as file_:
            print(decode_text().encode("utf-8"), file=file_)
        '''
    else:
        raise Exception("Enter correct input")

#os.chdir('C:\\Users\\danie\\Desktop\\python_programs\\steganography')
delimiter = "#####"

try:
    main()
except BaseException as error: #BaseException refers to all the exceptions/errors
    print(error)

#main()







                
