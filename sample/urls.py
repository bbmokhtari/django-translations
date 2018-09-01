import django

from .views import get_continent_list

app_name = 'sample'
urlpatterns = []

version = int(django.get_version().split('.')[0])
if version == 1:
    from django.conf.urls import url
    urlpatterns += [
        url('continent/list/', get_continent_list, name='continent_list'),
    ]
elif version == 2:
    from django.urls import path
    urlpatterns += [
        path('continent/list/', get_continent_list, name='continent_list'),
    ]
