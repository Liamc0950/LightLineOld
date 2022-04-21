#Boilerplate
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy

from django.shortcuts import render, redirect


from django.contrib.auth.decorators import login_required

from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#Modals
from bootstrap_modal_forms.generic import BSModalCreateView


from .models import *
from .forms import *
from followspots.models import *
from cueList.models import *
from database.models import *

@method_decorator(login_required, name='dispatch')
class ProjectCreateView(CreateView):
    template_name = 'projectManager/createProject.html'
    form_class = ProjectCreateForm
    success_message = 'Success: Project was created.'
    #On success, move on to cue list creation view
    success_url = reverse_lazy('createCueListPageView')

    def get_initial(self, *args, **kwargs):
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

@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
class FollowspotCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createFollowspot.html'
    form_class = FollowspotForm
    success_message = 'Success: Followspot was added.'
    success_url = reverse_lazy('projectSettings')

    def get_initial(self, *args, **kwargs):
        initial = super(FollowspotCreateView, self).get_initial(**kwargs)
        initial['project'] = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        return initial

@method_decorator(login_required, name='dispatch')
class ColorFlagCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createColorFlag.html'
    form_class = ColorFlagForm
    success_message = 'Success: Color Flag was added.'
    success_url = reverse_lazy('projectSettings')

    def get_initial(self, *args, **kwargs):
        initial = super(ColorFlagCreateView, self).get_initial(**kwargs)
        initial['project'] = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        return initial

@method_decorator(login_required, name='dispatch')
class ShotCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createShot.html'
    form_class = ShotForm
    success_message = 'Success: Shot was added.'
    success_url = reverse_lazy('projectSettings')

    def get_initial(self, *args, **kwargs):
        initial = super(ShotCreateView, self).get_initial(**kwargs)
        initial['project'] = Project.objects.get(lightingDesigner=self.request.user.profile, active=True)
        return initial

@login_required
def focusDelete(request, focusID):
    focus = Focus.objects.get(id=focusID)
    focus.delete()
    return HttpResponseRedirect('/lightlineapp/projectSettings')


@login_required
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


#Project Settings - Followspot update
@login_required
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
@login_required
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
@login_required
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

@login_required
#Project settings view
def projectSettings(request):
    #try to get the active project, then get all the cues in cueList linked to active project
    try:
        activeProject = Project.objects.get(lightingDesigner=request.user.profile, active=True)
        projectCueLists = CueList.objects.filter(project = activeProject)
        projectOperators = Operator.objects.filter(project = activeProject)
        projectFocus = Focus.objects.filter(project = activeProject)
        spotList = Followspot.objects.filter(project = activeProject)
        colorList = ColorFlag.objects.filter(project = activeProject).order_by('index')
        shots = Shot.objects.filter(project = activeProject)
        focusList = Focus.objects.filter(project = activeProject)
        projectColorFlags = ColorFlag.objects.filter(project = activeProject)
    except:
        activeProject = Project.objects.none()
        cueList = Cue.objects.none()

    projects = Project.objects.filter(lightingDesigner=request.user.profile)
    template = loader.get_template('projectManager/projectSettings.html')
    context = {
        'activeProject': activeProject,
        'projects' : projects,
        'projectCueLists' : projectCueLists,
        'projectOperators' : projectOperators,
        'projectFocus' : projectFocus,
        'shots' : shots,
        'focusList' : focusList,
        'projectColorFlags' : projectColorFlags,
        'spotList' : spotList,
        'colorList' : colorList,
        'colors' : Color.objects.all(),
    }

    return HttpResponse(template.render(context, request))
