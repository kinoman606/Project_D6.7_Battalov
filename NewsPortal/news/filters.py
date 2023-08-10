from django.forms import DateTimeInput
from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateTimeFilter
from .models import Category


class PostFilter(FilterSet):

    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='по названию',

    )
    postCategory = ModelChoiceFilter(
        field_name='postcategory__category_through',
        queryset=Category.objects.all(),
        label='по категории',
        empty_label='любая'
    )

    datePost = DateTimeFilter(
        field_name='date_post',
        lookup_expr='gt',
        label='позже указываемой даты',
        widget=DateTimeInput(attrs={'type': 'datetime-local'}),
    )







