from django_filters import CharFilter, FilterSet
from prophecies.core.models import TaskRecord, TaskRecordReview
from prophecies.core.models.task_record_review import StatusType
from actstream.models import Action, user_stream,actor_stream,target_stream
from django.contrib.auth.models import User


class ActionFilter(FilterSet):
    user_stream = CharFilter(method='user_stream_filter')
    class Meta:
        model = Action
        fields = {'verb':['exact', 'in']}
        
    def user_stream_filter(self, queryset, name, value):
        user = User.objects.get(pk=value)
        return queryset & (actor_stream(user) |  target_stream(user))
    
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
    task_record__locked = CharFilter(method='locked_filter')
    task_record__has_notes = CharFilter(method='has_notes_filter')
    task_record__has_disagreements = CharFilter(method='has_disagreements_filter')
    task_record__bookmarked_by = CharFilter(method='bookmarked_by_filter')

    class Meta:
        model = TaskRecordReview
        fields = {
          'checker': ('exact', 'in', 'isnull'),
          'choice': ('exact', 'in', 'isnull'),
          'alternative_value': ('icontains', 'exact', 'iexact', 'contains', 'in', 'iregex'),
          'task_record__priority': ('exact', 'in'),
          'task_record__rounds': ('exact', 'in'),
          'task_record__task': ('exact', 'in'),
          'task_record__predicted_value': ('icontains', 'exact', 'iexact', 'contains', 'in', 'iregex'),
          'task_record__original_value': ('icontains', 'exact', 'iexact', 'contains', 'in'),
          'task_record__reviews__checker': ('exact', 'in'),
          'task_record__reviews__choice': ('exact', 'in'),
          'task_record__reviews__id': ('exact', 'in'),
        }
    
    @staticmethod
    def get_as_boolean(value):
        if value == '0' or value == '1':
            return True, bool(int(value))
        return False,
    
    def boolean_filter_on(self, queryset, filter_name, value):
        is_param_valid, filter_value = self.get_as_boolean(value)
        if is_param_valid:
            ftr = {filter_name: filter_value}
            return queryset \
                    .filter(**ftr)
        return queryset
    
    def has_disagreements_filter(self, queryset, name, value):
        return self.boolean_filter_on(queryset, "task_record__has_disagreements", value)
        
    def has_notes_filter(self, queryset, name, value):
        return self.boolean_filter_on(queryset, "task_record__has_notes", value)

    def locked_filter(self, queryset, name, value):
        return self.boolean_filter_on(queryset, "task_record__locked", value)

    def bookmarked_by_filter(self, queryset, name, value):
        if len(value) > 1:
            union = queryset.none()
            for user in value.split(','):
                union = union | queryset.filter(task_record__bookmarked_by=user)
            return union
        else:
            return queryset.filter(task_record__bookmarked_by=value)

    def reviewed_filter(self, queryset, name, value):
        is_param_valid, filter_value = self.get_as_boolean(value)
        if not is_param_valid:
            return queryset       
        if filter_value:
            return queryset \
                .filter(task_record__reviews__status=StatusType.PENDING)
        else:
            return queryset \
                .filter(task_record__reviews__status=StatusType.DONE) \
                .exclude(task_record__reviews__status=StatusType.PENDING)