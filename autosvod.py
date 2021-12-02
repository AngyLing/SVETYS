# coding: utf8

import pymorphy2
import time
import joblib
import pandas as pd

data = {}  # data[word][0] - forms, data[word][1] - vars
time0 = time.time()
morph = pymorphy2.MorphAnalyzer()

# Здесь должен быть массив слов для проверки - words (в качестве тестового можно использовать словник words
# Сводного этимологического словаря "СвЭтиС", для которого писалась функция)

words = joblib.load('../autosvod/variants/svet_vcb.pkl')
variants = joblib.load('../autosvod/data/shved_dict_vars.pkl')

words = joblib.load('svet_vocab-25.10.pkl')
variants = joblib.load('shved_dict_vars.pkl')



count = 0
# test_list = []

# TODO: предобработка (пословно)

for word in words:
    word = word.lower()
    # print(word)

    "ПОИСК ВАРИАНТОВ СЛОВ"
    if word in variants.keys() and variants[word].upper() in words:
        if variants[word] in data.keys():
            data[variants[word]][1].append(word)
        else:
            data[variants[word]] = [[], [word]]
        print(word, '-', variants[word])
        continue

    data[word] = [[], []]

    # if len(new_print) > 1:
    #     new_print = '&&&'.join(new_print)
    # else:
    #     new_print = new_print[0]
    # df.loc[k, 'pymorphy2'] = new_print

    """
    Для отладки системы используйте альтернативную выдачу: раздокументируйте строку после объявления переменной count и
    следующие строки (закомментировав предыдущую)
    """
    # result = is_unusual_dict_entry(word)
    # count += result[0]
    # if result[1] != '':
    #     test_list.append(result[1])
# print(test_list)


#
# time1 = time.time()
# print(f'\nПрограмма выполнена за {round(time1 - time0, 5)} сек.')


print(len(data))
print(len(words))
