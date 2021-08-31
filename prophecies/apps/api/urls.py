from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework import routers
from prophecies.apps.api.views.action import ActionViewSet
from prophecies.apps.api.views.choice_group import ChoiceGroupViewSet
from prophecies.apps.api.views.notification import NotificationViewSet
from prophecies.apps.api.views.project import ProjectViewSet
from prophecies.apps.api.views.setting import SettingViewSet
from prophecies.apps.api.views.task_record import TaskRecordViewSet
from prophecies.apps.api.views.task_record_review import TaskRecordReviewViewSet
from prophecies.apps.api.views.task import TaskViewSet
from prophecies.apps.api.views.user import UserViewSet
from prophecies.apps.api.views.tip import TipViewSet

router = routers.DefaultRouter()
router.register(r'actions', ActionViewSet)
router.register(r'choice-groups', ChoiceGroupViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'settings', SettingViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'task-records', TaskRecordViewSet)
router.register(r'task-record-reviews', TaskRecordReviewViewSet)
router.register(r'users', UserViewSet)
router.register(r'tips', TipViewSet)

urlpatterns = [
    path('', RedirectView.as_view(url='v1/')),
    path('v1/', include(router.urls)),
    path('v1/task-records/<pk>/relationships/actions/', view=TaskRecordViewSet.as_view({ 'get': 'actions' }), name='task-record-actions'),
    path('v1/users/<pk>/relationships/actions/', view=UserViewSet.as_view({ 'get': 'actions' }), name='user-actions'),
]
