from django.contrib import admin
from django.contrib.admin.decorators import register

from core.models import Stock, DayCandle


class DayCandleInlines(admin.TabularInline):
    model = DayCandle
    extra = 0
    fields = [
        'o',
        'c',
        'oc_diff',
        'oc_diff_up_zero',
        'h',
        'l',
        'v',
        'time',
    ]
    max_num = 50


@register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_filter = ['currency', ]
    search_fields = ['ticker', 'figi', ]
    list_display = [
        'ticker',
        'name',
        'currency',
        'figi',
        'isin',
        'lot',
        'min_price_increment',
    ]
    inlines = [DayCandleInlines, ]
