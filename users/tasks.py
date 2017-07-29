from datetime import timedelta

from django.utils import timezone

from Arthur.celery import app
from users.admin import UserChangeHistoryAdmin
from users.models import UserExchangeHistory


# @app.task
def send_exchange_info():
    today = timezone.now()
    UserChangeHistoryAdmin.exchange_to_xls(queryset=UserExchangeHistory.objects.filter(date__gte=today - timedelta(days=1))
                                           .order_by('-date'),
                                           day_from=today.strftime("%Y-%m-%d"),
                                           send=True)