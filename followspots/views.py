#Boilerplate
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView

from django.views.decorators.csrf import csrf_exempt


from .models import *

from projectManager.models import *
from cueList.models import *
from landing.models import Profile
from .forms import *


#Modals
from bootstrap_modal_forms.generic import BSModalCreateView


@login_required
#Followspots feature view
def followspotsView(request):
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
        #get all operators linked to activeProject
        projectOperators = Operator.objects.filter(project = activeProject)
    except:
        projectOperators = None 
    try:
        #Get all focus linked to activeProject
        projectFocus = Focus.objects.filter(project = activeProject)
    except:
        projectFocus = None
    try:
        #Get all shots linked to activeProject
        shots = Shot.objects.all()
    except:
        shots = None
    try:
        #Get all colorFlags linked to activeProject
        projectColorFlags = ColorFlag.objects.filter(project = activeProject)
    except:
        projectColorFlags = None


    projects = Project.objects.filter(lightingDesigner=request.user.profile)
    template = loader.get_template('followspots/followspots.html')
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

    return HttpResponse(template.render(context, request))


#Create Focus
class FocusCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createFocus.html'
    form_class = FocusForm
    success_message = 'Success: Focus was added.'
    success_url = reverse_lazy('followspots')

    def get_initial(self, *args, **kwargs):
        initial = super(FocusCreateView, self).get_initial(**kwargs)
        initial['project'] = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        return initial

#Create Action
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


#Delete Cue - deletes given cue (designated by parent of delete button)
def cueDeleteFollowspot(request, cueID):
    cue = Cue.objects.get(id=cueID)
    cue.delete()
    return HttpResponseRedirect('/followspots')

# Delete Action - deletes given followspot action (designated by parent of delete button)
def actionDelete(request, actionID):
    action = Action.objects.get(id=actionID)
    action.delete()
    return HttpResponseRedirect('/followspots')


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

