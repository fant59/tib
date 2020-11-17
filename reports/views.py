import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from django.views.generic import TemplateView, ListView

from core.models import Stock, CurrencyChoices
from reports.api.serializers import DayCandleSerializer
from reports.utils import ger_report_app


class IndexView(ListView):
    queryset = Stock.objects.filter(currency=CurrencyChoices.usd)
    template_name = 'reports/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = ger_report_app()
        return context
