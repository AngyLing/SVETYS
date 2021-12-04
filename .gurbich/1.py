# def get_letters_dict(word):
#     """Возвращает словарь вида символ : их количество в слове word"""
#     result = {}
#     for letter in list(word):
#         if letter in result.keys():
#             result[letter] += 1
#         else:
#             result[letter] = 1
#     return result


# def difference(word0, word1):
#     """
#     Возвращает количество букв, которыми отличаются слова word0 и word1.
#     """
#     res = 0
#     letters0 = get_letters_dict(word0)
#     letters1 = get_letters_dict(word1)
#
#     len0, len1 = len(word0), len(word1)
#     # смотрим
#     for sign, numer in letters0.items():
#         if sign in letters1.keys():
#             if letters1[sign] != 0:
#                 letters1[sign]
#
#     print(res, '\t', ''.join(word0), '\t', ''.join(word1))
#     if res >= 2 or res == 0:
#         return False
#     return True
