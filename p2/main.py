#!/usr/bin/env python3
"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
 info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:

    Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание
    данных. В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
    «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения каждого параметра поместить в
    соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
    os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и
    поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта»,
    «Тип системы». Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для
    каждого файла);

    Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение данных
    через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;
    Проверить работу программы через вызов функции write_to_csv(). ###

2. Задание на закрепление знаний по модулю json.
     Есть файл orders в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными.
      Для этого:
    Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
    цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл
     orders.json. При записи данных указать величину отступа в 4 пробельных символа;
    Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.

3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле
    YAML-формата. Для этого:
    Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число,
    третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в
    кодировке ASCII (например, €);
    Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла
     с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
    Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.

"""

import re
import json

os_prod_list = []
os_name_list = []
os_code_list = []
os_type_list = []
main_data = []

def get_data():
    with open('main_data.txt', 'w', encoding='utf-8') as file_main:
        for i in main_data:
            file_main.write(i + ', ')

    for i in range(1, 4):
        name = 'info_' + str(i) + '.txt'
        with open(name, 'r', encoding='windows-1251') as file_info:
            for l in file_info:
                os_prod_find = re.findall(r'Изготовитель системы:.*',l)
                if os_prod_find:
                    os_prod_list.append(re.split(r'Изготовитель системы:\s+', os_prod_find[0])[1])

                os_name_find = re.findall(r'Название ОС:.*',l)
                if os_name_find:
                    os_name_list.append(re.split(r'Название ОС:\s+', os_name_find[0])[1])

                os_code_find = re.findall(r'Код продукта:.*',l)
                if os_code_find:
                    os_code_list.append(re.split(r'Код продукта:\s+', os_code_find[0])[1])

                os_type_find = re.findall(r'Тип системы:.*',l)
                if os_type_find:
                    os_type_list.append(re.split(r'Тип системы:\s+', os_type_find[0])[1])

    main_data.append(os_prod_list)
    main_data.append(os_name_list)
    main_data.append(os_code_list)
    main_data.append(os_type_list)

    with open('main_data.txt', 'w', encoding='utf-8') as file_main:
        j = 0
        file_main.write('Изготовитель системы, ' + 'Название ОС, ' + 'Код продукта, ' + 'Тип системы' + '\n')
        for j in range(len(main_data[i])):
            for l in range(len(main_data[i])):
                if l < len(main_data[i]) - 1:
                    file_main.write(main_data[l][j] + ', ')
                    l += l
                else:
                    file_main.write(main_data[l][j] + '\n')


#def write_to_csv():
#

def write_order_to_json(item,quantity,price,buyer,date):
    order = {}
    order["item"] = item
    order["quantity"] = quantity
    order["price"] = price
    order["buyer"] = buyer
    order["date"] = date

    order = json.dumps(order, indent = 4,  sort_keys = True)
    with open('order.json', 'w') as json_file:
        json.dump(order, json_file)

if __name__ == '__main__':
#    get_data()
    write_order_to_json(item=1,quantity=1,price=1,buyer=1,date=1)