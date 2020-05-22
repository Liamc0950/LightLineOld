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
    path('followspots/createCue/', views.CueCreateView.as_view(), name='createCue'),
    path('followspots/createAction/', views.ActionCreateView.as_view(), name='createAction'),
    path('followspots/createFocus/', views.FocusCreateView.as_view(), name='createFocus'),
    #project settings modals
    path('projectSettings/createOperator/', views.OperatorCreateView.as_view(), name='createOperator'),
    path('projectSettings/createFollowspot/', views.FollowspotCreateView.as_view(), name='createFollowspot'),
    path('projectSettings/createColorFlag/', views.ColorFlagCreateView.as_view(), name='createColorFlag'),
    #path('projectSettings/createShareNode/', views.ShareNodeCreateView.as_view(), name='createShareNode'),
    #followspot app live update
    path('followspots/updateCue/', views.updateCue, name='updateCue'),
    path('followspots/updateAction/', views.updateAction, name='updateAction'),
    #project creation
    path('createProject/', views.ProjectCreateView.as_view(), name='createProject'),
    #project settings
    path('projectSettings/', views.projectSettings, name='projectSettings'),
    #project settings live update
    path('projectSettings/updateFollowspot/', views.updateFollowspot, name='updateFollowspot'),
    path('projectSettings/updateOperator/', views.updateOperator, name='updateOperator'),
    path('projectSettings/updateColorFlag/', views.updateColorFlag, name='updateColorFlag'),
    #path('projectSettings/updateShareNode/', views.updateShareNode, name='updateShareNode'),
    #project selection
    path('switchActiveProject/', views.switchActiveProject, name='switchActiveProject'),
    #cueList Selection
    path('switchActiveCueList/', views.switchActiveCueList, name='switchActiveCueLis'),
    #followspot delete buttons
    path('followspots/deleteCue/<int:cueID>', views.CueDelete, name='deleteCue'),
    path('followspots/deleteAction/<int:actionID>', views.actionDelete, name='deleteAction'),

]
