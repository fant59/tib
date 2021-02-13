from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from users import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('reports', include('reports.urls', namespace='reports')),
    path('login/', views.login, {'template_name': 'login.html'}, name='login-view'),
    path('logout/', views.logout_view, name='logout-view'),
    path('', include('portfolio.urls', namespace='portfolio')),
]


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += staticfiles_urlpatterns('/.' + settings.STATIC_URL)
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
