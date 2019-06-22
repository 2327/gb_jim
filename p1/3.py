#!/usr/bin/env python3
"""
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
"""

l = ['attribute', 'класс', 'функция', 'type']

for i in l:
    try:
        a = print(bytes(i, 'utf-8'))
    except:
        print('fail')