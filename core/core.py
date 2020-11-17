import typing
from datetime import datetime
from time import sleep, time as this_time

import tinvest
from dateutil.relativedelta import relativedelta
from django.apps import apps
from django.db.models import OuterRef, Subquery, DateTimeField
from django.db.models.functions import Cast
from requests import RequestException
from tinvest import (
    SandboxRegisterRequest,
    BrokerAccountType,
    CandleResolution,
)


class SandBox:
    datetime_or_str = typing.Union[datetime, None]

    def __init__(self, token) -> None:
        self.Stock = apps.get_model('core', 'Stock')
        self.DayCandle = apps.get_model('core', 'DayCandle')

        self.client = tinvest.SyncClient(token, use_sandbox=True)
        self.sandbox = tinvest.SandboxApi(self.client)
        self.market = tinvest.MarketApi(self.client)
        self._is_init = False
        self.account = None

    def init(self) -> None:
        self._is_init = False
        body = SandboxRegisterRequest(
            broker_account_type=BrokerAccountType.tinkoff)

        result = self.sandbox.sandbox_register_post(body)

        if result.status_code != 200:
            raise RequestException(result.text)

        self.account = result.parse_json().payload
        self._is_init = True

    def get_market_stocks(self) -> None:
        r = self.market.market_stocks_get()
        if r.status_code == 200:
            for i in r.parse_json().payload.instruments:
                _i = i.dict()
                _ = _i.pop('type')
                figi = _i.pop('figi')
                obj, _ = \
                    self.Stock.objects.update_or_create(figi=figi, defaults=_i)

    def get_candles(self, deep_year: int = 10,
                    request_count: int = 120) -> None:

        if not self._is_init:
            raise ValueError('must be init first')

        today = datetime.now()

        subquery = self.DayCandle.objects.filter(
            stock=OuterRef('pk')).order_by('-time')
        from_date = Cast(Subquery(subquery.values('time')[:1]),
                         output_field=DateTimeField())
        qs = self.Stock.objects.annotate(from_date=from_date).values(
            'figi', 'from_date', 'id')

        time_measurement = this_time()
        count = 0

        for stock in qs:
            from_date = \
                stock['from_date'] or today - relativedelta(years=deep_year)
            from_date = from_date.replace(tzinfo=None)

            while from_date <= today:
                this_from = from_date
                from_date += relativedelta(years=1)
                this_to = from_date

                r = self.market.market_candles_get(
                    stock['figi'],
                    this_from,
                    this_to,
                    CandleResolution.day
                )
                generator = (i for i in r.parse_json().payload.candles
                             if r.status_code == 200)
                for i in generator:
                    _i = i.dict()
                    time = _i.pop('time')
                    _ = _i.pop('figi')
                    _ = _i.pop('interval')
                    obj, _ = self.DayCandle.objects.update_or_create(
                        stock_id=stock['id'], time=time, defaults=_i)

                count += 1
                if count == request_count:
                    diff = this_time() - time_measurement
                    sleep(diff if diff < 60 else 0)

                    time_measurement = this_time()
                    count = 0
