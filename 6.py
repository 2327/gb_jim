#!/usr/bin/env python3
"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
 Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""

l = ['сетевое программирование', 'сокет', 'декоратор']

with open('f.txt','w') as f_txt:
    for i in l:
        f_txt.write(i + "\n")
f_txt.close()


with open('f.txt', 'r', encoding='utf-8') as f_txt:
    for i in f_txt:
        print(i, end='')
f_txt.close()