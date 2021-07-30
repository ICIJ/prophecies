import json
from django.urls import reverse
from django.utils.html import format_html
from prophecies.core.contrib.variant import to_variant


def display_json(obj, indent=2):
    if obj is None:
        return '-'
    pretty = json.dumps(obj, indent=indent)
    return format_html('<pre class="m-0 p-0"><code class="language-json">{0}</code></pre>', pretty)


def display_task_addon(task):
    color_var = f'--task-addon-bg: {task.color};'
    href = reverse('admin:core_task_change', args=[task.id])
    context = dict(href=href, task=task, color_var=color_var)
    return format_html('<a href="{href}" class="task-addon" style="{color_var}">{task}</a>', **context)


def display_task_record_link(task_record):
    if not task_record.link and not task_record.task.recordLinkTemplate:
        return '-'
    href = task_record.computed_link()
    return format_html('<a href="{0}" target="_blank">{0}</a>', href)


def display_status(status):
    variant = to_variant(status, prefix='badge-')
    context = dict(status=status, variant=variant)
    return format_html('<span class="badge {variant}">{status}</span>', **context)
