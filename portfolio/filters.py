import django_filters

from portfolio.models import PortfolioStockLine


class PortfolioStockLineFilter(django_filters.FilterSet):
    portfolio_stock_id = django_filters.NumberFilter(
        field_name='portfolio_stock_id'
    )

    class Meta:
        model = PortfolioStockLine
        fields = ['portfolio_stock_id']
