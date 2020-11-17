# coding=utf-8
from __future__ import unicode_literals, absolute_import

import itertools

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from django.template.loader import get_template
from rest_framework import viewsets
from rest_framework.response import Response

from core.models import DayCandle
from .filters import DayCandleFilter
from .serializers import DayCandleSerializer


class BaseChartsViewSet(viewsets.ReadOnlyModelViewSet):
    model = DayCandle
    queryset = DayCandle.objects.filter()

    serializer_class = DayCandleSerializer
    filterset_class = DayCandleFilter

    @staticmethod
    def make_month_results(data, month_slice=1):
        now = pd.to_datetime("today")
        start_date = now - relativedelta(months=month_slice - 1)
        start_date = start_date.date().replace(day=1)
        date_slice = pd.date_range(
            start=start_date,
            end=now,
            freq='W'
        )

        _df = data[date_slice[0]:]

        # all diff more then zero and less the zero
        oc_diff_up_zero = _df['oc_diff_up_zero'].sum()
        oc_diff_down_zero = _df.shape[0] - oc_diff_up_zero

        try:
            oc_diff_up_zero = oc_diff_up_zero / _df.shape[0]
        except ZeroDivisionError:
            oc_diff_up_zero = 0

        try:
            oc_diff_down_zero = oc_diff_down_zero / _df.shape[0]
        except ZeroDivisionError:
            oc_diff_down_zero = 0

        result = _df.mean().round(2).to_dict()
        result.update({
            'oc_diff_up_zero': round(oc_diff_up_zero, 2),
            'oc_diff_down_zero': round(oc_diff_down_zero, 2)
        })
        return result

    def get_last_statistic(self, data, by_html=True):
        day_df = data[['time', 'o', 'c', 'oc_diff', 'oc_diff_up_zero']]
        day_df = day_df.resample('B', on='time').min()
        day_df = day_df.dropna()

        # diff = close value - open value
        day_df['oc_diff_cumsum'] = day_df['oc_diff_up_zero'].cumsum()

        month_1 = self.make_month_results(day_df, month_slice=1)
        month_3 = self.make_month_results(day_df, month_slice=3)
        month_6 = self.make_month_results(day_df, month_slice=6)

        last = [
            {
                'period': ' 1',
                'data': month_1},
            {
                'period': ' 3',
                'data': month_3},
            {
                'period': ' 6',
                'data': month_6},
        ]
        if by_html:
            template = get_template('reports/item_table.html')
            return template.render({'last': last}, self.request)

        return last

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(
            stock__figi=request.query_params['figi'])

        serializer = self.get_serializer(queryset, many=True)

        base_df = pd.DataFrame(serializer.data)

        base_df['time'] = pd.to_datetime(base_df['time'])
        base_df.drop(columns=['stock'], inplace=True)

        df = base_df[['time', 'o', 'c', 'oc_diff', 'oc_diff_up_zero']]
        df = df.resample('W', on='time').agg(
            {'o': np.min, 'oc_diff': np.sum, 'oc_diff_up_zero': np.sum})

        # diff = close value - open value
        df['oc_diff_cumsum'] = df['oc_diff_up_zero'].cumsum()

        df = df.dropna(0)
        color_gen = itertools.count()

        colors = ['red', 'blue', 'green', 'black']
        result = {
            'datasets': [
                {
                    'label': 'oc_diff',
                    'data': df['oc_diff'].round(2).tolist(),
                    'backgroundColor': 'rgba(0,0,0,0)',
                    'borderColor': colors[color_gen.__next__()]},
                {
                    'label': 'oc_diff_cumsum',
                    'data': df['oc_diff_cumsum'].round(2).tolist(),
                    'backgroundColor': colors[color_gen.__next__()]},
                {
                    'label': 'open',
                    'data': df['o'].round(5).tolist(),
                    'backgroundColor': colors[color_gen.__next__()]},
            ],
            'labels': df.index.strftime('%d.%m.%Y').tolist(),
            'last': self.get_last_statistic(base_df),
        }

        return Response(result)
