import django

from . import views

app_name = 'sample'
urlpatterns = []

if int(django.get_version().split('.')[0]) == 2:
    from django.urls import path
    urlpatterns += [
        path(
            'continent/list/',
            views.get_continent_list,
            name='continent_list'
        ),
        path(
            'continent/detailed/',
            views.get_continent_list_detailed,
            name='continent_list_detailed'
        ),
    ]
else:
    from django.conf.urls import url
    urlpatterns += [
        url(
            'continent/list/',
            views.get_continent_list,
            name='continent_list'
        ),
        url(
            'continent/detailed/',
            views.get_continent_list_detailed,
            name='continent_list_detailed'
        ),
    ]
