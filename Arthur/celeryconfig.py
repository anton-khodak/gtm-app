from __future__ import absolute_import
from celery.schedules import crontab
import datetime


CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json',]
CELERY_TIMEZONE = 'Europe/Kiev'


CELERYBEAT_SCHEDULE = {
    'send-exchange-info-24-hours': {
        'task': 'users.tasks.send_exchange_info',
        'schedule': crontab(minute=0, hour=13),
        # 'args': ('12 hr', )
     },
}