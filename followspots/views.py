# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy

from django.shortcuts import render
from .models import SpotCue
from .forms import SpotCueForm, ActionForm, OperatorForm, FocusForm

from bootstrap_modal_forms.generic import BSModalCreateView


def index(request):
    spotCueList = SpotCue.objects.order_by('eosCueNumber')[:20]
    template = loader.get_template('index.html')
    context = {
        'spotCueList': spotCueList,
    }
    return HttpResponse(template.render(context, request))


class SpotCueCreateView(BSModalCreateView):
    template_name = 'followspots/createSpotCue.html'
    form_class = SpotCueForm
    success_message = 'Success: Spot Cue was created.'
    success_url = reverse_lazy('index')

class ActionCreateView(BSModalCreateView):
    template_name = 'followspots/createAction.html'
    form_class = ActionForm
    success_message = 'Success: Action was created.'
    success_url = reverse_lazy('index')

class OperatorCreateView(BSModalCreateView):
    template_name = 'followspots/createOperator.html'
    form_class = OperatorForm
    success_message = 'Success: Operator was added.'
    success_url = reverse_lazy('index')

class FocusCreateView(BSModalCreateView):
    template_name = 'followspots/createFocus.html'
    form_class = FocusForm
    success_message = 'Success: Focus was added.'
    success_url = reverse_lazy('index')
