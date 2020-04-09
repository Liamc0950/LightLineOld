# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy

from django.shortcuts import render
from .models import SpotCue, ColorFlag, Color
from .forms import SpotCueForm, ActionForm, OperatorForm, FocusForm


from bootstrap_modal_forms.generic import BSModalCreateView


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(request))


def followspots(request):
    spotCueList = SpotCue.objects.order_by('eosCueNumber')[:20]
    template = loader.get_template('followspots.html')
    context = {
        'spotCueList': spotCueList,
    }
    return HttpResponse(template.render(context, request))


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

