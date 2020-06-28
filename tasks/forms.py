from django.forms import ModelForm, Textarea, DateInput
from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ['author']
        widgets = {
            'task_content': Textarea(
                attrs={
                    'rows': 7,
                    'class': 'form-control'
                }
            ),
            'task_date': DateInput(
                # format="'%d/%m/%Y'",
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control form-control-sm extendable'
                }
            )
        }
