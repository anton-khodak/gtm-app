EMPTY = ' '

GENDER_CHOICES = [
    ('male', 'Мужчина'),
    ('female', 'Женщина')
]

CURING_FORM_CHOICES = [
    ('stationar', 'Cтационарное'),
    ('poliklinika', 'Поликлиническое')
]

CATEGORY_CHOICES = [
    ('first', 'Первая'),
    ('second', 'Вторая'),
    ('no_category', 'Без категории'),
]

POLL_CHOICES = [
    ('simple', 'Простой'),
    ('text', 'Текстовый'),
]

ORDER_CHOICES = [
    ('question__poll__id', 'По опросам'),
    ('user__user__id', 'По пользователям'),

]

ORDERS = set(x[0] for x in ORDER_CHOICES)

COLUMN_NAMES_TRANSLATE_DICT = {
    'user__id': 'ID пользователя',
    'user__username': 'Логин',
    'user__first_name': 'Имя',
    'user__last_name': 'Фамилия',
    'patronimyc': 'Отчество',
    'user__email': 'Почта',
    'date_of_birth': 'Дата рождения',
    'age': 'Возраст',
    'gender': 'Пол',
    'city__name': 'Город',
    'area__name': 'Область',
    'score': 'На счету',
    'total_score': 'Всего заработано баллов',
    'total_exchange': 'Всего обменяно',
    'speciality__name': 'Специальность',
    'work__name': 'Леч. учреждение',
    'curing_form': 'Форма лечения',
    'position__name': 'Должность',
    'category': 'Категория',
    'bed_quantity': 'Кол-во коек',
    'patient_quantity': 'Кол-во пациентов',
    'main_phone': 'Главный телефон',
    'secondary_phone': 'Дополнительный телефон',
    'work_phone': 'Рабочий телефон',
    'district': 'Район',
    'house': 'Дом',
    'flat': 'Квартира',
    'index': 'Почтовый индекс',
    # Polls
    'question__poll__id': 'ID опроса',
    'question__poll__name': 'Название опроса',
    'question__id': 'ID вопроса',
    'question__question_text': 'Текст вопроса',
    'id': 'ID ответа',
    'answer_text': 'Текст ответа',
    'useranswers': 'Кол-во ответов пользователей',
    'percent': 'Кол-во ответов в процентах',
    # Exchange
    'user__user__id': 'ID пользователя',
    'user__user__username': 'Логин',
    'user__user__email': 'Почта',
    'exchange': 'Сумма обмена',
    'date': 'Дата',
    'user__score': 'Остаток на счету',
    'user__total_score': 'Всего заработано',
    'user__total_exchange': 'Всего обменяно',
    # UserPoll
    'answer__id': 'ID ответа',
    'answer__answer_text': 'Текст ответа',
    'other_answer': 'Ответ пользователя',
}

GENDER_CHOICES_USER_PROFILE = GENDER_CHOICES.copy()
GENDER_CHOICES_USER_PROFILE.insert(0, (EMPTY, 'Выбрать...'))
CURING_FORM_CHOICES_USER_PROFILE = CURING_FORM_CHOICES.copy()
CURING_FORM_CHOICES_USER_PROFILE.insert(0, (EMPTY, 'Выбрать...'))
CATEGORY_CHOICES_USER_PROFILE = CATEGORY_CHOICES.copy()
CATEGORY_CHOICES_USER_PROFILE.insert(0, (EMPTY, 'Выбрать...'))
