from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework import routers
from prophecies.apps.api.views.action import ActionViewSet
from prophecies.apps.api.views.choice_group import ChoiceGroupViewSet
from prophecies.apps.api.views.project import ProjectViewSet
from prophecies.apps.api.views.setting import SettingViewSet
from prophecies.apps.api.views.task_record import TaskRecordViewSet
from prophecies.apps.api.views.task_record_review import TaskRecordReviewViewSet
from prophecies.apps.api.views.task import TaskViewSet
from prophecies.apps.api.views.user import UserViewSet

router = routers.DefaultRouter()
router.register(r'actions', ActionViewSet)
router.register(r'choice-groups', ChoiceGroupViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'settings', SettingViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'task-records', TaskRecordViewSet)
router.register(r'task-record-reviews', TaskRecordReviewViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', RedirectView.as_view(url='v1/')),
    path('v1/', include(router.urls)),
    path('v1/users/<pk>/relationships/actions/', view=UserViewSet.as_view({ 'get': 'actions' }), name='user-actions'),
]
