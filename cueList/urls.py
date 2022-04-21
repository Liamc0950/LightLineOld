from django.urls import path

from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    #ROOT
    path('', views.cueListView, name='cueList'),


    #cueList app live update
    path('updateCue/', views.updateCue, name='updateCue'),
    #cueList Selection
    path('switchActiveCueList/', views.switchActiveCueList, name='switchActiveCueLis'),
    #cueList delete buttons
    path('deleteCue/<int:cueID>', views.cueDeleteCueList, name='deleteCue'),
    #cueList add cue
    path('addCue/', views.CueCreateView.as_view(), name='addCue'),
    path('addNextCue/<int:lastCueNum>', views.cueCreateCueList, name='addNextCue'),
    #cueList add Header
    path('addHeader/', views.HeaderCreateView.as_view(), name='addHeader'),
    #CueList PrintPDF
    path('printPDF/', views.printPDF, name='printPDF'),
    #CueList Export Eos CSV
    path('exportEosCSV/<int:activeCueListID>', views.exportEosCSV, name='exportEosCSV'),
    #CueList Create CueList
    path('createCueList', views.CueListCreateView.as_view(), name='createCueList'),
    #CueList Create Cue
    path('createCueList', views.CueListCreateView.as_view(), name='createCueList'),
    #Page View Create CueList - for project setup sequence page view
    path('createCueListPageView', views.CueListCreateViewPageView.as_view(), name='createCueListPageView')

]
