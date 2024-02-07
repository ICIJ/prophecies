from hashlib import md5
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from prophecies.apps.api.views.action import ActionSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema
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
        fields = ['id', 'url', 'first_name', 'last_name', 'username', 'email',
                  'email_md5', 'is_staff', 'is_superuser', 'csrf_token', 'last_login']


@extend_schema_view(
    list=extend_schema(
        operation_id="List Users",
        description="Returns a list of Users.",
    ),
    retrieve=extend_schema(
        operation_id="Get User",
        description="Get a single User using an ID.",
    ),
)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Users list, also known as checkers.
    """

    queryset = User.objects
    serializer_class = UserSerializer
    search_fields = ['first_name', 'last_name', 'username']
    ordering = ['-id']
    ordering_fields = ['id', 'first_name', 'last_name', 'username']
    filterset_fields = {
        'username': ('icontains', 'exact', 'iexact', 'contains', 'in'),
        'is_staff': ('exact',)
    }

    def get_object(self):
        try:
            pk = self.kwargs['pk']
            if str(pk).isdigit():
                return User.objects.get(pk=pk)
            return User.objects.get(username=pk)
        except User.DoesNotExist:
            raise exceptions.NotFound()

    @action(methods=['get'], detail=True)
    def actions(self, request, pk=None, **kwargs):
        """
        List of actions performed by the user.
        """
        # Change the resource name for the current view to ensure the "type" of
        # the serialized data is correct (the render uses this view property
        # to find the current type).
        self.resource_name = 'Action'
        queryset = self.get_object().actor_actions.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ActionSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = ActionSerializer(page, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def me(self, request, **kwargs):
        """
        Profile of the current user.
        """
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)
