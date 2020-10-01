# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПРОЦЕССНОМ стиле
#
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
import csv
import os
import threading
from multiprocessing import Process, Pipe


class Trades(Process):

    def __init__(self, file, dirpath, connection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.common_price = []
        self.file = file
        self.dirpath = dirpath
        self.path = os.path.join(dirpath, file)
        self.common_volatility = []
        self.null_volatility = []
        self.connection = connection

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
            self.connection.send([self.common_volatility, self.null_volatility])
            self.connection.close()
            self.common_price.clear()


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
    pipes = []

    for dirpath, dirnames, filenames in os.walk('trades'):
        for file in filenames:
            parent_connection, child_connection = Pipe()
            new_obj.append(Trades(file, dirpath, connection=child_connection))
            pipes.append(parent_connection)
    for object in new_obj:
        object.start()
    for object in new_obj:
        object.join()
    for connection in pipes:
        list_of_good, list_of_bad = connection.recv()
        good_volatility += list_of_good
        zero_volatility += list_of_bad

    sorting_and_printing(good_volatility, zero_volatility)


if __name__ == '__main__':
    main()
#зачёт!