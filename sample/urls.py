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
            'continent/<int:pk>/',
            views.get_continent_detail,
            name='continent_detail'
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
            'continent/(?P<pk>[0-9]+)/',
            views.get_continent_detail,
            name='continent_detail'
        ),
    ]
