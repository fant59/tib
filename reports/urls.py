from django.urls import path, include

from . import views
from .stocks.views import ReportView as StocksView
from .advice.views import ReportView as AdviceView
from .api.routes import router

app_name = 'reports'

urlpatterns = [
    path('', (views.IndexView.as_view()), name='index'),
    path('stocks/', (StocksView.as_view()), name='stocks'),
    path('advice/', (AdviceView.as_view()), name='advice'),
    path('api/', include(router.urls)),
]
