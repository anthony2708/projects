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
         views.match_arrange_result, name='match_arrange_result'),


    # Admin site
    path('admin_site', views.admin_site, name='admin_site'),
    path('admin_site/signin', views.admin_signin, name='admin_signin'),
    path('admin_site/signout', views.admin_signout, name='admin_signout'),
    path('admin_site/<int:tabActive>', views.admin_site, name='admin_site'),
    path('admin_site/1/create_tournament',
         views.admin_create_tournament, name='admin_create_tournament'),
    path('admin_site/1/create_tournament/back',
         views.admin_create_tournament_back,
         name='admin_create_tournament_back'),
    path('admin_site/1/search', views.admin_search, name='admin_search'),
    path('admin_site/1/tournament/<int:pk>', views.admin_view_tournament, name='admin_view_tournament'),
    path('admin_site/1/tournament/<int:pk>/update', views.admin_update_tournament, name='admin_update_tournament'),
    path('admin_site/1/tournament/<int:pk>/update/back', views.admin_update_tournament_back, name='admin_update_tournament_back'),
    path('admin_site/1/tournament/<int:pk>/delete', views.admin_delete_tournament, name='admin_delete_tournament'),
    path('admin_site/1/tournament/<int:pk>/match_arrange', views.admin_match_arrange, name='admin_match_arrange'),
    path('admin_site/1/user/<int:pk>', views.admin_view_user, name='admin_view_user'),
    path('admin_site/1/user/<int:pk>/delete', views.admin_delete_user, name='admin_delete_user'),

    
    
]
