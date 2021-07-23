from constance.backends.database.models import Constance
from django.shortcuts import get_object_or_404
from rest_framework import permissions, serializers, viewsets
from rest_framework.response import Response

class SettingSerializer(serializers.ModelSerializer):
    key = serializers.CharField()
    value = serializers.CharField()

    class Meta:
        model = Constance
        fields = ['key', 'value']


class SettingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Constance.objects.all()
    serializer_class = SettingSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def retrieve(self, request, pk=None):
        queryset = Constance.objects.all()
        setting = get_object_or_404(queryset, key=pk)
        serializer = SettingSerializer(setting)
        return Response(serializer.data)
