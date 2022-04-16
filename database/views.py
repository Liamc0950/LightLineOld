
#Boilerplate
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView

from .models import *

from lightlineapp.models import *

@login_required
#Database feature view
def databaseView(request):
    #try to get the active project, then get all the cues in cueList linked to active project
    try:
        activeProject = Project.objects.get(lightingDesigner=request.user.profile, active=True)
        instrumentList = Instrument.objects.filter(project=activeProject)
    #if no active project, set cueList to empty queryset
    except:
        activeProject = Project.objects.none()
        instrumentList = Instrument.objects.none()

    print("DATABASE")

    context={
        'activeProject': activeProject,
        'instrumentList' : instrumentList,
    }

    return render(request, "database/database.html", context)

