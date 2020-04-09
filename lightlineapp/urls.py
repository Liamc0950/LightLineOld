from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('followspots/', views.followspots, name='followspots'),
    path('cueList/', views.cueList, name='cueList'),
    path('database/', views.database, name='database'),
    path('notes/', views.notes, name='notes'),
    path('followspots/createSpotCue/', views.SpotCueCreateView.as_view(), name='createSpotCue'),
    path('followspots/createAction/', views.ActionCreateView.as_view(), name='createAction'),
    path('followspots/createOperator/', views.OperatorCreateView.as_view(), name='createOperator'),
    path('followspots/createFocus/', views.FocusCreateView.as_view(), name='createFocus'),
    path('followspots/updateColorFlags/', views.FocusCreateView.as_view(), name='updateColorFlags')
]
