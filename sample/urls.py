import django

from .views import get_continent_list

app_name = 'sample'
urlpatterns = []

if int(django.get_version().split('.')[0]) == 2:
    from django.urls import path
    urlpatterns += [
        path('continent/list/', get_continent_list, name='continent_list'),
    ]
else:
    from django.conf.urls import url
    urlpatterns += [
        url('continent/list/', get_continent_list, name='continent_list'),
    ]
