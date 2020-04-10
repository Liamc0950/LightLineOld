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
    path('followspots/createOperator/', views.OperatorCreateView.as_view(), name='createOperator'),
    path('followspots/createFocus/', views.FocusCreateView.as_view(), name='createFocus'),
    path('followspots/updateColorFlags/', views.FocusCreateView.as_view(), name='updateColorFlags')
]
