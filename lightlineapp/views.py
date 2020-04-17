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

def CueDelete(request, cueID):
    cue = Cue.objects.get(id=cueID)
    cue.delete()
    return HttpResponseRedirect('/lightlineapp/followspots')

def actionDelete(request, actionID):
    action = Action.objects.get(id=actionID)
    action.delete()
    return HttpResponseRedirect('/lightlineapp/followspots')


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
        activeCues = Cue.objects.order_by('eosCueNumber').filter(cueList__project = activeProject, cueList__active = True)
        projectCueLists = CueList.objects.filter(project = activeProject)
        activeCueList = CueList.objects.get(project = activeProject, active = True)
        projectOperators = Operator.objects.filter(project = activeProject)
        projectFocus = Focus.objects.filter(project = activeProject)
        shots = Shot.objects.all()
        projectColorFlags = ColorFlag.objects.filter(project = activeProject)
    #if no active project, set cueList to empty queryset
    except:
        activeProject = Project.objects.none()
        cueList = Cue.objects.none()

    projects = Project.objects.filter(lightingDesigner=request.user.profile)
    template = loader.get_template('followspots.html')
    context = {
        'cueList': activeCues,
        'activeProject': activeProject,
        'projects' : projects,
        'projectCueLists' : projectCueLists,
        'activeCueList' : activeCueList,
        'projectOperators' : projectOperators,
        'projectFocus' : projectFocus,
        'shots' : shots,
        'projectColorFlags' : projectColorFlags,
    }

    csv = open('lightlineapp/roscolux.csv', 'r')  
    for line in csv:
        print(line)
        line =  line.split(',')
        print("Hello" + str(len(line[0])) + "there")
        if len(line[0]) == 1:
            pass
        else: 
            color = Color()  
            color.colorName = line[1]
            color.colorCode = line[0]  
            color.colorHex = line[2]
            color.save()  

    csv.close() 



    return HttpResponse(template.render(context, request))

#Followspot Modal Views
class CueCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createCue.html'
    form_class = CueForm
    success_message = 'Success: Spot Cue was created.'
    success_url = reverse_lazy('followspots')

    def get_initial(self, *args, **kwargs):
        initial = super(CueCreateView, self).get_initial(**kwargs)
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


#Followspot update Cue 
@csrf_exempt
def updateCue(request):
    id=request.POST.get('id','')
    type=request.POST.get('type','')
    value=request.POST.get('value','')
    cue=Cue.objects.get(id=id)
    if type=="eosCueNumber":
        cue.eosCueNumber=value

    if type == "cueLabel":
        cue.cueLabel = value

    if type == "pageNumber":
        cue.pageNumber = value
    cue.save()
    return JsonResponse({"success":"Updated Cue"})

#Followspot update Action 
@csrf_exempt
def updateAction(request):
    id=request.POST.get('id','')
    type=request.POST.get('type','')
    value=request.POST.get('value','')
    action=Action.objects.get(id=id)
    choiceID = request.POST.get('choiceID', '')
    if type=="eosCueNumber":
        #if the number specified is a cue in the cueList, then update it
        #If not, add a new cue
        activeProject = Project.objects.get(lightingDesigner=request.user.profile, active=True)
        #get all cues where cueList's project is the active project and cueList is active
        activeCues = Cue.objects.order_by('eosCueNumber').filter(cueList__project = activeProject, cueList__active = True)
        activeCueList = CueList.objects.get(project = activeProject, active = True)

        try:
            cue = activeCues.get(eosCueNumber = value)
            action.cue = cue
        except:
            newCue = Cue.objects.create(cueList=activeCueList, eosCueNumber=value)
            action.cue = newCue

    if type == "operator":
        action.operator = Operator.objects.get(id=value)

    if type == "focus":
        action.focus = Focus.objects.get(id=value)

    if type == "shotType":
        action.shotType = Shot.objects.get(id=value)

    if type == "intensity":
        action.intensity = value

    if type == "colorFlag":
        action.colorFlag = ColorFlag.objects.get(id=value)

    if type == "fadeTime":
        action.fadeTime = value
    action.save()
    return JsonResponse({"success":"Updated Action"})
