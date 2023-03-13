from constance import config
from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site
from django.urls import include, path, reverse_lazy
from django.views.generic import TemplateView, RedirectView
from social_django.models import UserSocialAuth, Nonce, Association

admin.site.site_header = config.appName
admin.site.site_title = config.appName
admin.site.unregister(Site)
admin.site.unregister(UserSocialAuth)
admin.site.unregister(Nonce)
admin.site.unregister(Association)

urlpatterns = [
    path('', include('social_django.urls', namespace='sso')),
    path('', TemplateView.as_view(template_name="index.html"), name="home"),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if not settings.DJANGO_ADMIN_LOGIN:
    redirect_login_view = RedirectView.as_view(url=reverse_lazy('home'), permanent=True, query_string=True)
    redirect_login_path = path('admin/login/', redirect_login_view)
    urlpatterns = [redirect_login_path] + urlpatterns

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
