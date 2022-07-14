import django_filters
from django.forms import DateInput
from django_filters import FilterSet
from .models import *
from django_currentuser.middleware import get_current_user, get_current_authenticated_user


class RespFilter(FilterSet):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('my_user_id', None)
        super(RespFilter, self).__init__(*args, **kwargs)

        self.filters['adv_id'].extra.update({
            'queryset': Adv.objects.filter(user_id=self.user),
            'help_text': False
        })

    date_create = django_filters.DateFilter(
        field_name='date_create',
        lookup_expr='gt',
        widget=DateInput(attrs={'type': 'date'},),
        label='Начиная с даты:',
    )

    adv_id = django_filters.ModelChoiceFilter(
        field_name='adv_id',
        label='Объявление:'
    )

    text = django_filters.CharFilter(
        field_name='text',
        label='Текст отклика',
        lookup_expr='icontains',
    )

    class Meta:
        model = Response
        fields = {'adv_id', 'text', 'date_create',}

