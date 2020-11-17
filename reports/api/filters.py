# coding=utf-8

from __future__ import unicode_literals

import django_filters
from core.models import DayCandle


class DayCandleFilter(django_filters.FilterSet):
    figi = django_filters.CharFilter(method='filter_figi')

    class Meta:
        model = DayCandle
        fields = ['figi']

    def filter_figi(self, queryset, name, value):
        if not value:
            return self.Meta.model.objects.none()
        return queryset.filter(stock__figi=value)

