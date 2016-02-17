import os

from django.http import HttpResponse
from pandas import ExcelWriter


def export_to_xls(df, path, format_excel=None, engine='xlsxwriter'):
    writer = ExcelWriter(path,
                         engine=engine,
                         datetime_format='hh:mm:ss mmm d yyyy',
                         date_format='mmmm dd yyyy')
    df.to_excel(writer)
    writer.save()
    if format_excel: format_excel(path)
    return download_file(path)


def download_file(path):
    with open(path, "rb") as excel:
        data = excel.read()
    response = HttpResponse(data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=' + path
    # os.remove(path)
    return response
