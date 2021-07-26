from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site
from django.urls import include, path
from django.views.generic import TemplateView
from social_django.models import UserSocialAuth, Nonce, Association
from constance import config

admin.site.site_header = config.appName
admin.site.site_title = config.appName
admin.site.unregister(Site)
admin.site.unregister(UserSocialAuth)
admin.site.unregister(Nonce)
admin.site.unregister(Association)

urlpatterns = [
    path('', include('social_django.urls', namespace='sso')),
    path('', TemplateView.as_view(template_name="index.html"), name="app"),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [ path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
