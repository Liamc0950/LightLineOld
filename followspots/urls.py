from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('createSpotCue/', views.SpotCueCreateView.as_view(), name='createSpotCue'),
    path('createAction/', views.ActionCreateView.as_view(), name='createAction'),
    path('createOperator/', views.OperatorCreateView.as_view(), name='createOperator'),
    path('createFocus/', views.FocusCreateView.as_view(), name='createFocus')
]
