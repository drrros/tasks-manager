from django import forms
from django.forms import ModelForm, Textarea, DateInput, DateTimeInput
from .models import Task


class TaskForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['author'].queryset = Task.objects.filter(owner=request.user)

    # task_date = forms.DateTimeField(required=False,
    #                                  widget=DateTimeInput(
    #                                      format='%d/%m/%Y %H:%M',
    #                                      attrs={'class': 'datetimefield'}
    #                                  ),
    #                                  localize=True,
    #                                  input_formats=['%d/%m/%Y %H:%M',])

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
