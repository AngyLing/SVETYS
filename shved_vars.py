# coding: utf8
import joblib
import pymorphy2
import pandas as pd


def end_difference(res, word0, word1):
    # print(word0, word1, len(word0), len(word1), len(word0) == len(word1), res, sep='\t')
    if ((res == 1 and word0[-1] == 'а' and word0[-2] != 'к' and word1[-1:-3:-1] == 'ак') or
            (res == 1 and word0[-1:-3:-1] == 'ак' and word1[-1:-4:-1] == 'акч') or
            (res > 2 or res == 0)) and not (res == 3 and
                                            (word0[-1:-3:-1] == 'це' and word1[-1:-4:-1] == 'аци' or
                                            word0[-1:-3:-1] == 'ян' and word1[-1:-4:-1] == 'ьне' or
                                            word0 == 'брильянт' and word1 == 'бриллиант')):
        # print(word0, word1, len(word0), len(word1), len(word0) == len(word1), res, sep='\t')
        return False

    return True


def difference(word0, word1):
    """Возвращает True / False в зависимости от количества букв, которыми отличаются слова word0 и word1."""

    res = 0
    len0, len1 = len(word0), len(word1)

    """Если длины равны, смотрим совпадение символов на одинаковых позициях"""
    if len0 == len1:
        for k in range(min(len0, len1)):
            if word0[k] != word1[k]:
                res += 1
        return end_difference(res, word0, word1)

    """Если длины слов разные, находим префикс и суффикс"""
    if len0 > len1:  # убеждаемся, что word0 короче word1, иначе меняем их местами
        word0, word1 = word1, word0
        len0, len1 = len1, len0

    for k in range(len0):
        if word0[k] != word1[k]:
            left = k
            break
    else:  # если word0 полностью входит в word1
        res = len1 - len0
        return end_difference(res, word0, word1)

    """Если разные длины и префикс не равен word0 (тк предыдущий цикл прервался и не ушёл в return), ищем суффикс"""
    # right = 0
    for i in range(-1, -(len0-left+1), -1):
        if word0[i] != word1[i]:
            if i == -1:
                res = len1 - left
                return end_difference(res, word0, word1)
            right = i + 1
            # print(word0, word1, left, right)
            break
    else:  # если суффикс word0, оставшийся после удаления префикса, полностью содержится в word1
        res = len1 - len0
        return end_difference(res, word0, word1)
    # print(left, right)
    if right != 0:
        new_word0 = word0[left:len0 + right]
        new_word1 = word1[left:len1 + right]

        if new_word0 in new_word1:
            res = len(new_word1) - len(new_word0)
        else:
            new_word1 = list(new_word1)

            for sign in new_word0:
                if sign in new_word1:
                    new_word1.remove(sign)
                else:
                    res += 1
    else:
        res += 1
    res += len1 - len0
    return end_difference(res, word0, word1)

    # print(word0, word1, '|', 'word0:', word0[:left], '+', word0[left:len0+right], '+', word0[len0 + right:], '|',
    #       'word1:', word1[:left], '+', word1[left:len1 + right], '+', word1[len1 + right:], '|',
    #       'left=', left, 'right=', right, 'left-right+1=', left-right+1, len0)


data = joblib.load('shved_vocab.pkl')  # импортируем словник ТЭСРЯ вместе с вариантами слов (варианты через &)
var_list = [x.strip().replace('-...', '...').lower() for x in data if '&' in x]
dict_vars = {}  # структура item: слово : [[варианты], 0/1] 0 if это родитель варианта, 1 if ребёнок

vars = 0
morph = pymorphy2.MorphAnalyzer()
for k in range(len(var_list)):
    base = []

    for element in var_list[k].split('&'):
        if element not in base:
            while element[-1] in '0123456789-':
                element = element[:-1]
            base.append(element)

    if len(base) == 1:
        continue
    # отсеивание вариантов типа ОБТИРАТЬ, [ОБТИРАТЬ]СЯ, ОБТИРКА, ОБТИРОЧНЫЙ см. обтереть, ся. (подробнее см. док)
    # для решения проблемы проверяем, не явлются ли вариантами слова разных частей речи (чаще всего прил-сущ), также
    # убираем глаголы, тк у нас они разделены на отдельные единицы

    # if убрать этот фильтр, останется 2214 слов в словаре
    # if убрать только if 'INFN' in poses, 2158
    vars += 1

    poses = {morph.parse(word)[0].tag.POS for word in base}

    if 'INFN' in poses or 'NOUN' in poses and 'ADJF' in poses:
        continue

    var_list[k] = base

    if len(base) == 3 and difference(base[0], base[2]):  # для
        dict_vars[base[2]] = base[0]

    if difference(base[0], base[1]):
        dict_vars[base[1]] = base[0]


# df = pd.DataFrame(dict_vars)
print(dict_vars)
joblib.dump(dict_vars, 'shved_dict_vars.pkl')
# print(vars)
print(len(dict_vars))

print(difference('заусеница', 'заусенец'))
