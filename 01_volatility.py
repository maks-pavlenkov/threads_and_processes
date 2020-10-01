# -*- coding: utf-8 -*-


# Описание предметной области:
#
# При торгах на бирже совершаются сделки - один купил, второй продал.
# Покупают и продают ценные бумаги (акции, облигации, фьючерсы, етс). Ценные бумаги - это по сути долговые расписки.
# Ценные бумаги выпускаются партиями, от десятка до несколько миллионов штук.
# Каждая такая партия (выпуск) имеет свой торговый код на бирже - тикер - https://goo.gl/MJQ5Lq
# Все бумаги из этой партии (выпуска) одинаковы в цене, поэтому говорят о цене одной бумаги.
# У разных выпусков бумаг - разные цены, которые могут отличаться в сотни и тысячи раз.
# Каждая биржевая сделка характеризуется:
#   тикер ценнной бумаги
#   время сделки
#   цена сделки
#   обьем сделки (сколько ценных бумаг было куплено)
#
# В ходе торгов цены сделок могут со временем расти и понижаться. Величина изменения цен называтея волатильностью.
# Например, если бумага №1 торговалась с ценами 11, 11, 12, 11, 12, 11, 11, 11 - то она мало волатильна.
# А если у бумаги №2 цены сделок были: 20, 15, 23, 56, 100, 50, 3, 10 - то такая бумага имеет большую волатильность.
# Волатильность можно считать разными способами, мы будем считать сильно упрощенным способом -
# отклонение в процентах от полусуммы крайних значений цены за торговую сессию:
#   полусумма = (максимальная цена + минимальная цена) / 2
#   волатильность = ((максимальная цена - минимальная цена) / полусумма) * 100%
# Например для бумаги №1:
#   half_sum = (12 + 11) / 2 = 11.5
#   volatility = ((12 - 11) / half_sum) * 100 = 8.7%
# Для бумаги №2:
#   half_sum = (100 + 3) / 2 = 51.5
#   volatility = ((100 - 3) / half_sum) * 100 = 188.34%
#
# В реальности волатильность рассчитывается так: https://goo.gl/VJNmmY
#
# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью.
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#
# Подготовка исходных данных
# 1. Скачать файл https://drive.google.com/file/d/1l5sia-9c-t91iIPiGyBc1s9mQ8RgTNqb/view?usp=sharing
#       (обратите внимание на значок скачивания в правом верхнем углу,
#       см https://drive.google.com/file/d/1M6mW1jI2RdZhdSCEmlbFi5eoAXOR3u6G/view?usp=sharing)
# 2. Раззиповать средствами операционной системы содержимое архива
#       в папку python_base/lesson_012/trades
# 3. В каждом файле в папке trades содержится данные по сделакам по одному тикеру, разделенные запятыми.
#   Первая строка - название колонок:
#       SECID - тикер
#       TRADETIME - время сделки
#       PRICE - цена сделки
#       QUANTITY - количество бумаг в этой сделке
#   Все последующие строки в файле - данные о сделках
#
# Подсказка: нужно последовательно открывать каждый файл, вычитывать данные, высчитывать волатильность и запоминать.
# Вывод на консоль можно сделать только после обработки всех файлов.
#
# Для плавного перехода к мультипоточности, код оформить в обьектном стиле, используя следующий каркас
#
# class <Название класса>:
#
#     def __init__(self, <параметры>):
#         <сохранение параметров>
#
#     def run(self):
#         <обработка данных>
import csv
import os


class Trades:

    def __init__(self, file, dirpath):
        self.common_price = []
        self.file = file
        self.dirpath = dirpath
        self.path = os.path.join(dirpath, file)
        self.common_volatility = []
        self.null_volatility = []

    def run(self):
        with open(file=self.path, mode='r') as file_1:
            reader = csv.reader(file_1)
            for row in reader:
                if row[3].isalpha():
                    continue
                self.common_price.append(float(row[2]))
            max_price = max(self.common_price)
            min_price = min(self.common_price)
            half_sum = (max_price + min_price) / 2
            volatility = ((max_price - min_price) / half_sum) * 100
            if volatility != 0:
                self.common_volatility.append([self.file, round(volatility, 2)])
            else:
                self.null_volatility.append(self.file)
            self.common_price.clear()
            return self.common_volatility, self.null_volatility


def sorting_and_printing(common_volatility, null_volatility):
    sorted_volatility = sorted(common_volatility, key=lambda vol: vol[1], reverse=True)
    for i in range(len(sorted_volatility)):
        new_char = sorted_volatility[i][0].replace('.csv', '')
        sorted_volatility[i][0] = new_char
    for k in range(len(null_volatility)):
        new_null = null_volatility[k].replace('.csv', '')
        null_volatility[k] = new_null
    max_volatility = sorted_volatility[:3]
    min_volatility = sorted_volatility[-3:]
    print(
        f'Максимальная волатильность:\n{max_volatility[0][0]} - {max_volatility[0][1]} %\n'
        f'{max_volatility[1][0]} - {max_volatility[1][1]} %\n'
        f'{max_volatility[2][0]} - {max_volatility[2][1]} %\n')
    print(
        f'Минимальная волатильность:\n{min_volatility[0][0]} - {min_volatility[0][1]} %\n'
        f'{min_volatility[1][0]} - {min_volatility[1][1]} %\n'
        f'{min_volatility[2][0]} - {min_volatility[2][1]} %\n')
    print('Нулевая волатильность: ')
    for element in null_volatility:
        print(f'{element}', end=', ')


def main():
    new_obj = []
    good_volatility = []
    zero_volatility = []

    for dirpath, dirnames, filenames in os.walk('trades'):
        for file in filenames:
            new_obj.append(Trades(file, dirpath))
    for object in new_obj:
        data1, data2 = object.run()
        if data1:
            good_volatility.append(data1[0])
        if data2:
            zero_volatility.append(data2[0])
    sorting_and_printing(good_volatility, zero_volatility)


if __name__ == '__main__':
    main()
#зачёт!