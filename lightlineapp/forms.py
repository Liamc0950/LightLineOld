from .models import *
from bootstrap_modal_forms.forms import BSModalForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import HiddenInput

from django import forms

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class ProjectCreateForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['lastUpdate']
        widgets = {'lightingDesigner': forms.HiddenInput(),
                    'active' : forms.HiddenInput()}



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

""" class ShareNodeForm(BSModalForm):
    class Meta:
        model = ShareNode
        exclude = ['lastUpdate']
        widgets = {'project': forms.HiddenInput()}
 """
