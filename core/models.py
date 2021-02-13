from datetime import datetime
from typing import Union

from django.db import models
from django.db.models import Max


class CurrencyChoices(models.TextChoices):
    rub = 'RUB', 'RUB'
    usd = 'USD', 'USD'
    eur = 'EUR', 'EUR'
    gbp = 'GBP', 'GBP'
    hkd = 'HKD', 'HKD'
    chf = 'CHF', 'CHF'
    jpy = 'JPY', 'JPY'
    cny = 'CNY', 'CNY'
    try_ = 'TRY', 'TRY'


class Stock(models.Model):
    currency = models.CharField(
        max_length=4,
        choices=CurrencyChoices.choices,
        blank=True,
        null=True,
    )
    figi = models.CharField(
        unique=True,
        max_length=12,
    )
    isin = models.CharField(
        max_length=12,
    )
    lot = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    min_price_increment = models.FloatField(
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=150,
    )
    ticker = models.CharField(
        max_length=8,
    )
    min_quantity = models.FloatField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        ordering = ('ticker', )

    def __str__(self):
        return f'{self.ticker}:{self.name}'


class DayCandleQuerySet(models.QuerySet):
    def get_last_date(self) -> Union[datetime, None]:
        obj = self.aggregate(max_time=Max('time'))
        try:
            return obj['max_time']
        except (AttributeError, KeyError):
            return None


class DayCandle(models.Model):
    stock = models.ForeignKey(
        Stock,
        related_name='candles',
        on_delete=models.CASCADE
    )
    o = models.FloatField(
        default=0
    )
    c = models.FloatField(
        default=0
    )
    oc_diff = models.FloatField(
        default=0
    )
    oc_diff_up_zero = models.IntegerField(
        default=0
    )
    h = models.FloatField(
        default=0
    )
    l = models.FloatField(
        default=0
    )
    v = models.FloatField(
        default=0
    )
    time = models.DateField(
        blank=True,
        null=True
    )

    objects = DayCandleQuerySet.as_manager()

    class Meta:
        verbose_name = 'Day candle'
        verbose_name_plural = 'Day candles'
        ordering = ['stock', '-time']

    def __str__(self):
        return f'{self.stock}:{self.time.strftime("%d.%m.%Y")}'

    def _set_diff(self):
        self.oc_diff = (self.c - self.o) / self.o * 100
        self.oc_diff_up_zero = 1 if self.oc_diff > 0 else -1

    def save(self, *args, **kwargs):
        if self.id is None:
            self._set_diff()

        super().save(*args, **kwargs)



