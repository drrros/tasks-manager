import django_filters
from django.forms import DateTimeInput

from .models import Task

class TaskFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name='task_date',
                                           lookup_expr='gte',
                                           label='Дата с',
                                           widget=DateTimeInput(format="'%D.%m.%Y %H:%M'",
                                                                attrs={'class':'datetimefield'}
                                                                )
                                           )
    end_date = django_filters.DateTimeFilter(field_name='task_date',
                                         lookup_expr='lte',
                                         label='по ',
                                         widget=DateTimeInput(format="'%D.%m.%Y %H:%M'",
                                                              attrs={'class': 'datetimefield'}
                                                              )
                                         )
    task_header = django_filters.CharFilter(field_name='task_header', lookup_expr='icontains', label='Поиск по содержанию:')
    class Meta:
        model = Task
        fields = ['task_header', 'task_type']
