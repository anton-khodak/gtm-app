import string

from constants.constants import COLUMN_NAMES_TRANSLATE_DICT


def translit(s):
    """
    Функція переводить у трансліт та нижній регістр рядок
    """
    DICT = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ж': 'zh',
        'з': 'z',
        'и': 'i',
        'й': 'j',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'h',
        'ц': 'c',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'sch',
        'ь': '',
        'ю': 'yu',
        'я': 'ya',
        'ы': 'y',
        'ъ': 'j',
        'э': 'e',
        'ё': 'e',
        ' ': '_',
    }
    res = ''
    for letter in string.punctuation:
        DICT[letter] = '_'
    if s:
        s = s.lower()
        for letter in s:
            if letter in DICT.keys():
                res += DICT[letter]
            else:
                res += letter
        res = res.replace('___', '_')
        res = res.replace('__', '-')
        res = res[:20]
    return res


def translate_column_names(df):
    """
    :param df: Pandas dataframe
    :return: same dataframe with renamed columns
    """
    col = {}
    for column in df.columns:
        col[column] = COLUMN_NAMES_TRANSLATE_DICT.get(column, column)
    return df.rename(columns=col)
