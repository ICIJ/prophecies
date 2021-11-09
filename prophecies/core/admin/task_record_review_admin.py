from admin_auto_filters.filters import AutocompleteFilterFactory
from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ExportMixin
from textwrap import shorten

from prophecies.core.models import TaskRecordReview
from prophecies.core.contrib.display import display_status, display_task_addon, display_choice


@admin.register(TaskRecordReview)
class TaskRecordReviewAdmin(ExportMixin, admin.ModelAdmin):    
    list_display = ['review_with_details', 'task_with_addon', 'round', 'status_badge']
    list_filter = [
        AutocompleteFilterFactory('task', 'task_record__task'),
        AutocompleteFilterFactory('project', 'task_record__task__project'),
        AutocompleteFilterFactory('checkers', 'checker'),
        'choice',
        'status',
        'round',
    ]
    
    # By default, we deactivate adding review to force users to
    # assign them through the "task record" admin page.
    def has_add_permission(self, request, obj=None):
        return False
    
    
    def get_queryset(self, request):
        return super().get_queryset(request) \
            .prefetch_related('checker') \
            .prefetch_related('task_record') \
            .prefetch_related('task_record__task') \
            .prefetch_related('task_record__task__project')

    def review_with_details(self, review):
        review_title = str(review)
        excerpt = shorten(review.task_record.original_value, width=140, placeholder='...') if review.task_record else ''
        choice = display_choice(review.choice) if review.choice else ''
        context = dict(review_title=review_title, excerpt=excerpt, choice=choice)
        template = """
            <div class="task-record-review-display">
                <div>{review_title}</div>
                <div class="font-weight-light text-quiet">{excerpt}</div>
                <div class="task-record-review-display__choice font-weight-normal text-quiet">{choice}</div>
            </div>
        """
        return format_html(template, **context)

    review_with_details.short_description = "Review"


    def status_badge(self, review):
        return display_status(review.get_status_display())

    status_badge.short_description = "Status"


    def task_with_addon(self, review):
        if review.task_record:
            return display_task_addon(review.task_record.task)
        return ''

    task_with_addon.short_description = "Task"
