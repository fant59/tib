from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import Portfolio, PortfolioStock, PortfolioStockLine, PortfolioStockGoals


class PortfolioStockInlines(admin.TabularInline):
    model = PortfolioStock
    extra = 0
    fields = [
        'id',
        'stock',
        'direction',
        'fee',
    ]
    max_num = 50
    readonly_fields = ['stock', ]


@register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'user',
    ]
    inlines = [PortfolioStockInlines, ]
    list_select_related = ['user', ]


class PortfolioStockLineInlines(admin.TabularInline):
    model = PortfolioStockLine
    extra = 0
    fields = [
        'id',
        'price',
        'quantity',
    ]
    max_num = 50


class PortfolioStockGoalsInlines(admin.TabularInline):
    model = PortfolioStockGoals
    extra = 0
    fields = [
        'id',
        'price',
        'quantity',
        'goal_type',
    ]
    max_num = 50


@register(PortfolioStock)
class PortfolioStockAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'portfolio',
        'stock',
        'direction',
        'fee',
    ]
    list_select_related = ['stock', 'portfolio']
    inlines = [PortfolioStockLineInlines, PortfolioStockGoalsInlines]
