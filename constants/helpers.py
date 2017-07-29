import logging
import string

import pandas as pd

from constants.constants import COLUMN_NAMES_TRANSLATE_DICT
from users.models import UserProfile


class LoggerFactory:

    @staticmethod
    def get_logger(name='Plain logger'):
        # create logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        return logger


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


def append_user_m2m_fields(df, user_column_id, place):
    """
    :param df: датафрейм, кожен рядок у якому містить id користувача
    :param user_column_id: назва колонки, у якій знаходиться id користувача, може бути user__id, user__user__id
    :param place: колонка, після якої вставляємо нові
    :return: датафрейм df з колонками additional_speciality, additional_position, additional_work
    """
    def get_specialities(user):
        specialities = ', '.join([speciality.name for speciality in user.additional_speciality.all()])
        specialities.strip(', ')
        return {'additional_speciality': specialities}
    
    def get_works(user):
        works = ', '.join([work.name for work in user.works.all()])
        return {'works': works}    
    
    def get_positions(user):
        positions = ', '.join([position.name for position in user.positions.all()])
        return {'positions': positions}

    def get_groups(user):
        groups = ', '.join([group.name for group in user.userfilter_set.all()])
        return {'groups': groups}

    def insert_m2m_columns(column):
        """
        :param column: колонка, яку вставляємо
        :return: датафрейм з вставленою колонкою
        """
        df[column] = new_df[column]
        columns = list(df.columns.values)
        columns.remove(column)
        columns.insert(columns.index(place) + 1, column)
        return df[columns]

    cache_dict = {}
    m2m_columns = ['additional_speciality', 'positions', 'works', 'groups']
    new_df = pd.DataFrame(columns=m2m_columns)
    for row in df.iterrows():
        user_id = row[1][user_column_id]
        if not cache_dict.get(user_id, ''):
            user = UserProfile.objects.get(pk=user_id)
            cache_dict[user_id] = {}
            cache_dict[user_id].update(get_specialities(user))
            cache_dict[user_id].update(get_works(user))
            cache_dict[user_id].update(get_positions(user))
            cache_dict[user_id].update(get_groups(user))
        new_df = new_df.append(cache_dict[user_id], ignore_index=True)
    new_df = new_df.set_index(df.index.values)

    df = insert_m2m_columns('groups')
    df = insert_m2m_columns('additional_speciality')
    df = insert_m2m_columns('positions')
    df = insert_m2m_columns('works')
    return df


def translate_column_names(df):
    """
    :param df: Pandas dataframe
    :return: same dataframe with renamed columns
    """
    col = {}
    for column in df.columns:
        col[column] = COLUMN_NAMES_TRANSLATE_DICT.get(column, column)
    return df.rename(columns=col)

def unique_chain(*iterables):
    """
    :param iterables: querysets
    :return: uniquely chained querysets
    """
    known_ids = set()
    for it in iterables:
        for element in it:
            if element.pk not in known_ids:
                known_ids.add(element.pk)
                yield element