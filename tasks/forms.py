from django.forms import ModelForm, Textarea, DateTimeInput

from .models import Task


class TaskForm(ModelForm):

    class Meta:
        model = Task
        exclude = ['author']
        localized_fields = '__all__'
        widgets = {
            'task_content': Textarea(
                attrs={
                    'rows': 7,
                    'class': 'form-control'
                }
            ),
            'task_date': DateTimeInput(
                attrs={
                    'class': 'datetimefield'
                },

            )
        }
