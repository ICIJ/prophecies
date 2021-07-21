from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site
from django.urls import include, path
from social_django.models import UserSocialAuth, Nonce, Association

admin.site.site_header = "Prophecies"
admin.site.site_title = "Prophecies"
admin.site.unregister(Site)
admin.site.unregister(UserSocialAuth)
admin.site.unregister(Nonce)
admin.site.unregister(Association)

urlpatterns = [
    path('', include('social_django.urls', namespace='sso')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [ path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
