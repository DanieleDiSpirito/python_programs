with open('words.italian.txt') as file_:
    with open('five_char_words.italian.txt', 'w') as fivechar:
        while True:
            p = file_.readline()
            if len(p) == 6: # '\n'
                print(p, end = '', file = fivechar)
                print(p)
            elif p == None:
                break
        fivechar.close()
    file_.close()
print('Finito')
