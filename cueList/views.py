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

from lightlineapp.models import *

from .forms import *


#Modals
from bootstrap_modal_forms.generic import BSModalCreateView

from django.utils.decorators import method_decorator

@login_required
#CueList feature view    
def cueListView(request):
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
    template = loader.get_template('cueList/cueList.html')
    context = {
        'cueList': activeCues,
        'activeProject': activeProject,
        'projects' : projects,
        'projectCueLists' : projectCueLists,
        'activeCueList' : activeCueList,
    }

    return HttpResponse(template.render(context, request))



#Delete Cue - deletes given cue (designated by parent of delete button)
def cueDeleteCueList(request, cueID):
    cue = Cue.objects.get(id=cueID)
    cue.delete()
    return HttpResponseRedirect('/cueList')

#Create Cue - creates cue with no modal, cue number generated from cue num iterator from Cue model
def cueCreateCueList(request, lastCueNum):

    Cue.objects.createNext(lastCueNum)
    
    return HttpResponseRedirect('/cueList')

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


def switchActiveCueList(request):
    if request.method == "POST":
        #deactivate other cue lists
        activeProject = Project.objects.get(lightingDesigner=request.user.profile, active=True)
        projectCueLists = CueList.objects.filter(project = activeProject)

        for cueList in projectCueLists:
            cueList.active = False
            cueList.save()
        #Activate selected cue list
        cueListID = request.POST.get('cueList', '/')
        cueList = CueList.objects.get(id=cueListID)
        cueList.active = True;
        cueList.save()

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

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

#CueList Create CueList (MODAL VIEW)
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

# Create CueList (PAGE VIEW - USED IN INTITIAL PROJECT SETUP)
@method_decorator(login_required, name='dispatch')
class CueListCreateViewPageView(CreateView):
    template_name = 'cueList/createCueList.html'
    form_class = CueListCreateForm
    success_message = 'Success: Cue List was created.'
    success_url = reverse_lazy('projectSettings')

    def get_initial(self, *args, **kwargs):
        initial = super(CueListCreateViewPageView, self).get_initial(**kwargs)
        activeProject = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        initial['project'] = activeProject

        return initial

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.

        #Get the current active project
        activeProject = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        #Get all active cueLists linked to this project
        cueLists = CueList.objects.filter(project=activeProject)

        #Deactivate all active cueLists
        for cueList in cueLists:
            cueList.active = False
            cueList.save()

        return super().form_valid(form)



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
