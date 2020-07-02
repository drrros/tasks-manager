import django_filters
from django.forms import DateTimeInput, TextInput, Select

from .models import Task


class TaskFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name='task_date',
                                               lookup_expr='gte',
                                               label='',
                                               widget=DateTimeInput(format="'%D.%m.%Y %H:%M'",
                                                                    attrs={'class':'datetimefield form-control form-control-sm',
                                                                         'placeholder': 'Дата с:'}
                                                                    )
                                               )

    end_date = django_filters.DateTimeFilter(field_name='task_date',
                                             lookup_expr='lte',
                                             label='',
                                             widget=DateTimeInput(format="'%D.%m.%Y %H:%M'",
                                                                  attrs={'class': 'datetimefield form-control form-control-sm',
                                                                         'placeholder': 'Дата по:'
                                                                         }
                                                                  )
                                             )

    task_header = django_filters.CharFilter(field_name='task_header',
                                            lookup_expr='icontains',
                                            label='Поиск по содержанию:',
                                            widget=TextInput(attrs={'class': 'form-control form-control-sm',
                                                                         'placeholder': 'Поиск по заголовку события:'}
                                                             )
                                            )

    task_type = django_filters.ChoiceFilter(field_name='task_type',
                                            choices=[('Звонок', 'Звонок'), ('Встреча', 'Встреча')],
                                            widget=Select(attrs={'class': 'form-control form-control-sm',
                                                                }
                                                          )
                                            )
    class Meta:
        model = Task
        fields = ['task_header', 'task_type']
