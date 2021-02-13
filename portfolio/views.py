from django.contrib.auth import get_user
from django.db.models import F, FloatField, ExpressionWrapper, OuterRef, \
    Subquery, Value
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DeleteView,
    UpdateView,
    CreateView,
)

from core.models import DayCandle
from portfolio.filters import PortfolioStockLineFilter
from portfolio.forms import PortfolioForm, PortfolioStockForm, \
    PortfolioStockLineForm
from portfolio.models import Portfolio, PortfolioStock, PortfolioStockLine


class PortfolioListView(ListView):
    model = Portfolio
    queryset = Portfolio.objects.\
        prefetch_related('portfolio_stocks').\
        select_related('user')
    template_name = 'portfolio/list.html'

    def get(self, request, *args, **kwargs):
        try:
            self.portfolio_id = int(request.GET.get('portfolio_id'))
        except (ValueError, TypeError):
            self.portfolio_id = None

        self.user = get_user(self.request)

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        self.portfolio_id = self.portfolio_id \
            if self.portfolio_id is not None \
            else self.object_list.first()

        self.portfolio_id = self.portfolio_id.id \
            if isinstance(self.portfolio_id, self.model) \
            else self.portfolio_id

        context['portfolio_id'] = self.portfolio_id
        context['portfolio_stocks'] = PortfolioStock.objects.\
            filter(portfolio=self.portfolio_id,
                   portfolio__user_id=self.user.id).\
            select_related('stock').\
            prefetch_related('portfolio_stock_stock_lines',
                             'portfolio_stock_goals')

        return context

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.portfolio_stock = PortfolioStock.objects.none()
        self.portfolio_id = None
        self.user = None


class PortfolioCreateView(CreateView):
    model = Portfolio
    form_class = PortfolioForm
    template_name = 'portfolio/form.html'
    success_url = reverse_lazy('portfolio:portfolio_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': get_user(self.request)})
        return kwargs


class PortfolioUpdateView(UpdateView):
    model = Portfolio
    form_class = PortfolioForm
    template_name = 'portfolio/form.html'
    success_url = reverse_lazy('portfolio:portfolio_list')


class PortfolioDeleteView(DeleteView):
    model = Portfolio
    template_name = 'portfolio/delete.html'
    success_url = reverse_lazy('portfolio:portfolio_list')


class PortfolioStockCreateView(CreateView):
    model = PortfolioStock
    form_class = PortfolioStockForm
    template_name = 'portfolio_stock/form.html'
    success_url = reverse_lazy('portfolio:portfolio_list')

    def get_initial(self):
        initial = super().get_initial()
        if self.request.method == 'GET':
            initial.update(
                {'portfolio': self.request.GET.get('portfolio_id')}
            )
        return initial


class PortfolioStockUpdateView(UpdateView):
    model = PortfolioStock
    form_class = PortfolioStockForm
    template_name = 'portfolio_stock/form.html'
    success_url = reverse_lazy('portfolio:portfolio_list')


class PortfolioStockDeleteView(DeleteView):
    model = PortfolioStock
    template_name = 'portfolio_stock/delete.html'
    success_url = reverse_lazy('portfolio:portfolio_list')


class PortfolioStockLineListView(ListView):
    model = PortfolioStockLine
    queryset = PortfolioStockLine.objects.\
        select_related('portfolio_stock',
                       'portfolio_stock__stock')
    template_name = 'portfolio_stock_line/list.html'
    context_object_name = 'portfolio_stocks_lines'
    filter_class = PortfolioStockLineFilter

    def get_queryset(self):
        candle = DayCandle.objects.\
            select_related('stock').\
            filter(stock_id=OuterRef('portfolio_stock__stock__id'))

        qs = super().get_queryset(). \
            annotate(day_price=Subquery(candle.values('o')[:1])). \
            annotate(buy_total=ExpressionWrapper(
                F('price') * F('quantity'),
                output_field=FloatField())). \
            annotate(day_total=ExpressionWrapper(
                (F('day_price') - F('price')) * F('quantity'),
                output_field=FloatField())).\
            annotate(day_percent=ExpressionWrapper(
                F('day_total') / F('buy_total') * Value(100),
                output_field=FloatField()))

        return self.filter_class(self.request.GET, qs).qs


class PortfolioStockLineCreateView(CreateView):
    model = PortfolioStockLine
    form_class = PortfolioStockLineForm
    template_name = 'portfolio_stock_line/form.html'
    success_url = reverse_lazy('portfolio:portfolio_list')

    def get_initial(self):
        initial = super().get_initial()
        if self.request.method == 'GET':
            initial.update(
                {'portfolio_stock': self.request.GET.get('portfolio_stock_id')}
            )
        return initial


class PortfolioStockLineUpdateView(UpdateView):
    model = PortfolioStockLine
    form_class = PortfolioStockLineForm
    template_name = 'portfolio_stock_line/form.html'
    success_url = reverse_lazy('portfolio:portfolio_list')


class PortfolioStockLineDeleteView(DeleteView):
    model = PortfolioStockLine
    template_name = 'portfolio_stock_line/delete.html'
    success_url = reverse_lazy('portfolio:portfolio_list')

