from django.urls import path

from sample import views


app_name = 'sample'
urlpatterns = [
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
