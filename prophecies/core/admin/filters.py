from django.contrib.admin.filters import AllValuesFieldListFilter

class DistinctValuesDropdownFilter(AllValuesFieldListFilter):
    template = 'admin/filters/distinct_values_dropdown_filter.html'
