import re
from datetime import datetime, date
from difflib import SequenceMatcher
from typing import List, Optional, Tuple


####################################################
#                  STRING CLEANUP                  #
####################################################

def whitespaces_clean(word: str) -> str:
    return re.sub(r'\s', ' ', re.sub(r'\s+', ' ', word)).strip()


def remove_parenthesis(word: str) -> str:
    return whitespaces_clean(re.sub(r'\([\w\-_−–#: !+]*\)', '', word))


def remove_symbols(word: str, ignore_quotes: bool = False) -> str:
    reg = r'[^a-zA-Z0-9\-"\']' if ignore_quotes else r'[^a-zA-Z0-9\-]'
    return whitespaces_clean(re.sub(reg, ' ', word))


def remove_editions(word: str) -> str:
    return whitespaces_clean(' '.join(w for w in word.split() if find_roman(re.sub(r'[\'\".:]', '', w)) is None))


def remove_conjunctions(word: str) -> str:
    conjunctions = [
        'EL', 'LA', 'LOS', 'LAS',
        'O', 'A', 'OS', 'AS',
        'DE', 'DA', 'DO', 'DAS', 'DOS', 'DEL',
        'L', 'ELS', 'LES', 'SES', 'ES', 'SA',
    ]
    return ' '.join(i for i in word.split() if i not in conjunctions)


####################################################
#                  ROMAN NUMBERS                   #
####################################################

def find_roman(word: str) -> Optional[str]:
    """
    :return: #word if #word is a roman number
    """
    match = re.match(r'^M{0,3}(CM|CD|D?C{0,3})?(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?$', word)
    return ''.join(match.groups()) if match else None


def int_to_roman(num: int) -> str:
    """
    :return: converts an integer number to a roman number
    """
    val = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    syb = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I')
    roman_num = ""
    for i in range(len(val)):
        count = int(num / val[i])
        roman_num += syb[i] * count
        num -= val[i] * count
    return roman_num


def roman_to_int(s: str) -> int:
    """
    :return: converts a roman number to an integer number
    """
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


####################################################
#                       DATE                       #
####################################################
def find_date(w: str) -> Optional[date]:
    """
    :return: any matching date in the format of DD-MM-YYYY
    """
    match = re.search(r"([0-9]{2}-[0-9]{2}-[0-9]{4})", w)
    if not match:
        return None
    try:
        return datetime.strptime(match.group(0), '%d-%m-%Y').date()
    except ValueError:
        return None


####################################################
#                    UTILITIES                     #
####################################################

def closest_result(keyword: str, elements: List[str]) -> Tuple[Optional[str], float]:
    if any(e == keyword for e in elements):
        return keyword, 1.

    best_distance = SequenceMatcher(a=keyword, b=elements[0]).ratio()
    best_word = elements[0]
    for possibility in elements:
        if all(w in keyword for w in possibility.split()) and all(w in possibility for w in keyword.split()):
            return possibility, 1.

        d = SequenceMatcher(a=keyword, b=possibility).ratio()
        if d > best_distance:
            best_distance = d
            best_word = possibility

    return best_word, best_distance
