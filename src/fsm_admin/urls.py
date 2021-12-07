from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createtournaments', views.createtournaments, name='createtournaments'),
    path('tournament/<str:pk>', views.tournament, name='tournament'),
    path('search', views.search, name='search'),
    path('edittournament/<str:pk>', views.edittournament, name='edittournament'),
]
