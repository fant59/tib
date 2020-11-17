from celery.task import task
from django.conf import settings

from core.core import SandBox


@task
def get_candles():
    api = SandBox(settings.TOKEN)
    api.init()
    api.get_candles()
