from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from prophecies.core.models.setting import Setting


class SettingSerializer(serializers.ModelSerializer):
    key = serializers.CharField()
    value = serializers.CharField()
    search_fields = ['key', 'value']
    ordering_fields = ['key']
    ordering = ['key']
    filterset_fields = ['key', 'value']

    class Meta:
        model = Setting
        fields = ['key', 'value']


class SettingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Setting.objects.all()
    serializer_class = SettingSerializer
    pagination_class = None

    def list(self, request, **kwargs):
        with_env = Setting.objects.with_env()
        serializer = SettingSerializer(with_env, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kargs):
        try:
            with_env = Setting.objects.with_env()
            setting = next(s for s in with_env if s.key == pk)
        except StopIteration:
            raise NotFound()
        serializer = SettingSerializer(setting, context={'request': request}, many=False)
        return Response(serializer.data)
