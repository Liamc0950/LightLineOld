from .models import SpotCue, Action, Operator, Focus, ColorFlag
from bootstrap_modal_forms.forms import BSModalForm

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

