import re
from collections import OrderedDict
from rest_framework.response import Response


class DataTablesListMixin(object):

    def assemble_dt_dict(self, request):
        request_dict = request.GET
        columns_dict = {
            'columns': {},
            'order': {}
        }

        for key in request_dict:
            if 'columns' in key:
                try:
                    col_idx = re.match('columns\[(\d+)\]', key).group(1)
                    if col_idx in columns_dict['columns']:
                        continue
                    else:
                        col_prefix = 'columns[{}]'.format(col_idx)
                        columns_dict['columns'][col_idx] = {
                            'data': request_dict[col_prefix + '[data]'],
                            'name': request_dict[col_prefix + '[name]'],
                            'orderable': request_dict[col_prefix + '[orderable]'] == 'true',
                            'search_regex': request_dict[col_prefix + '[search][regex]'] == 'true',
                            'search_value': request_dict[col_prefix + '[search][value]'],
                            'searchable': request_dict[col_prefix + '[searchable]'] == 'true',
                        }
                except AttributeError:
                    continue
            if 'order' in key:
                try:
                    order_idx = re.match('order\[(\d+)\]', key).group(1)
                    if order_idx in columns_dict['order']:
                        continue
                    else:
                        columns_dict['order'][order_idx] = {
                            'column': request_dict['order[' + order_idx + '][column]'],
                            'dir': request_dict['order[' + order_idx + '][dir]']
                        }
                except AttributeError:
                    continue
            else:
                continue

        return columns_dict

    def get_response(self, data):
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
            return self.get_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        response = self.get_response(serializer.data)

        return response

    def dispatch(self, request, *args, **kwargs):
        self.dt_dict = self.assemble_dt_dict(request)

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
