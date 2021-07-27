from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework import routers
from prophecies.apps.api.views.project import ProjectViewSet
from prophecies.apps.api.views.setting import SettingViewSet
from prophecies.apps.api.views.task import TaskViewSet
from prophecies.apps.api.views.user import UserViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'settings', SettingViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', RedirectView.as_view(url='v1/')),
    path('v1/', include(router.urls)),
]
