#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import glob
import csv
from datetime import datetime, timedelta, timezone
import pytz
import os
import shutil


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


def phone_cleaner(phone: [str, int], prefix: str = '7'):
    """Функция очистки номера сотового телефона от лишних символов, с заменой первой цифры.

    :param phone: строка с номером телефона
    :param prefix: начальный символ номера телефона '8' или '7' (по умолчанию) на выходе
    """

    clear_phone = ''
    for digit in str(phone):
        if digit in '1,2,3,4,5,6,7,8,9,0':
            clear_phone += digit

    if len(clear_phone) != 11:
        return f'Не верный номер телефона {clear_phone}, должно быть 11 цифр!'

    if clear_phone[0] != prefix:
        return f'{prefix}{clear_phone[1:]}'
    else:
        return clear_phone


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


def get_mails(string: str = None, single: bool = False, regex: bool = False, file_name: str = None,
              file_type: str = 'txt'):
    """Получение e-mail из текстовой строки или файла(-ов)

    :param string: строка текста
    :param single: поиск первого значения
    :param regex: True используется re для поиска в строке, False find
    :param file_name: путь к файлу, для поиска в файле
    :param file_type: расширение файлов для поиска, при использовании glob, по умолчанию `txt`
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
        for file in glob.glob(f'*.{file_type}'):
            with open(file, 'r') as f:
                file_text = f.read()
                mails.append(re.findall(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+', file_text))

        result = []
        for x in mails:
            result.extend(x if isinstance(x, list) else [x])
        return list(set(result))


def list_filter(filter_list: (list, tuple), filter_value: int = None, filter_type: int = 1, even: int = None):
    """Фильтрация списка чисел по занчению

    :param filter_list: список значений
    :param filter_value: значение для сравнения
    :param filter_type: тип сравнения: 1 ==, 2 !=, 3 >, 4 >=, 5 <, 6 <=
    :param even: отбор чисел из списка: 1 четные, 2 не четные
    """

    if even == 1:
        return list(int(y) for y in filter(lambda x: ('' if x is None else int(x) % 2 == 0), filter_list))
    elif even == 2:
        return list(int(y) for y in filter(lambda x: ('' if x is None else int(x) % 2 != 0), filter_list))

    new_list = []
    for el in filter_list:

        if el is not None:
            el = int(el)
        else:
            continue

        if filter_type == 1:
            if el == filter_value:
                new_list.append(el)

        elif filter_type == 2:
            if el != filter_value:
                new_list.append(el)

        elif filter_type == 3:
            if el > filter_value:
                new_list.append(el)

        elif filter_type == 4:
            if el >= filter_value:
                new_list.append(el)

        elif filter_type == 5:
            if el < filter_value:
                new_list.append(el)

        elif filter_type == 6:
            if el <= filter_value:
                new_list.append(el)

    return new_list


def unique(file_name: str):
    """Функция удаляющая дубли в переданном файле"""

    unique_lines = set(open(file_name, 'r', encoding='utf-8').readlines())
    open(file_name, 'w', encoding='utf-8').writelines(set(unique_lines))


def divide_list(list_string: list[str, int], size: int) -> list:
    """Функция возвращающая массив чисел разделенный на равные части"""

    divide = lambda lst, sz: [lst[i:i + sz] for i in range(0, len(lst), sz)]
    number_list = [int(numeric_string) for numeric_string in list_string if int(numeric_string)]
    return divide(number_list, size)


def list_flatten(old_list):
    """Перевести вложенный список в плоский"""

    new_list = []
    for x in old_list:
        if isinstance(x, (list, tuple)):
            new_list += list_flatten(x)
        else:
            new_list.append(x)
    return new_list


def current_datetime(days: int = 0, hours: int = 0, minutes: int = 0, tz: str = "Europe/Moscow") -> datetime:
    """Возвращает текущий datetime с учётом времненной зоны, по умолчанию tz Мск."""

    delta = timedelta(days=days, hours=hours, minutes=minutes)
    tz = pytz.timezone(tz)
    now = datetime.now(tz) + delta
    return now


def current_datetime_formatted(str_type: int = None, minus_days: int = 0, plus_days: int = 0) -> str:
    """Возвращает текущую дату строкой"""

    if str_type == 1:
        ft = '%d.%m.%Y'
    elif str_type == 2:
        ft = '%Y-%m-%d %H:%M:%S'
    elif str_type == 3:
        ft = '%d_%m_%Y'
    elif str_type == 4:
        ft = '%H:%M:%S'
    elif str_type == 5:
        ft = '%H'
    elif str_type == 6:
        ft = '%Y-%m-%d'
    elif str_type == 7:
        ft = '%d_%m_%y'
    else:
        ft = '%d.%m.%Y %H:%M:%S'

    return (current_datetime() - timedelta(days=minus_days) + timedelta(days=plus_days)).strftime(ft)


def string_to_datetime(date_string: str, date_format: str = '%Y-%m-%d %H:%M:%S'):
    """Перевод строкового пердставления даты в datetime"""
    return datetime.strptime(date_string, date_format)


def seconds_to_time(seconds: int, time_format: str = 'short') -> str:
    """Конвертация секунд в `ЧЧ:ММ:СС`

    :param seconds: количество секунд
    :param time_format: 'long' "%02d:%02d:%02d", 'short' "%02d:%02d"
    """

    seconds = seconds % (24 * 3600)
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    if time_format == 'long':
        return "%02d:%02d:%02d" % (hours, minutes, seconds)
    if time_format == 'short':
        return "%02d:%02d" % (hours, minutes)


def create_directory(file_path: str) -> None:
    """Функция для создания директории file_path: str путь до файла"""
    if not os.path.exists(file_path):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)
        try:
            os.makedirs(path)
            print(f'INFO: создали > {file_path}')
        except Exception as e:
            print(f'WARNING: {path} > {e}')


def clear_directory(file_path: str) -> None:
    """Функция удаляющая данные из папки file_path: str путь до файла"""
    if os.path.exists(file_path):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_path)
        try:
            shutil.rmtree(path)
            print(f'INFO: очистили > {path}')
        except FileExistsError as e:
            print(f'WARNING: {path} > {e}')


if __name__ == '__main__':
    print(list_filter(['1', 2, 3, 4, 5, 6, 7, '8', 9, 0, None], even=2))
    print(sum(list_filter(['1', 2, 3, 4, 5, 6, 7, '8', 9, 0, None], even=2)))
