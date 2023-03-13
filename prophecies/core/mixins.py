import tablib
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import StreamingHttpResponse
from import_export.admin import ExportMixin
from import_export.forms import ExportForm


class ExportCsvGeneratorMixin:

    def export_csv_as_generator(self, queryset=None, *args, **kwargs):
        self.before_export(queryset, *args, **kwargs)
        queryset = self.get_queryset() if queryset is None else queryset
        # Yield the headers of the CSV
        headers = self.get_export_headers()
        yield tablib.Dataset(headers=headers).csv
        # Iterate without the queryset cache, to avoid wasting memory when exporting large datasets.
        iterable = queryset.iterator() if isinstance(queryset, QuerySet) else queryset
        for row in iterable:
            # Yield one row at a time
            data = tablib.Dataset()
            data.append(self.export_resource(row))
            yield data.csv
        self.after_export(queryset, data, *args, **kwargs)
        yield


class ExportWithCsvStreamMixin(ExportMixin):
    export_template_name = 'admin/import_export/export_with_csv_note.html'

    def export_action(self, request, *args, **kwargs):
        if not self.has_export_permission(request):
            raise PermissionDenied

        formats = self.get_export_formats()
        form = ExportForm(formats, request.POST or None)

        if form.is_valid():
            # Get the current file format
            file_format_idx = int(form.cleaned_data['file_format'])
            file_format = formats[file_format_idx]()
            file_content_type = file_format.get_content_type()
            # Stream response only with CSV
            if file_content_type == 'text/csv':
                dataset = self.resource_class().export_csv_as_generator()
                queryset = self.get_export_queryset(request)
                filename = self.get_export_filename(request, queryset, file_format)
                response = StreamingHttpResponse(dataset, content_type=file_content_type)
                response['Content-Disposition'] = 'attachment; filename="%s"' % filename
                return response

        return super().export_action(request, *args, **kwargs)
