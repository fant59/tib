from rest_framework import serializers

from core.models import DayCandle


class DayCandleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayCandle
        fields = [
            'stock',
            'o',
            'c',
            'h',
            'l',
            'v',
            'time',
            'oc_diff',
            'oc_diff_up_zero',
        ]
