from rest_framework import pagination


class DataTablesPagination(pagination.LimitOffsetPagination):
    limit_query_param = 'length'
    offset_query_param = 'start'
