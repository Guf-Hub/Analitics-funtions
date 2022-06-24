#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import glob
import csv


def write_csv(file_name: str, row):
    with open(file_name, 'a', newline='\n', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL, delimiter=',')
        writer.writerow([row])


def get_and_save_phones(file_name: str, save_as: str = 'phones.csv'):
    """Получить сотовые телефоны из файла и записать в файл phones.csv"""

    with open(file_name, 'r') as file:
        text = file.read()
        text = text.replace('+7', '7')
        text = re.sub(r'[().+-]', '', text).replace(' ', '').split(sep=None)

    text = ' '.join(text)
    phones = re.findall(r"[\+\(]?[7-9][0-9.\-\(\)]{8,}[0-9]", text)

    temp = []
    for phone in phones:
        if len(phone) == 11:
            if phone[0] == '7':
                temp.append(phone)
            elif phone[0] == '8':
                temp.append(f'7{phone[1:]}')
        elif len(phone) == 10:
            temp.append(f'7{phone}')

    for item in list(set(temp)):
        write_csv(file_name=save_as, row=item)


def get_phones(string: str = None, file_name: str = None) -> list:
    """Получение телефонов из текстовой строки или файла(-ов)

    :param string: строка текста
    :param file_name: путь к файлу, для поиска в файле
    """

    phones = []
    if string:
        return list(set(re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', string)))
    elif file_name:
        with open(file_name, 'r') as f:
            file_text = f.read()
            return list(set(re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', file_text)))
    else:
        for file in glob.glob('*.txt'):
            with open(file, 'r') as f:
                file_text = f.read()
                phones.append(re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', file_text))

        result = []
        for x in phones:
            result.extend(x if isinstance(x, list) else [x])
        return list(set(result))


def get_mails(string: str = None, single: bool = False, regex: bool = False, file_name: str = None):
    """Получение e-mail из текстовой строки или файла(-ов)

    :param string: строка текста
    :param single: поиск первого значения
    :param regex: True используется re для поиска в строке, False find
    :param file_name: путь к файлу, для поиска в файле
    """

    mails = []

    if string and not regex and single:
        list_rom_string = string.replace('\n', ' ').split(' ')
        for item in list_rom_string:
            if item.find('@') > 0:
                return item
    elif string and not regex and not single:
        list_rom_string = string.replace('\n', ' ').split(' ')
        for item in list_rom_string:
            if item.find('@') > 0:
                mails.append(item)
        return list(set(mails))
    elif regex:
        return list(set(re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', string)))

    elif file_name:
        with open(file_name, 'r') as f:
            file_text = f.read()
            return list(set(re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', file_text)))
    else:
        for file in glob.glob('*.txt'):
            with open(file, 'r') as f:
                file_text = f.read()
                mails.append(re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', file_text))

        result = []
        for x in mails:
            result.extend(x if isinstance(x, list) else [x])
        return list(set(result))


if __name__ == '__main__':
    get_and_save_phones('examples/resume2.txt')
