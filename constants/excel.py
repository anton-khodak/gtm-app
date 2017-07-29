import datetime
import locale
import os

from django.core.mail.message import EmailMessage
from django.http import HttpResponse
from pandas import ExcelWriter


admin_mail = 'anton.khodak@ukr.net'


def export_to_xls(df, path, format_excel=None, engine='openpyxl', send=False):
    writer = ExcelWriter(path,
                         engine=engine,
                         datetime_format='hh:mm:ss mmm d yyyy',
                         date_format='mmmm dd yyyy')
    df.to_excel(writer)
    writer.save()
    if format_excel: format_excel(path)
    if send:
        send_file_by_email(path)
    else:
        return download_file(path)


def download_file(path):
    with open(path, "rb") as excel:
        data = excel.read()
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + path
    os.remove(path)
    return response

def send_file_by_email(path):
    print('path: ', path)
    with open(path, "rb") as excel:
        data = excel.read()
    email = EmailMessage(subject='Обмены баллов {0}'.format(datetime.date.today().strftime('%d %b')),
                         body='',
                         to=[admin_mail, ],
                         attachments=[(path, data, 'application/vnd.ms-excel') ])
    email.send()
    print('sent!')

    # os.remove(path)





