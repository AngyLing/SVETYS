# coding: utf8
import pymorphy2
import time
import joblib

time0 = time.time()
morph = pymorphy2.MorphAnalyzer()


def is_unusual_dict_entry(input_word):
    """
    Функция принимает на вход строку в любом регистре.
    Слова, которые представляют опасность для лингвографической работы и нуждаются в дополнительном просмотре,
    выводятся в виде, удобном для переноса в таблицы формата Microsoft Excel (со знаками табуляции и конца абзаца в
    качестве разделителей столбцов и строк, соответственно). У данных единиц должен быть хотя бы один из таких вариантов
    разбора, как: 1) условная часть речи, по определению не являющаяся начальной формой слова: VERB (спрягаемая форма
    глагола), COMP (форма сравнения), ADJS (краткая форма прилагательного); 2) форма множественного числа или
    принадлежности слова к словам, имеющим формы только множественного числа (типа pluralia tantum); 3) единицы, чьи
    значения отличаются от вариантов её лемм.
    Функция возвращает 1, если слово было выведено, иначе 0.
    Альтернативный вид возвращаемого значения закомментирован в коде, он отличается добавлением исходного слова, если
    оно было признано нестандартным, или пустой строки в ином случае. Так появляется возможность сохранять выданные
    слова в отдельный массив и использовать его для отладки программы под конкретные особенности поданных единиц
    (просмотра различий прошлого и нового массивов с выведенными единицами при редактировании кода или корректировке
    использованных в нём параметров).
    """
    word = input_word.lower()
    if ' ' in word or '...' in word or '…' in word or word[-1] == '-' or word[0] == '-':
        return
    parser = morph.parse(word)

    tags = []
    lemmas = []
    scores = []
    poses = set()

    plural_test = False
    super_test = False
    nomasc_test = False
    test = True

    for var in parser:
        if var.score >= 0.1:
            pos = var.tag.POS
            tag = var.tag
            poses.add(pos)
            tags.append(tag)
            lemmas.append(var.normal_form)
            scores.append(var.score)

            '''проверка на принадлежность форме множественного числа'''
            if ('Pltm' in tag or 'plur' in tag) and 'nomn' in tag and 'Fixd' not in tag:
                plural_test = True

            '''проверка слов именных частей речи на соответствие форме среднего/женского рода'''
            if ('femn' in tag or 'neut' in tag) and 'nomn' in tag and word != var.normal_form:
                nomasc_test = True

            '''проверка на принадлежность превосходной степени сравнения'''
            if 'Supr' in tag and 'nomn' in tag:
                super_test = True

            '''отсеивание субстантивов из выдачи'''
            if pos == 'NOUN':
                nomasc_test = super_test = False

            '''отсеивание слов в именит. падаже и инфинитивов при условии непрохождения предыдущих тестов'''
            if ('nomn' in tag or pos == 'INFN') and not (plural_test or nomasc_test or super_test):
                test = False
                break

    '''вывод единиц'''
    if (word not in lemmas or plural_test or super_test or nomasc_test or 'COMP' in poses or 'VERB' in poses or
            'ADJS' in poses and 'ADVB' not in poses) and test and len(lemmas) > 0:
        print(word, end='\t')
        try:
            print(','.join(poses), end='')
        except TypeError:
            print('Error with POSes', end='')
        finally:
            for i in range(len(lemmas)):
                print('\t', end='')
                print(lemmas[i], tags[i], round(scores[i], 3), sep='\t', end='')
            print('')
            return 1
            # в случае альтернативной выдачи вместо предыдущей строки надо раздокументировать следующую
            # return 1, word
    return 0
    # в случае альтернативной выдачи вместо предыдущей строки следует раздокументировать следующую
    # return 0, ''


# Здесь должен быть массив слов для проверки - words (в качестве тестового можно использовать словник words
# Сводного этимологического словаря "СвЭтиС", для которого писалась функция)
words = joblib.load('test_voc.pkl')

count = 0
# test_list = []


for word in words:
    count += is_unusual_dict_entry(word)
    """
    Для отладки системы используйте альтернативную выдачу: раздокументируйте строку после объявления переменной count и
    следующие строки (закомментировав предыдущую)
    """
    # result = is_unusual_dict_entry(word)
    # count += result[0]
    # if result[1] != '':
    #     test_list.append(result[1])
# print(test_list)

print(f'\nВы подали слов: {len(words)}')
print(
    f'Я сомневаюсь в {count} - их нужно проверить, это составит {round(count * 100 / len(words), 5)} % всего словника')
print(f'Эта программа избавила вас от {round((1 - count / len(words)) * 100, 5)} % ручной обработки')

time1 = time.time()
print(f'\nПрограмма выполнена за {round(time1 - time0, 5)} сек.')


# developed by Angy
