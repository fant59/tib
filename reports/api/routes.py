# coding=utf-8
from __future__ import unicode_literals, absolute_import

from django.conf import settings

from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register(r'report-base-chart',
                views.BaseChartsViewSet,
                basename='report-base-chart')
