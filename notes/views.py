#Boilerplate
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import *


# Create your views here.

@login_required
#Notes feature view
def notes(request):
    template = loader.get_template('notes.html')
    context={}
    return HttpResponse(template.render(context, request))
