from django.urls import path

from .views import get_continent_list

app_name = 'sample'
urlpatterns = [
    path('continent/list/', get_continent_list, name='continent_list'),
]
