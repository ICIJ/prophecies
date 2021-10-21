from django_filters import CharFilter, FilterSet 
from prophecies.core.models import TaskRecord, TaskRecordReview
from prophecies.core.models.task_record_review import StatusType


class TaskRecordFilter(FilterSet):
    reviewed = CharFilter(method='reviewed_filter')

    class Meta:
        model = TaskRecord
        fields = ['reviewed']

    def reviewed_filter(self, queryset, name, value):
        if value == '0':
            return queryset \
                .filter(reviews__status=StatusType.PENDING)
        if value == '1':
            return queryset \
                .filter(reviews__status=StatusType.DONE) \
                .exclude(reviews__status=StatusType.PENDING)
        return queryset


class TaskRecordReviewFilter(FilterSet):
    task_record__reviewed = CharFilter(method='reviewed_filter')

    class Meta:
        model = TaskRecordReview
        fields = {
          'checker': ('exact', 'in', 'isnull'),
          'choice': ('exact', 'in', 'isnull'),
          'alternative_value': ('icontains', 'exact', 'iexact', 'contains', 'in', 'iregex'),
          'task_record__priority': ('exact', 'in'),
          'task_record__rounds': ('exact', 'in'),
          'task_record__task': ('exact', 'in'),
          'task_record__locked': ('exact',),
          'task_record__has_notes': ('exact',),
          'task_record__has_disagreements': ('exact',),
          'task_record__predicted_value': ('icontains', 'exact', 'iexact', 'contains', 'in', 'iregex'),
          'task_record__original_value': ('icontains', 'exact', 'iexact', 'contains', 'in'),
          'task_record__reviews__checker': ('exact', 'in'),
          'task_record__reviews__choice': ('exact', 'in'),
          'task_record__reviews__id': ('exact', 'in'),
        }

    def reviewed_filter(self, queryset, name, value):
        if value == '0':
            return queryset \
                .filter(task_record__reviews__status=StatusType.PENDING)
        if value == '1':
            return queryset \
                .filter(task_record__reviews__status=StatusType.DONE) \
                .exclude(task_record__reviews__status=StatusType.PENDING)
        return queryset