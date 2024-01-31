from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from prophecies.core.models.setting import Setting


class SettingSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()
    public = serializers.BooleanField()


class SettingViewSet(viewsets.ViewSet):
    serializer_class = SettingSerializer
    pagination_class = None
    resource_name = 'Setting'
    http_method_names = ['get', 'head']
    permission_classes = []

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Setting.objects.all_public_with_env()
        return Setting.objects.all_with_env()

    def list(self, request, **_kwargs):
        settings = self.get_queryset()
        serializer = SettingSerializer(settings, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **_kwargs):
        try:
            setting = next(s for s in self.get_queryset() if s.key == pk)
        except StopIteration:
            raise NotFound()
        serializer = SettingSerializer(setting, context={'request': request}, many=False)
        return Response(serializer.data)
