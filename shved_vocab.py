# coding: utf8
import joblib
import pymorphy2

data = joblib.load('shved_vocab.pkl')  # импортируем словник ТЭСРЯ вместе с вариантами слов (варианты через &
var_list = [x.strip().replace('-...', '...').lower() for x in data if '&' in x]
dict_vars = {}  # структура item: слово : [[варианты], 0/1] 0 if это родитель варианта, 1 if ребёнок

morph = pymorphy2.MorphAnalyzer()
for k in range(len(var_list)):
    base = []

    for element in var_list[k].split('&'):
        if element not in base:
            # while element[-1] in '0123456789-':
            #     element = element[:-1]
            base.append(element)

    if len(base) == 1:
        continue
    # отсеивание вариантов типа ОБТИРАТЬ, [ОБТИРАТЬ]СЯ, ОБТИРКА, ОБТИРОЧНЫЙ см. обтереть, ся. (подробнее см. док)
    # для решения проблемы проверяем, не явлются ли вариантами слова разных частей речи (чаще всего прил-сущ), также
    # убираем глаголы, тк у нас они разделены на отдельные единицы

    # if убрать этот фильтр, останется 2214 слов в словаре
    # if убрать только if 'INFN' in poses, 2158

    poses = {morph.parse(word)[0].tag.POS for word in base}

    if 'INFN' in poses or 'NOUN' in poses and 'ADJF' in poses:
        continue

    var_list[k] = base
    if len(base) == 2:
        dict_vars[base[0]] = ([base[1]], 0)
        dict_vars[base[1]] = ([base[0]], 1)

    # просмотр единиц, где число вариантов осталось более одного. обнаружение
    # ['замуслить', 'замуслиться', 'замусолить', 'замусолиться']
    else:
        assert len(base) > 2
        dict_vars[base[1]] = ([base[0], base[2]], 1)
        dict_vars[base[2]] = ([base[0], base[1]], 1)


print(dict_vars)
print(len(dict_vars))
# joblib.dump(dict_vars, 'shved_dict_vars.pkl')
