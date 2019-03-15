from django.urls import path

from sample import views


app_name = 'sample'
urlpatterns = [
    path(
        'continent/list/',
        views.ContinentListView.as_view(),
        name='continent_list'
    ),
    path(
        'continent/<str:pk>/',
        views.ContinentView.as_view(),
        name='continent_detail'
    ),
]
