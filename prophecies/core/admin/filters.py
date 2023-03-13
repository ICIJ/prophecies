from django.contrib import admin
from django.contrib.admin.filters import AllValuesFieldListFilter
from prophecies.core.filters import TaskRecordFilter


class DistinctValuesDropdownFilter(AllValuesFieldListFilter):
    template = 'admin/filters/distinct_values_dropdown_filter.html'


class ReviewedTaskRecordFilter(admin.SimpleListFilter):
    title = 'review status'
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'reviewed'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Reviewed'),
            ('0', 'Not reviewed'),
        )

    def queryset(self, request, queryset):
        params = {'reviewed': self.value()}
        return TaskRecordFilter(params, queryset=queryset).qs
