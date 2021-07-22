from django.contrib.auth.models import User
from rest_framework import viewsets, serializers, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'is_staff']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False)
    def me(self, request, **kwargs):
        """
        Profile of the current user.
        """
        if not request.user.is_authenticated:
            raise PermissionDenied()
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)
