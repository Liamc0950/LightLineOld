# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from .models import SpotCue, ColorFlag, Color
from .forms import SpotCueForm, ActionForm, OperatorForm, FocusForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from bootstrap_modal_forms.generic import BSModalCreateView

from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('followspots')
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
    spotCueList = SpotCue.objects.order_by('eosCueNumber')[:20]
    template = loader.get_template('followspots.html')
    context = {
        'spotCueList': spotCueList,
    }
    return HttpResponse(template.render(context, request))

#Followspot Modal Views
class SpotCueCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createSpotCue.html'
    form_class = SpotCueForm
    success_message = 'Success: Spot Cue was created.'
    success_url = reverse_lazy('followspots')

class ActionCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createAction.html'
    form_class = ActionForm
    success_message = 'Success: Action was created.'
    success_url = reverse_lazy('followspots')

class OperatorCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createOperator.html'
    form_class = OperatorForm
    success_message = 'Success: Operator was added.'
    success_url = reverse_lazy('followspots')

class FocusCreateView(BSModalCreateView):
    template_name = 'lightlineapp/createFocus.html'
    form_class = FocusForm
    success_message = 'Success: Focus was added.'
    success_url = reverse_lazy('followspots')

