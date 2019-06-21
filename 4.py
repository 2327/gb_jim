#!/usr/bin/env python3
"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое
и выполнить обратное преобразование (используя методы encode и decode).
"""

l = ['разработка', 'администрирование', 'protocol']
for i in l:
    tmp = str(i).encode('utf-8')
    i = tmp.decode()
    print(i)
