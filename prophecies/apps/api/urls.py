from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework import routers
from .views.user import UserViewSet
from .views.setting import SettingViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'settings', SettingViewSet)

urlpatterns = [
    path('', RedirectView.as_view(url='v1/')),
    path('v1/', include(router.urls)),
]
