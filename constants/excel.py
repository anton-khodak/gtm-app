import datetime

from django.core.mail.message import EmailMessage
from django.http import HttpResponse
from pandas import ExcelWriter


admin_mail = 'gtm.admi@gmail.com'


def export_to_xls(df, path, format_excel=None, engine='xlsxwriter', send=False):
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
    # os.remove(path)
    return response

def send_file_by_email(path):
    with open(path, "rb") as excel:
        data = excel.read()
    email = EmailMessage(subject='Отчёт {0}'.format(str(datetime.date.today)),
                         body='',
                         to=[admin_mail, ],
                         attachments=[(path, data, 'application/vnd.ms-excel') ])
    email.send()





