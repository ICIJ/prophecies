from django.contrib import admin, messages
from django.contrib.admin.helpers import AdminForm
from django.shortcuts import redirect, render
from django.urls import path
from prophecies.core.models import AlternativeValue
from prophecies.core.forms import AlternativeValueUploadForm


@admin.register(AlternativeValue)
class AlternativeValueAdmin(admin.ModelAdmin):
    change_list_template = "admin/alternative_value_changelist.html"
    list_display = ['__str__', 'choice_group']
    list_filter = ['choice_group']
    search_fields = ['name', 'value']

    def get_urls(self):
        urls = [
            path('upload/', self.upload_view, name='core_alternativevalue_upload'),
        ]
        return urls + super().get_urls()

    def form_as_adminform(self, form, request):
        prepopulated_fields = self.get_prepopulated_fields(request)
        fields = form.base_fields
        fieldsets = [(None, {'fields': fields})]
        return AdminForm(form, fieldsets, prepopulated_fields)

    def build_intermediate_form_context(self, request, form, title):
        adminform = self.form_as_adminform(form, request)
        return dict(self.admin_site.each_context(request),
                    form=form, adminform=adminform,
                    opts=AlternativeValue._meta,
                    original=title, title=title,
                    has_change_permission=self.has_change_permission(request),
                    has_view_permission=self.has_view_permission(request))

    def upload_view(self, request):
        if request.method == "POST":
            # Handle the request in a separated method
            return self.upload_form_handler(request)
        # Or display the upload form
        return self.upload_form_view(request)

    def upload_form_view(self, request, extra_context=None):
        choice_group = request.GET.get('choice_group')
        extra_context = extra_context or {}
        form = extra_context.get('form', AlternativeValueUploadForm(initial={'choice_group': choice_group}))
        title = 'Upload alternative values'
        context = self.build_intermediate_form_context(request=request, form=form, title=title)
        return render(request, "admin/upload_form.html", context)

    def upload_form_handler(self, request):
        form = AlternativeValueUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # The save method will take care of handling the CSV and creating alternative values
            form.save()
            self.message_user(request, "Your csv file has been imported", messages.INFO)
            # Everything is fine, go back to the list of alternative values
            return redirect("..")
        else:
            self.message_user(request, "Unable to import the alternative values", messages.ERROR)
            # Call the same view with the received form
            return self.upload_form_view(request, extra_context={'form': form})
