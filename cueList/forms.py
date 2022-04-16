from lightlineapp.models import *
from bootstrap_modal_forms.forms import BSModalForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import HiddenInput

from django import forms


class CueForm(BSModalForm):
    class Meta:
        model = Cue
        exclude = ['lastUpdate']
        widgets = {'cueList': forms.HiddenInput()}

class HeaderForm(BSModalForm):
    class Meta:
        model = Header
        exclude = ['lastUpdate']
        widgets = {'cueList': forms.HiddenInput()}
