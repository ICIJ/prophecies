from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework_json_api import serializers
from prophecies.core.models.setting import Setting


class SettingSerializer(serializers.ModelSerializer):
    key = serializers.CharField()
    value = serializers.CharField()
    public = serializers.BooleanField()
    search_fields = ['key', 'value']
    ordering_fields = ['key']
    ordering = ['key']
    filterset_fields = ['key', 'value']

    class Meta:
        model = Setting
        fields = ['key', 'value', 'public']


class SettingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Setting.objects.none()
    serializer_class = SettingSerializer
    pagination_class = None
    permission_classes = []


    def get_queryset(self):        
        if not self.request.user.is_authenticated:
            return Setting.objects.public()
        else:
            return Setting.objects.all_with_env()
        

    def list(self, request, **kwargs):
        settings = self.get_queryset()
        serializer = SettingSerializer(settings, context={'request': request}, many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None, **kargs):
        try:
            setting = next(s for s in self.get_queryset() if s.key == pk)
        except StopIteration:
            raise NotFound()
        serializer = SettingSerializer(setting, context={'request': request}, many=False)
        return Response(serializer.data)
