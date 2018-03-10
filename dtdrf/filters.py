import operator
from functools import reduce
from django.db.models import Q
from rest_framework import filters


class DataTablesFilterBackend(filters.BaseFilterBackend):

    def get_ordering(self, request, queryset, view):
        order_dict = view.dt_dict['order']
        col_dict = view.dt_dict['columns']
        ordering = []
        for key in order_dict:
            col_idx = order_dict[key]['column']
            field_name = col_dict[col_idx]['data']
            direction = '-' if order_dict[key]['dir'] == 'desc' else ''
            ordering.append(direction + field_name)
        return ordering

    def filter_queryset(self, request, queryset, view):

        global_search = request.GET.get('search[value]')

        # https://yuji.wordpress.com/2009/09/12/django-python-dynamically-create-queries-from-a-string-and-the-or-operator/
        filters = []
        columns_dict = view.dt_dict['columns']
        for col in list(columns_dict.values()):
            if global_search:
                filters.append(Q(**{col['data'] + '__icontains': global_search}))

            if col['searchable'] and col['search_value']:
                filters.append(Q(**{col['data'] + '__icontains': col['search_value']}))

        if filters:
            query = reduce(operator.or_, filters)
        else:
            query = Q()

        queryset = queryset.filter(query)

        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            return queryset.order_by(*ordering)

        return queryset
