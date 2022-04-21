from .models import *
from bootstrap_modal_forms.forms import BSModalModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import HiddenInput

from django import forms

from projectManager.models import Project

from followspots.models import *

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class ProjectCreateForm(BSModalModelForm):
    class Meta:
        model = Project
        exclude = ['lastUpdate']
        widgets = {'lightingDesigner': forms.HiddenInput(),
                    'active' : forms.HiddenInput()}


#SETTINGS
class FocusForm(BSModalModelForm):
    class Meta:
        model = Focus
        exclude = ['lastUpdate']
        widgets = {'project': forms.HiddenInput()}

class OperatorForm(BSModalModelForm):
    class Meta:
        model = Operator
        exclude = ['lastUpdate']
        widgets = {'project': forms.HiddenInput()}
    def __init__(self,project, *args,**kwargs):
        super (OperatorForm,self ).__init__(*args,**kwargs)


class FollowspotForm(BSModalModelForm):
    class Meta:
        model = Followspot
        exclude = ['lastUpdate']
        widgets = {'project': forms.HiddenInput()}

class ColorFlagForm(BSModalModelForm):
    class Meta:
        model = ColorFlag
        exclude = ['lastUpdate']
        widgets = {'project': forms.HiddenInput()}

class ShotForm(BSModalModelForm):
    class Meta:
        model = Shot
        exclude = ['lastUpdate']
        widgets = {'project': forms.HiddenInput()}

class FocusForm(BSModalModelForm):
    class Meta:
        model = Focus
        exclude = ['lastUpdate']
        # widgets = {'project': forms.HiddenInput()}
