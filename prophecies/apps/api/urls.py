from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework import routers
from .views.user import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', RedirectView.as_view(url='v1/')),
    path('v1/', include(router.urls)),
]
