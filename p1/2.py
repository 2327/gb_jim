#!/usr/bin/env python3
"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
"""

CLASS = 'class'
FUNCTION = 'function'
METHOD = 'method'

CLASS_B = bytes(CLASS, 'utf-8')
FUNCTION_B = bytes(FUNCTION, 'utf-8')
METHOD_B = bytes(METHOD, 'utf-8')


print("Слово {} в байтовом представлении: ".format(CLASS))
for i in CLASS_B:
    print(i, end=' ')

print("\nСлово {} в байтовом представлении: ".format(FUNCTION))
for i in FUNCTION_B:
    print(i, end=' ')

print("\nСлово {} в байтовом представлении: ".format(METHOD))
for i in METHOD_B:
    print(i, end=' ')