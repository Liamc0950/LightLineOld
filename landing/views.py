#Boilerplate
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse_lazy

from django.shortcuts import render, redirect

#Landing and Authorization Views
from .forms import *
#User Auth
from django.contrib.auth import login, authenticate


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
    return render(request, 'landing/signup.html', {'form': form})



#Landing page View
def index(request):
    template = loader.get_template('landing/index.html')
    context={}
    return HttpResponse(template.render(context, request))
