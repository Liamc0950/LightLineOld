#Boilerplate
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .models import *
from projectManager.models import *
from cueList.models import *
from landing.models import Profile

# Create your views here.

@login_required
#Notes feature view
def notes(request):

    #try to get the active project
    try:
        activeProject = Project.objects.get(lightingDesigner=request.user.profile, active=True)
    except:
        activeProject = None
    #try to get the active cueList and cues
    try:
        activeCueList = CueList.objects.get(project = activeProject, active = True)
        #get all cues where cueList's project is the activeProject and cueList is active
        activeCues = Cue.objects.order_by('eosCueNumber').filter(cueList__project = activeProject, cueList__active = True)
        #get all activeProject cue Lists
        projectCueLists = CueList.objects.filter(project = activeProject)
    except:
        activeCueList = None
        activeCues = None
        projectCueLists = None

    try:
        projects = Project.objects.filter(lightingDesigner=request.user.profile)
    except:
        projects = None

    template = loader.get_template('notes/notes.html')
    context = {
        'cueList': activeCues,
        'activeProject': activeProject,
        'projects' : projects,
        'projectCueLists' : projectCueLists,
        'activeCueList' : activeCueList,
    }
    return HttpResponse(template.render(context, request))
