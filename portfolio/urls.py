from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

app_name = 'portfolio'

urlpatterns = [
    path(
        '',
        login_required(views.PortfolioListView.as_view()),
        name='portfolio_list'
    ),
    path(
        'portfolio/create/',
        login_required(views.PortfolioCreateView.as_view()),
        name='portfolio_create'
    ),
    path(
        'portfolio/delete/<int:pk>/',
        login_required(views.PortfolioDeleteView.as_view()),
        name='portfolio_delete'
    ),
    path(
        'portfolio/update/<int:pk>/',
        login_required(views.PortfolioUpdateView.as_view()),
        name='portfolio_update',
    ),

    # portfolio_stock ---------------------------------------------------------
    path(
        'portfolio_stock/create/',
        login_required(views.PortfolioStockCreateView.as_view()),
        name='portfolio_stock_create'
    ),
    path(
        'portfolio_stock/update/<int:pk>/',
        login_required(views.PortfolioStockUpdateView.as_view()),
        name='portfolio_stock_update',
    ),
    path(
        'portfolio_stock/delete/<int:pk>/',
        login_required(views.PortfolioStockDeleteView.as_view()),
        name='portfolio_stock_delete',
    ),

    # portfolio_stock_line-----------------------------------------------------
    path(
        'portfolio_stock_line/list/',
        login_required(views.PortfolioStockLineListView.as_view()),
        name='portfolio_stock_line_list'
    ),
    path(
        'portfolio_stock_line/create/',
        login_required(views.PortfolioStockLineCreateView.as_view()),
        name='portfolio_stock_line_create'
    ),
    path(
        'portfolio_stock_line/update/<int:pk>/',
        login_required(views.PortfolioStockLineUpdateView.as_view()),
        name='portfolio_stock_line_update'
    ),
    path(
        'portfolio_stock_line/delete/<int:pk>/',
        login_required(views.PortfolioStockLineDeleteView.as_view()),
        name='portfolio_stock_line_delete'
    ),
]
