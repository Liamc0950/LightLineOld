from django.urls import path

from . import views


urlpatterns = [

    #NOTES
    path('', views.notes, name='notes'),

]
