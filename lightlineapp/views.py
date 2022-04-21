# -*- coding: utf-8 -*-

#Boilerplate
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy

from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView

from .models import *
from .forms import *


#User Auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

#Modals
from bootstrap_modal_forms.generic import BSModalCreateView


#PDF
from lightlineapp.print import PDF_Printer
from io import BytesIO

#CSV
import csv




def cueDeleteFollowspot(request, cueID):
    cue = Cue.objects.get(id=cueID)
    cue.delete()
    return HttpResponseRedirect('/lightlineapp/followspots')

def cueDeleteCueList(request, cueID):
    cue = Cue.objects.get(id=cueID)
    cue.delete()
    return HttpResponseRedirect('/lightlineapp/cueList')


def cueCreateCueList(request, lastCueNum):

    Cue.objects.createNext(lastCueNum)
    
    return HttpResponseRedirect('/lightlineapp/cueList')


def actionDelete(request, actionID):
    action = Action.objects.get(id=actionID)
    action.delete()
    return HttpResponseRedirect('/lightlineapp/followspots')


#IMPORT CSV FROM LIGHTWRIGHT
def importLWCSV(request):
    activeProject = Project.objects.get(lightingDesigner= request.user.profile, active=True)
    csv = open('lightlineapp/testLWExport.csv', 'r')  

    Instrument.addInstrumentsFromCSV(csv, activeProject)

    csv.close() 

    return HttpResponseRedirect('/lightlineapp/database')







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




#PrintPDF
def printPDF(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="My Users.pdf"'

    buffer = BytesIO()

    report = PDF_Printer(buffer, 'Letter', request)
    pdf = report.printTest()

    response.write(pdf)
    return response


#Update Cue 
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
    if type == "cueTime":
        cue.cueTime = value
    if type == "cueDescription":
        cue.cueDescription = value

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


@login_required
#Project settings view
def projectSettings(request):
    #try to get the active project, then get all the cues in cueList linked to active project
    try:
        activeProject = Project.objects.get(lightingDesigner=request.user.profile, active=True)
        #get all cues where cueList's project is the active project and cueList is active
        activeCues = Cue.objects.order_by('eosCueNumber').filter(cueList__project = activeProject, cueList__active = True)
        projectCueLists = CueList.objects.filter(project = activeProject)
        activeCueList = CueList.objects.get(project = activeProject, active = True)
        projectOperators = Operator.objects.filter(project = activeProject)
        projectFocus = Focus.objects.filter(project = activeProject)
        opList = Operator.objects.filter(project = activeProject)
        spotList = Followspot.objects.filter(project = activeProject)
        colorList = ColorFlag.objects.filter(project = activeProject).order_by('index')
        shots = Shot.objects.filter(project = activeProject)
        focusList = Focus.objects.filter(project = activeProject)
        projectColorFlags = ColorFlag.objects.filter(project = activeProject)
        cueLists = CueList.objects.filter(project = activeProject)
        #shareNodes = ShareNode.objects.filter(project = activeProject)
    #if no active project, set cueList to empty queryset
    except:
        activeProject = Project.objects.none()
        cueList = Cue.objects.none()

    projects = Project.objects.filter(lightingDesigner=request.user.profile)
    template = loader.get_template('projectSettings.html')
    context = {
        'cueList': activeCues,
        'cueLists' : cueLists,
        'activeProject': activeProject,
        'projects' : projects,
        'projectCueLists' : projectCueLists,
        'activeCueList' : activeCueList,
        'projectOperators' : projectOperators,
        'projectFocus' : projectFocus,
        'shots' : shots,
        'focusList' : focusList,
        'projectColorFlags' : projectColorFlags,
        'opList' : opList,
        'spotList' : spotList,
        'colorList' : colorList,
        'colors' : Color.objects.all(),
        #'shareNodes' : shareNodes,
    }

    return HttpResponse(template.render(context, request))
