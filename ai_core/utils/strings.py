import re
from typing import List


def whitespaces_clean(word: str) -> str:
    return re.sub(r'\s', ' ', re.sub(r'\s+', ' ', word)).strip()


def remove_parenthesis(word: str) -> str:
    return whitespaces_clean(re.sub(r'\([\w\-_−–#: !+]*\)', '', word).strip())


def int_to_roman(num: int) -> str:
    val = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    syb = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    roman_num = ""
    for i in range(len(val)):
        count = int(num / val[i])
        roman_num += syb[i] * count
        num -= val[i] * count
    return roman_num


def roman_to_int(s: str) -> int:
    roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000, 'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90,
             'CD': 400, 'CM': 900}
    i = 0
    num = 0
    while i < len(s):
        if i + 1 < len(s) and s[i:i + 2] in roman:
            num += roman[s[i:i + 2]]
            i += 2
        else:
            num += roman[s[i]]
            i += 1
    return num


def levenshtein_distance(s1, s2):
    # This function has already been implemented for you.
    # Source of the implementation:
    # https://stackoverflow.com/questions/2460177/edit-distance-in-python
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2 + 1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1],
                                           distances_[-1])))
        distances = distances_
    return distances[-1]


def closest_result(keyword: str, elements: List[str]) -> str:
    best_distance = levenshtein_distance(keyword, elements[0])
    best_word = elements[0]
    for w in elements:
        d = levenshtein_distance(keyword, w)
        if d < best_distance:
            best_distance = d
            best_word = w

    return best_word
