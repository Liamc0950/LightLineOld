# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy

from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from bootstrap_modal_forms.generic import BSModalCreateView

from django.views.generic.edit import CreateView

from .models import *
from .forms import *


class ProjectCreateView(CreateView):
    template_name = 'createProject.html'
    form_class = ProjectCreateForm

    success_message = 'Success: Project was created.'
    success_url = reverse_lazy('followspots')

    def get_initial(self, *args, **kwargs):
        #deactivate other projects
        userProjects = Project.objects.filter(lightingDesigner= self.request.user.profile, active=True)
        for project in userProjects:
            project.active = False
            project.save()
        initial = super(ProjectCreateView, self).get_initial(**kwargs)
        initial['lightingDesigner'] = self.request.user.profile
        initial['active'] = True
        return initial



def switchActiveProject(request):
    if request.method == "POST":
        #deactivate other projects
        userProjects = Project.objects.filter(lightingDesigner=request.user.profile, active=True)
        for project in userProjects:
            project.active = False
            project.save()
        #Activate selected project
        projID = request.POST.get('proj', '/')
        proj = Project.objects.get(id=projID)
        proj.active = True;
        proj.save()

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

def switchActiveCueList(request):
    if request.method == "POST":
        #deactivate other projects
        activeProject = Project.objects.get(lightingDesigner=request.user.profile, active=True)
        projectCueLists = CueList.objects.filter(project = activeProject)

        for cueList in projectCueLists:
            cueList.active = False
            cueList.save()
        #Activate selected project
        cueListID = request.POST.get('cueList', '/')
        cueList = CueList.objects.get(id=cueListID)
        cueList.active = True;
        cueList.save()

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('createProject')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



#Landing page View
def index(request):
    template = loader.get_template('index.html')
    context={}
    return HttpResponse(template.render(context, request))

@login_required
#Notes feature view
def notes(request):
    template = loader.get_template('notes.html')
    context={}
    return HttpResponse(template.render(context, request))

@login_required
#CueList feature view    
def cueList(request):
    template = loader.get_template('cueList.html')
    context={}
    return HttpResponse(template.render(context, request))

@login_required
#Database feature view
def database(request):
    template = loader.get_template('database.html')
    context={}
    return HttpResponse(template.render(context, request))

@login_required
#Followspots feature view
def followspots(request):
    #try to get the active project, then get all the cues in cueList linked to active project
    try:
        activeProject = Project.objects.get(lightingDesigner=request.user.profile, active=True)
        #get all cues where cueList's project is the active project and cueList is active
        activeCues = SpotCue.objects.order_by('eosCueNumber').filter(cueList__project = activeProject, cueList__active = True)
        projectCueLists = CueList.objects.filter(project = activeProject)
        activeCueList = CueList.objects.get(project = activeProject, active = True)
    #if no active project, set spotCueList to empty queryset
    except:
        activeProject = Project.objects.none()
        spotCueList = SpotCue.objects.none()

    projects = Project.objects.filter(lightingDesigner=request.user.profile)
    template = loader.get_template('followspots.html')
    context = {
        'spotCueList': activeCues,
        'activeProject': activeProject,
        'projects' : projects,
        'projectCueLists' : projectCueLists,
        'activeCueList' : activeCueList
    }

    return HttpResponse(template.render(context, request))

#Followspot Modal Views
class SpotCueCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createSpotCue.html'
    form_class = SpotCueForm
    success_message = 'Success: Spot Cue was created.'
    success_url = reverse_lazy('followspots')

    def get_initial(self, *args, **kwargs):
        initial = super(SpotCueCreateView, self).get_initial(**kwargs)
        activeProject = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        activeCueList = CueList.objects.get(project = activeProject, active = True)
        initial['project'] = activeProject
        initial['cueList'] = activeCueList

        return initial



class ActionCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createAction.html'
    form_class = ActionForm
    success_message = 'Success: Action was created.'
    success_url = reverse_lazy('followspots')

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(ActionCreateView, self).get_form_kwargs(*args, **kwargs)
        activeProject = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        activeCueList = CueList.objects.get(project = activeProject, active = True)
        form_kwargs['project'] = activeProject
        form_kwargs['activeCueList'] = activeCueList
        return form_kwargs


class FocusCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createFocus.html'
    form_class = FocusForm
    success_message = 'Success: Focus was added.'
    success_url = reverse_lazy('followspots')

    def get_initial(self, *args, **kwargs):
        initial = super(FocusCreateView, self).get_initial(**kwargs)
        initial['project'] = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        print("PROJECT FOR FOCUS ADD")
        print( Project.objects.get(lightingDesigner=self.request.user.profile, active=True))
        return initial


#Followspot update SpotCue 
@csrf_exempt
def updateSpotCue(request):
    id=request.POST.get('id','')
    type=request.POST.get('type','')
    value=request.POST.get('value','')
    cue=SpotCue.objects.get(id=id)
    if type=="eosCueNumber":
        cue.eosCueNumber=value

    if type == "cueLabel":
        cue.cueLabel = value

    if type == "pageNumber":
        cue.pageNumber = value
    cue.save()
    return JsonResponse({"success":"Updated SpotCue"})

#Followspot update Action 
@csrf_exempt
def updateAction(request):
    id=request.POST.get('id','')
    type=request.POST.get('type','')
    value=request.POST.get('value','')
    action=Action.objects.get(id=id)
    print("ACTION TO BE UPDATED")
    print(action)
    if type=="eosCueNumber":
        action.eosCueNumber=value

    if type == "operator":
        action.operator = value

    if type == "focus":
        action.focus = value

    if type == "shotType":
        action.shotType = value

    if type == "intensity":
        action.intensity = value

    if type == "colorFlag":
        action.colorFlag = value

    if type == "fadeTime":
        action.fadeTime = value
    action.save()
    return JsonResponse({"success":"Updated Action"})
