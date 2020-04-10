from .models import SpotCue, Action, Operator, Focus, ColorFlag
from bootstrap_modal_forms.forms import BSModalForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class SpotCueForm(BSModalForm):
    class Meta:
        model = SpotCue
        exclude = ['lastUpdate']

class ActionForm(BSModalForm):
    class Meta:
        model = Action
        exclude = ['lastUpdate']

class OperatorForm(BSModalForm):
    class Meta:
        model = Operator
        exclude = ['lastUpdate']

class FocusForm(BSModalForm):
    class Meta:
        model = Focus
        exclude = ['lastUpdate']
        
class ColorFlagForm(BSModalForm):
    class Meta:
        model = ColorFlag
        exclude = ['lastUpdate']

