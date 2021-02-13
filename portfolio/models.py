from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import Stock


class DirectionChoices(models.TextChoices):
    short = 'short', 'short'
    long = 'long', 'long'


class Portfolio(models.Model):
    name = models.CharField(
        verbose_name=_('Название'),
        max_length=255,
        default='',
        blank=True,
        null=False,
    )
    description = models.TextField(
        verbose_name=_('Описание'),
        default='',
        blank=True,
        null=False,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name=_("Пользователь"),
    )

    def __str__(self):
        return f'{self.name}::{self.user}'

    class Meta:
        verbose_name = _('Портфель')
        verbose_name_plural = _('Портфели')


class PortfolioStock(models.Model):
    portfolio = models.ForeignKey(
        Portfolio,
        verbose_name=_('Портфель'),
        related_name='portfolio_stocks',
        on_delete=models.CASCADE
    )
    stock = models.ForeignKey(
        Stock,
        verbose_name=_('Акция'),
        related_name='portfolio_stocks',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    direction = models.CharField(
        verbose_name=_('Направление'),
        choices=DirectionChoices.choices,
        max_length=5,
        default=DirectionChoices.long,
        blank=True,
        null=False,
    )
    fee = models.FloatField(
        verbose_name=_('Комиссия брокера'),
        default=0,
        blank=True,
        null=False,
    )

    def __str__(self):
        return f'{self.portfolio}::{self.stock.ticker}'

    class Meta:
        verbose_name = _('Элемент портфеля')
        verbose_name_plural = _('Элементы портфелей')


class PortfolioStockLine(models.Model):
    portfolio_stock = models.ForeignKey(
        PortfolioStock,
        verbose_name=_('Элемент портфеля'),
        related_name='portfolio_stock_stock_lines',
        on_delete=models.CASCADE,
        null=True,
    )
    date = models.DateField(
        verbose_name=_('Дата'),
        default=timezone.now,
        blank=True,
        null=False,
    )
    price = models.FloatField(
        verbose_name=_('Цена'),
        default=0,
        blank=True,
        null=False,
    )
    quantity = models.IntegerField(
        verbose_name=_('Количество'),
        default=0,
        blank=True,
        null=False,
    )

    def __str__(self):
        return f'{self.portfolio_stock}::{self.price}::{self.quantity}'

    class Meta:
        verbose_name = _('Акция в портфеле')
        verbose_name_plural = _('Акции в портфеле')


class GoalTypeChoices(models.TextChoices):
    up = 'up', _('вверх')
    down = 'down', _('вниз')


class PortfolioStockGoals(models.Model):
    portfolio_stock = models.ForeignKey(
        PortfolioStock,
        verbose_name=_('Портфель'),
        related_name='portfolio_stock_goals',
        on_delete=models.CASCADE,
        null=True,
    )
    price = models.FloatField(
        verbose_name=_('Цена'),
        default=0,
        blank=True,
        null=False,
    )
    quantity = models.IntegerField(
        verbose_name=_('Количество'),
        default=0,
        blank=True,
        null=False,
    )
    goal_type = models.CharField(
        verbose_name=_('Направление'),
        choices=GoalTypeChoices.choices,
        max_length=4,
        default=GoalTypeChoices.up,
        blank=True,
        null=False,
    )

    def __str__(self):
        return f'{self.portfolio_stock}::{self.price}::{self.quantity}'

    class Meta:
        verbose_name = _('Цель')
        verbose_name_plural = _('Цели')
