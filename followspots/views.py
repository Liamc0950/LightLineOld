# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import loader

from django.shortcuts import render
from .models import SpotCue

def index(request):
    spotCueList = SpotCue.objects.order_by('eosCueNumber')[:20]
    template = loader.get_template('followspots/index.html')
    context = {
        'spotCueList': spotCueList,
    }
    return HttpResponse(template.render(context, request))
