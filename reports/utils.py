from django.apps import apps
from django.urls import reverse


def ger_report_app():
    reports = []
    for app in apps.get_app_configs():
        name = app.name.split('.')
        if len(name) > 1 and name[0] == 'reports':
            reports.append({
                'name': app.verbose_name,
                'url': reverse(f'reports:{app.label}')
            })
    return reports
