from lightlineapp.models import *
from bootstrap_modal_forms.forms import BSModalForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import HiddenInput

from django import forms

from .models import *

class ActionForm(BSModalForm):
    class Meta:
        model = Action
        exclude = ['lastUpdate']

    def __init__(self,project, activeCueList, *args,**kwargs):
        super (ActionForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['operator'].queryset = Operator.objects.filter(project=project)
        self.fields['colorFlag'].queryset = ColorFlag.objects.filter(project=project)
        self.fields['focus'].queryset = Focus.objects.filter(project=project)
        self.fields['cue'].queryset = Cue.objects.filter(cueList=activeCueList)

class FocusForm(BSModalForm):
    class Meta:
        model = Focus
        exclude = ['lastUpdate']
        widgets = {'project': forms.HiddenInput()}
class OperatorForm(BSModalForm):
    class Meta:
        model = Operator
        exclude = ['lastUpdate']
        widgets = {'project': forms.HiddenInput()}
    def __init__(self,project, *args,**kwargs):
        super (OperatorForm,self ).__init__(*args,**kwargs) # populates the post
        #limit to shareNodes of this project and of role 6 (operator)
        #self.fields['shareNode'].queryset = ShareNode.objects.filter(project=project, role=6)


class FollowspotForm(BSModalForm):
    class Meta:
        model = Followspot
        exclude = ['lastUpdate']
        widgets = {'project': forms.HiddenInput()}

class ColorFlagForm(BSModalForm):
    class Meta:
        model = ColorFlag
        exclude = ['lastUpdate']
        widgets = {'project': forms.HiddenInput()}

class ShotForm(BSModalForm):
    class Meta:
        model = Shot
        exclude = ['lastUpdate']
        widgets = {'project': forms.HiddenInput()}

class FocusForm(BSModalForm):
    class Meta:
        model = Focus
        exclude = ['lastUpdate']
        # widgets = {'project': forms.HiddenInput()}

