from django.urls import path

from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    #landing page
    path('', views.index, name='index'),
    #login
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #
    path('signup/', views.signup, name='signup'),
    #app pages
    path('followspots/', views.followspots, name='followspots'),
    path('cueList/', views.cueList, name='cueList'),
    path('database/', views.database, name='database'),
    path('notes/', views.notes, name='notes'),
    #followspot app modals
    path('followspots/createSpotCue/', views.SpotCueCreateView.as_view(), name='createSpotCue'),
    path('followspots/createAction/', views.ActionCreateView.as_view(), name='createAction'),
    path('followspots/createFocus/', views.FocusCreateView.as_view(), name='createFocus'),
    #followspot app live update
    path('followspots/updateSpotCue/', views.updateSpotCue, name='updateSpotCue'),
    path('followspots/updateAction/', views.updateAction, name='updateAction'),
    #project creation
    path('createProject/', views.ProjectCreateView.as_view(), name='createProject'),
    #project selection
    path('switchActiveProject/', views.switchActiveProject, name='switchActiveProject'),
    #cueList Selection
    path('switchActiveCueList/', views.switchActiveCueList, name='switchActiveCueLis'),
]
