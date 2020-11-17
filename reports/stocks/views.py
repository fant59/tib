from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from core.models import Stock


class ReportView(ListView):
    model = Stock
    queryset = Stock.objects.filter()
    template_name = 'reports/stocks/list.html'

