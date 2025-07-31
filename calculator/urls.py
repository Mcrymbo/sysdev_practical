from django.urls import path
from . import views

app_name = 'calculator'

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('api/calculate/', views.api_calculate, name='api_calculate'),
] 