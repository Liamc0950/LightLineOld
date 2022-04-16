from django.urls import path

from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    #BASIC SITE STRUCTURE

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

    #FOLLOWSPOTS

    #followspot app modals
    path('followspots/createCue/', views.CueCreateViewFS.as_view(), name='createCue'),
    path('followspots/createAction/', views.ActionCreateView.as_view(), name='createAction'),
    path('followspots/createFocus/', views.FocusCreateView.as_view(), name='createFocus'),

    #followspot app live update
    path('followspots/updateCue/', views.updateCue, name='updateCue'),
    path('followspots/updateAction/', views.updateAction, name='updateAction'),
    #cueList app live update
    path('cueList/updateCue/', views.updateCue, name='updateCue'),

    #PROJECT CREATION AND SETTINGS

    #project creation
    path('createProject/', views.ProjectCreateView.as_view(), name='createProject'),
    #project settings
    path('projectSettings/', views.projectSettings, name='projectSettings'),
    #project settings live update
    path('projectSettings/updateFollowspot/', views.updateFollowspot, name='updateFollowspot'),
    path('projectSettings/updateOperator/', views.updateOperator, name='updateOperator'),
    path('projectSettings/updateColorFlag/', views.updateColorFlag, name='updateColorFlag'),
    #project selection
    path('switchActiveProject/', views.switchActiveProject, name='switchActiveProject'),
    
    #project settings modals
    path('projectSettings/createOperator/', views.OperatorCreateView.as_view(), name='createOperator'),
    path('projectSettings/createFollowspot/', views.FollowspotCreateView.as_view(), name='createFollowspot'),
    path('projectSettings/createColorFlag/', views.ColorFlagCreateView.as_view(), name='createColorFlag'),
    path('projectSettings/createShot/', views.ShotCreateView.as_view(), name='createShot'),
    path('projectSettings/createFocus/', views.FocusCreateView.as_view(), name='createFocus'),


    #CUE LIST

    #cueList Selection
    path('switchActiveCueList/', views.switchActiveCueList, name='switchActiveCueLis'),
    #followspot delete buttons
    path('followspots/deleteCue/<int:cueID>', views.cueDeleteFollowspot, name='deleteCue'),
    path('followspots/deleteAction/<int:actionID>', views.actionDelete, name='deleteAction'),
    #Settings Delete Buttons
    path('projectSettings/deleteFocus/<int:focusID>', views.focusDelete, name='deleteFocus'),
    #cueList delete buttons
    path('cueList/deleteCue/<int:cueID>', views.cueDeleteCueList, name='deleteCue'),
    #cueList add cue
    path('cueList/addCue/', views.CueCreateView.as_view(), name='addCue'),
    path('cueList/addNextCue/<int:lastCueNum>', views.cueCreateCueList, name='addNextCue'),
    #cueList add Header
    path('cueList/addHeader/', views.HeaderCreateView.as_view(), name='addHeader'),
    #CueList PrintPDF
    path('cueList/printPDF/', views.printPDF, name='printPDF'),
    #CueList Export Eos CSV
    path('cueList/exportEosCSV/<int:activeCueListID>', views.exportEosCSV, name='exportEosCSV'),
    #CueList Create CueList
    path('cueList/createCueList', views.CueListCreateView.as_view(), name='createCueList'),

    #DATABASE
    path('database/importLWCSV/', views.importLWCSV, name='importLWCSV'),

]
