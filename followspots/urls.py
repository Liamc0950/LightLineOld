from django.urls import path

from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    #DATABASE
    path('', views.followspotsView, name='followspots'),

    #followspot delete buttons
    path('deleteCue/<int:cueID>', views.cueDeleteFollowspot, name='deleteCue'),
    path('deleteAction/<int:actionID>', views.actionDelete, name='deleteAction'),

    #followspot app live update
    path('updateAction/', views.updateAction, name='updateAction'),
    #followspot app modals
    path('createCue/', views.CueCreateViewFS.as_view(), name='createCue'),
    path('createAction/', views.ActionCreateView.as_view(), name='createAction'),
    path('createFocus/', views.FocusCreateView.as_view(), name='createFocus'),

]
