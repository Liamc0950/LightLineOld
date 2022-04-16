from django.urls import path

from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    #DATABASE
    path('', views.followspotsView, name='followspots'),

    #followspot delete buttons
    path('followspots/deleteCue/<int:cueID>', views.cueDeleteFollowspot, name='deleteCue'),
    path('followspots/deleteAction/<int:actionID>', views.actionDelete, name='deleteAction'),

    #followspot app live update
    path('followspots/updateAction/', views.updateAction, name='updateAction'),
    #followspot app modals
    path('followspots/createCue/', views.CueCreateViewFS.as_view(), name='createCue'),
    path('followspots/createAction/', views.ActionCreateView.as_view(), name='createAction'),
    path('followspots/createFocus/', views.FocusCreateView.as_view(), name='createFocus'),

]
