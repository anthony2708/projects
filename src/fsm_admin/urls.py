from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home', views.index, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('editprofile', views.editprofile, name='editprofile'),
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
         name='jointournament'),  # join a tournament
    path('deletetournament/<str:pk>', views.deletetournament,
         name='deletetournament'),  # delete tournament
    path('matcharrange/<str:pk>', views.match_arrange, name='match_arrange'),
    path('matchupdate/<str:tourpk>/<str:matchpk>',
         views.matchupdate, name='matchupdate'),
    path('matcharrangeresult/<str:pk>',
         views.match_arrange_result, name='match_arrange_result')
]
