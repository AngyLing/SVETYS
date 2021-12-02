# coding: utf8
import pymorphy2
import time
import joblib

'''
Program to find word from svod which is form of another word from svod.

'''
time0 = time.time()

morph = pymorphy2.MorphAnalyzer()


def is_forms_of_word_svod(element, data):
    if len(element) == 1:
        return 0
    word = element.lower()
    parser = morph.parse(word)
    lemmas = set()
    poses = set()
    test = 0

    for var in parser:
        lemma = var.normal_form
        if var.score >= 0.2 and lemma != word and lemma.upper() in data:
            lemmas.add(lemma)
            poses.add(var.tag.POS)
            '''
            Важно добавлять хотя бы части речи для каждого варианта, чтобы смотреть проблемные единицы не по алфавиту 
            (что является неудобным), а по схожим случаям, разбив все слова на группы по части речи
            '''
            test = 1
    if test == 1:
        # TODO: add score in output
        print(word, end='\t')
        print(', '.join(poses), end='\t')
        print(', '.join(lemmas))
    return test


words = joblib.load('../autosvod/variants/svet_vcb.pkl')
print(words[:100])

res = 0

for word in words:
    res += is_forms_of_word_svod(word, words)

print(f'Вы подали {len(words)} слов')
print(f'Я сомневаюсь в {res}, их нужно проверить')
print(f'Эта программа избавила вас от {round((1 - res / len(words)) * 100, 3)} % ручной обработки :)')

time1 = time.time()

print(round(time1 - time0, 5))
