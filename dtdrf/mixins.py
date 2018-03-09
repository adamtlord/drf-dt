from collections import OrderedDict
from rest_framework.response import Response

import pprint
pp = pprint.PrettyPrinter(indent=4)


class DataTablesListMixin(object):

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('data', data)
        ]))

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        self.queryset_count = queryset.count()

        filtered_queryset = self.filter_queryset(queryset)
        self.filtered_count = filtered_queryset.count()

        page = self.paginate_queryset(filtered_queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        response = Response(serializer.data)

        return response

    def dispatch(self, request, *args, **kwargs):
        print()
        pp.pprint(request.GET)
        print()
        response = super(DataTablesListMixin, self).dispatch(request, args, kwargs)

        draw = int(request.GET.get('draw', 1))
        recordsTotal = self.queryset_count
        recordsFiltered = self.filtered_count

        response.data.update({
            'draw': draw,
            'recordsTotal': recordsTotal,
            'recordsFiltered': recordsFiltered
        })

        return response
