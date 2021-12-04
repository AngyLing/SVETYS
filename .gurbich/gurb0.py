# coding: utf8
import joblib


words = joblib.load('../../autosvod/data/test_voc.pkl')

len = len(words)
counter_defis = 0
counter_treespace = 0
counter_space = 0

for word in words:
    if ' ' in word:
        counter_space += 1
        # print(word)
    elif '...' in word or '…' in word:
        counter_treespace += 1

    elif word[-1] == '-' or word[0] == '-':
        counter_defis += 1

print('Spaces:', counter_space, round(counter_space * 100 / len, 3))
print('Treespaces:', counter_treespace, round(counter_treespace * 100 / len, 3))
print('Defises:', counter_defis, round(counter_defis * 100 / len, 3))

print(counter_treespace + counter_space, round((counter_treespace+counter_space) * 100 / len, 3))

print(len)