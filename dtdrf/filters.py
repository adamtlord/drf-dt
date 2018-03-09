import re
import operator
from functools import reduce
from django.db.models import Q
from rest_framework import filters
import pprint
pp = pprint.PrettyPrinter(indent=4)


class DataTablesFilterBackend(filters.BaseFilterBackend):
    def assemble_columns_list(self, request):
        request_dict = request.GET
        columns_dict = {}
        for key in request_dict:
            if 'columns' in key:
                try:
                    col_idx = re.match('columns\[(\d+)\]', key).group(1)
                    if col_idx in columns_dict:
                        continue
                    else:
                        col_prefix = 'columns[{}]'.format(col_idx)
                        columns_dict[col_idx] = {
                            'data': request_dict[col_prefix + '[data]'],
                            'name': request_dict[col_prefix + '[name]'],
                            'orderable': request_dict[col_prefix + '[orderable]'] == 'true',
                            'search_regex': request_dict[col_prefix + '[search][regex]'] == 'true',
                            'search_value': request_dict[col_prefix + '[search][value]'],
                            'searchable': request_dict[col_prefix + '[searchable]'] == 'true',
                        }
                except AttributeError:
                    continue
            else:
                continue

        return list(columns_dict.values())

    def filter_queryset(self, request, queryset, view):

        global_search = request.GET.get('search[value]')
        columns_list = self.assemble_columns_list(request)

        # https://yuji.wordpress.com/2009/09/12/django-python-dynamically-create-queries-from-a-string-and-the-or-operator/
        filters = []

        for col in columns_list:
            if global_search:
                filters.append(Q(**{col['data']+'__icontains': global_search}))

            if col['searchable'] and col['search_value']:
                filters.append(Q(**{col['data']+'__icontains': col['search_value']}))

        if filters:
            query = reduce(operator.or_, filters)
        else:
            query = Q()

        queryset = queryset.filter(query)
        print()
        print(queryset.count())
        print()
        return queryset
