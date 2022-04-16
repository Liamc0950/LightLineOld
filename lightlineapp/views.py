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


def focusDelete(request, focusID):
    focus = Focus.objects.get(id=focusID)
    focus.delete()
    return HttpResponseRedirect('/lightlineapp/projectSettings')


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


def exportEosCSV(request, activeCueListID):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="cueListForEos.csv"'},
    )

    activeCueList = CueList.objects.get(id=activeCueListID)

    cues = Cue.objects.filter(cueList=activeCueList)

    writer = csv.writer(response)
    #START TARGET CREATION
    writer.writerow(['START_TARGETS'])
    #WRITE HEADERS
    writer.writerow(['TARGET_TYPE','TARGET_TYPE_AS_TEXT','TARGET_LIST_NUMBER','TARGET_ID','TARGET_DCID','PART_NUMBER','LABEL','TIME_DATA','UP_DELAY','DOWN_TIME','DOWN_DELAY','FOCUS_TIME','FOCUS_DELAY','COLOR_TIME','COLOR_DELAY','BEAM_TIME','BEAM_DELAY','DURATION','MARK','BLOCK','ASSERT','ALL_FADE','PREHEAT','FOLLOW','LINK','LOOP','CURVE','RATE','EXTERNAL_LINKS','EFFECTS','MODE','CUE_NOTES','SCENE_TEXT','SCENE_END'])
    #START CUE LIST
    writer.writerow([15,'Cue_List','',activeCueList.cueListNumber,'','',activeCueList.listName,'','','','','','','','','','','','','','','','','','','','','','','','','','',''])

    #WRITE CUES
    for cue in cues:
        writer.writerow([1,'Cue',activeCueList.cueListNumber,cue.eosCueNumber,'','',cue.cueLabel,cue.cueTime,'','','','','','','','','',cue.cueTime,'','','','','','','','','','','','','','',cue.getHeader(),''])

    #END CUE LIST
    writer.writerow([15,'Cue_List','',activeCueList.cueListNumber,'','',activeCueList.listName,'','','','','','','','','','','','','','','','','','','','','','','','','','',''])


    
    #END TARGET CREATION
    writer.writerow(['END_TARGETS'])

    return response


class ProjectCreateView(CreateView):
    template_name = 'createProject.html'
    form_class = ProjectCreateForm
    success_message = 'Success: Project was created.'
    success_url = reverse_lazy('projectSettings')

    def get_initial(self, *args, **kwargs):
        #deactivate other projects
        initial = super(ProjectCreateView, self).get_initial(**kwargs)
        initial['lightingDesigner'] = self.request.user.profile
        initial['active'] = True
        return initial

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # Sets all projects to active=False 
        userProjects = Project.objects.filter(lightingDesigner= self.request.user.profile, active=True)
        for project in userProjects:
            project.active = False
            project.save()
        return super().form_valid(form)


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



@login_required
#CueList feature view    
def cueList(request):
    #try to get the active project, then get all the cues in cueList linked to active project
    try:
        activeProject = Project.objects.get(lightingDesigner=request.user.profile, active=True)
        #get all cues where cueList's project is the active project and cueList is active
        activeCues = Cue.objects.order_by('eosCueNumber').filter(cueList__project = activeProject, cueList__active = True)
        projectCueLists = CueList.objects.filter(project = activeProject)
        activeCueList = CueList.objects.get(project = activeProject, active = True)
    #if no active project, set cueList to empty queryset
    except:
        activeProject = Project.objects.none()
        cueList = Cue.objects.none()

    projects = Project.objects.filter(lightingDesigner=request.user.profile)
    template = loader.get_template('cueList.html')
    context = {
        'cueList': activeCues,
        'activeProject': activeProject,
        'projects' : projects,
        'projectCueLists' : projectCueLists,
        'activeCueList' : activeCueList,
    }

    return HttpResponse(template.render(context, request))

@login_required
#Database feature view
def database(request):

    print("lightlineapp")

    #try to get the active project, then get all the cues in cueList linked to active project
    try:
        activeProject = Project.objects.get(lightingDesigner=request.user.profile, active=True)
        instrumentList = Instrument.objects.filter(project=activeProject)
    #if no active project, set cueList to empty queryset
    except:
        activeProject = Project.objects.none()
        instrumentList = Instrument.objects.none()


    template = loader.get_template('database.html')
    context={
        'activeProject': activeProject,
        'instrumentList' : instrumentList,
    }
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

#Followspot Modal Views
class CueCreateViewFS(BSModalCreateView):
    template_name = 'lightlineapp/createCue.html'
    form_class = CueForm
    success_message = 'Success: Cue was created.'
    success_url = reverse_lazy('followspots')

    def get_initial(self, *args, **kwargs):
        initial = super(CueCreateView, self).get_initial(**kwargs)
        activeProject = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        activeCueList = CueList.objects.get(project = activeProject, active = True)
        initial['project'] = activeProject
        initial['cueList'] = activeCueList

        return initial

#CueList Create CueList
class CueListCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createCueList.html'
    form_class = CueForm
    success_message = 'Success: Cue was created.'
    success_url = reverse_lazy('cueList')

    def get_initial(self, *args, **kwargs):
        initial = super(CueListCreateView, self).get_initial(**kwargs)
        activeProject = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        activeCueList = CueList.objects.get(project = activeProject, active = True)
        initial['project'] = activeProject
        initial['cueList'] = activeCueList

        return initial


#CueList Add Cue
class CueCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createCue.html'
    form_class = CueForm
    success_message = 'Success: Cue was created.'
    success_url = reverse_lazy('cueList')

    def get_initial(self, *args, **kwargs):
        initial = super(CueCreateView, self).get_initial(**kwargs)
        activeProject = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        activeCueList = CueList.objects.get(project = activeProject, active = True)
        initial['project'] = activeProject
        initial['cueList'] = activeCueList

        return initial

#CueList Add Header
class HeaderCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createHeader.html'
    form_class = HeaderForm
    success_message = 'Success: Header was created.'
    success_url = reverse_lazy('cueList')

    def get_initial(self, *args, **kwargs):
        initial = super(HeaderCreateView, self).get_initial(**kwargs)
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
        return initial

class OperatorCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createOperator.html'
    form_class = OperatorForm
    success_message = 'Success: Operator was added.'
    success_url = reverse_lazy('projectSettings')

    def get_initial(self, *args, **kwargs):
        initial = super(OperatorCreateView, self).get_initial(**kwargs)
        initial['project'] = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(OperatorCreateView, self).get_form_kwargs(*args, **kwargs)
        activeProject = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        form_kwargs['project'] = activeProject
        return form_kwargs

class FollowspotCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createFollowspot.html'
    form_class = FollowspotForm
    success_message = 'Success: Followspot was added.'
    success_url = reverse_lazy('projectSettings')

    def get_initial(self, *args, **kwargs):
        initial = super(FollowspotCreateView, self).get_initial(**kwargs)
        initial['project'] = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        return initial

class ColorFlagCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createColorFlag.html'
    form_class = ColorFlagForm
    success_message = 'Success: Color Flag was added.'
    success_url = reverse_lazy('projectSettings')

    def get_initial(self, *args, **kwargs):
        initial = super(ColorFlagCreateView, self).get_initial(**kwargs)
        initial['project'] = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        return initial


class ShotCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createShot.html'
    form_class = ShotForm
    success_message = 'Success: Shot was added.'
    success_url = reverse_lazy('projectSettings')

    def get_initial(self, *args, **kwargs):
        initial = super(ShotCreateView, self).get_initial(**kwargs)
        initial['project'] = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        return initial

class FocusCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createFocus.html'
    form_class = FocusForm
    success_message = 'Success: Focus was added.'
    success_url = reverse_lazy('projectSettings')

    def get_initial(self, *args, **kwargs):
        initial = super(FocusCreateView, self).get_initial(**kwargs)
        initial['project'] = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        return initial


""" class ShareNodeCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createShareNode.html'
    form_class = ShareNodeForm
    success_message = 'Success: ShareNode was added.'
    success_url = reverse_lazy('projectSettings')

    def get_initial(self, *args, **kwargs):
        initial = super(ShareNodeCreateView, self).get_initial(**kwargs)
        initial['project'] = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        return initial
 """
""" #Project Settings - ShareNode update
@csrf_exempt
def updateShareNode(request):
    id=request.POST.get('id','')
    type=request.POST.get('type','')
    value=request.POST.get('value','')
    node=ShareNode.objects.get(id=id)
    if type=="role":
        node.role=value
        print("ROLE UPDATED")
    node.save()
    return JsonResponse({"success":"Updated share node"})
 """
#Project Settings - Followspot update
@csrf_exempt
def updateFollowspot(request):
    id=request.POST.get('id','')
    type=request.POST.get('type','')
    value=request.POST.get('value','')
    followspot=Followspot.objects.get(id=id)
    if type=="spotType":
        followspot.spotType=value
        print("TYPE UPDATED")

    if type == "wattage":
        followspot.wattage = value

    if type == "available":
        followspot.available = value
    followspot.save()
    return JsonResponse({"success":"Updated followspot"})

#Project Settings - Operator update
@csrf_exempt
def updateOperator(request):
    id=request.POST.get('id','')
    type=request.POST.get('type','')
    value=request.POST.get('value','')
    op=Operator.objects.get(id=id)
    if type=="operatorNumber":
        op.operatorNumber=value

    if type == "operatorName":
        op.operatorName = value

    if type == "followspotType":
        op.followspotType = Followspot.objects.get(id=value)

    if type == "notes":
        op.notes = value

    op.save()
    return JsonResponse({"success":"Updated Operator"})

#Project Settings - ColorFlag update
@csrf_exempt
def updateColorFlag(request):
    id=request.POST.get('id','')
    type=request.POST.get('type','')
    value=request.POST.get('value','')
    flag=ColorFlag.objects.get(id=id)
    if type=="index":
        flag.index=value

    if type == "color1":
        print(value)
        flag.color1 = Color.objects.get(colorCode=value)

    flag.save()
    return JsonResponse({"success":"Color Flag updated"})

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
