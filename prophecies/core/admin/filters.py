from django.contrib import admin
from django.contrib.admin.filters import AllValuesFieldListFilter
from prophecies.core.models.task_record_review import StatusType


class DistinctValuesDropdownFilter(AllValuesFieldListFilter):
    template = 'admin/filters/distinct_values_dropdown_filter.html'


class TaskRecordReviewFilter(admin.SimpleListFilter):
    title = 'review status'
    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'reviewed'

    def lookups(self, request, model_admin):
        return (
            ('1', 'Reviewed'),
            ('0', 'Not reviewed'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset \
                .filter(reviews__status=StatusType.PENDING)
        if self.value() == '1':
            return queryset \
                .filter(reviews__status=StatusType.DONE) \
                .exclude(reviews__status=StatusType.PENDING)
        return queryset
