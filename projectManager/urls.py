from django.urls import path

from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    #project creation
    path('createProject/', views.ProjectCreateView.as_view(), name='createProject'),
    #project settings
    path('projectSettings/', views.projectSettings, name='projectSettings'),
    #project settings live update
    path('projectSettings/updateFollowspot/', views.updateFollowspot, name='updateFollowspot'),
    path('projectSettings/updateOperator/', views.updateOperator, name='updateOperator'),
    path('projectSettings/updateColorFlag/', views.updateColorFlag, name='updateColorFlag'),
    
    #project settings modals
    path('projectSettings/createOperator/', views.OperatorCreateView.as_view(), name='createOperator'),
    path('projectSettings/createFollowspot/', views.FollowspotCreateView.as_view(), name='createFollowspot'),
    path('projectSettings/createColorFlag/', views.ColorFlagCreateView.as_view(), name='createColorFlag'),
    path('projectSettings/createShot/', views.ShotCreateView.as_view(), name='createShot'),
    path('projectSettings/createFocus/', views.FocusCreateView.as_view(), name='createFocus'),

    #Settings Delete Buttons
    path('projectSettings/deleteFocus/<int:focusID>', views.focusDelete, name='deleteFocus'),


]
