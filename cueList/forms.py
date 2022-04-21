from lightlineapp.models import *
from bootstrap_modal_forms.forms import BSModalModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import HiddenInput

from django import forms
from .models import *

class CueForm(BSModalModelForm):
    class Meta:
        model = Cue
        exclude = ['lastUpdate']
        widgets = {'cueList': forms.HiddenInput()}

class HeaderForm(BSModalModelForm):
    class Meta:
        model = Header
        exclude = ['lastUpdate']
        widgets = {'cueList': forms.HiddenInput()}

class CueListCreateForm(forms.ModelForm):
    class Meta:
        model = CueList
        exclude = ['lastUpdate']
        widgets = {'active' : forms.HiddenInput(), 
                   'project' : forms.HiddenInput(),}
