from Arthur.celery import app
from users.admin import UserChangeHistoryAdmin
from users.models import UserExchangeHistory


@app.task
def send_exchange_info():
    UserChangeHistoryAdmin.exchange_to_xls(UserExchangeHistory.objects.all().orderby('-date'))
