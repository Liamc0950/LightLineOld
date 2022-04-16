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
