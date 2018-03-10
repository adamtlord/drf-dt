# drf-dt
Django Rest Framework/DataTables server-side integration.

## DataTables Configuration
In your DataTables initialization:
 - Set the [`serverSide`](https://datatables.net/reference/option/serverSide) option to `true`
 - Set the [`ajax`](https://datatables.net/reference/option/ajax) param to the url of your list endpoint
 - Because DRF returns an array of objects instead of an array of arrays, it is necessary to define the data for each column in the [`columns`](https://datatables.net/reference/option/columns) or [`columnDefs`](https://datatables.net/reference/option/columnDefs) parameter. 

Example configuration:
```javascript
$('#table_id').DataTable({
  "processing": true,
  "serverSide": true,
  "ajax": "/api/widgets/",
  "columns": [
    { "data": "first_name" },
    { "data": "last_name" },
    { "data": "email" },
    { "data": "gender" },
    { "data": "city" },
  ]
});
```

## DRF Configuration
- Add `'dtdrf'` to your `INSTALLED_APPS` setting
- In the view or viewset that handles the list data for your table, add the `DataTablesListMixin`
- Import and set the options for `DataTablesPagination` and `DataTablesFilterBackend`

Example view:
```python
from rest_framework import viewsets

from dtdrf.mixins import DataTablesListMixin
from dtdrf.pagination import DataTablesPagination
from dtdrf.filters import DataTablesFilterBackend


class WidgetViewSet(DataTablesListMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows widgets to be viewed.
    """
    queryset = Widget.objects.all().order_by('-id')
    serializer_class = WidgetSerializer
    filter_backends = (DataTablesFilterBackend,)
    pagination_class = DataTablesPagination
```
