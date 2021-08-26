from actstream.models import Action
from hashlib import md5
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from prophecies.apps.api.views.action import ActionSerializer
from rest_framework import exceptions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_json_api import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    email_md5 = serializers.SerializerMethodField()
    csrf_token = serializers.SerializerMethodField()

    def get_email_md5(self, user):
        return md5(user.email.encode()).hexdigest()

    def get_csrf_token(self, user):
        request = self.context.get('request')
        if request.user == user:
            return str(csrf(request).get('csrf_token'))

    class Meta:
        model = User
        fields = ['id', 'url', 'first_name', 'last_name', 'username',
                    'email_md5', 'is_staff', 'csrf_token']


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects
    serializer_class = UserSerializer
    search_fields = ['first_name', 'last_name', 'username']
    ordering = ['-id']
    ordering_fields = ['id', 'first_name', 'last_name', 'username']
    filterset_fields = {
       'username': ('icontains', 'exact', 'iexact', 'contains', 'in'),
       'is_staff': ('exact',),
    }

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise exceptions.NotFound()

    @action(methods=['get'], detail=True)
    def actions(self, request, pk=None, **kwargs):
        queryset = self.get_user(pk).actor_actions.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ActionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ActionSerializer(page, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def me(self, request, **kwargs):
        """
        Profile of the current user.
        """
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)
