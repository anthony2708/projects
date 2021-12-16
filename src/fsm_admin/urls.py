from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home', views.index, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('createteam', views.createteam, name='createteam'),
    path('tournaments', views.allTournaments, name='tournaments'),
    path('createtournaments', views.createtournaments,
         name='createtournaments'),
    path('tournament/<str:pk>', views.tournament,
         name='tournament'),  # view tournament
    path('search', views.search, name='search'),
    path('edittournament/<str:pk>', views.edittournament,
         name='edittournament'),  # edit tournament
    path('jointournament/<str:pk>', views.jointournament,
         name='jointournament')
]
