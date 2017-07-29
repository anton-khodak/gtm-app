"""
скрипт проходиться по всіх userspolls і видаляє ті, які потрапили до користувача випадково або старі, тобто ті,
які на даний момент не було присвоєні користувачеві у жодному з опитувань чи то в групі, чи то окремо
"""

import os
from functools import lru_cache

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'Arthur.settings'
django.setup()


from constants.helpers import LoggerFactory
from polls.models import UsersPoll, Poll


def main():

    @lru_cache(maxsize=40)
    def get_related_users(poll):
        return poll.get_all_related_users()

    logger = LoggerFactory.get_logger(__name__)
    userspolls = UsersPoll.objects.all()
    logger.info('{0} userspolls in database'.format(userspolls.count()))

    userspolls_to_delete = []
    for userspoll in UsersPoll.objects.all():
        poll = Poll.objects.get(pk=userspoll.poll_id)
        if not userspoll.user in get_related_users(poll):
            logger.info('Deleting userspoll {0}-{1}'.format(userspoll.poll.name, userspoll.user.user.username))
            userspolls_to_delete.append(userspoll)
    logger.info('Deleting {0} userspolls'.format(len(userspolls_to_delete)))
    agreement = input('Удалить все опросы выше из кабинетов пользователей? y/n')
    if agreement == 'y':
        for up in userspolls_to_delete:
            up.delete()
        logger.info('{0} userspolls left'.format(UsersPoll.objects.all().count()))
    else:
        logger.info('Опросы не удалены')


if __name__ == "__main__":
    main()