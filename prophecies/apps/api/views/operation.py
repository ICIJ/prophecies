import json

from io import BytesIO
from rest_framework import exceptions, serializers, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_json_api.parsers import JSONParser

from prophecies.apps.api.views.task_record_review import TaskRecordReviewViewSet
from prophecies.apps.api.views.user_notification import UserNotificationViewSet

MODEL_VIEWS_MAPPING = {
    'TaskRecordReview': TaskRecordReviewViewSet,
    'UserNotification': UserNotificationViewSet
}

class PayloadValueFieldSerializer(serializers.Serializer):
    data = serializers.DictField()

    def validate_data(self, value):
        if 'type' not in value:
            raise serializers.ValidationError("Payload data must define a `type`")
        if value['type'] not in MODEL_VIEWS_MAPPING:
            types = ', '.join(MODEL_VIEWS_MAPPING.keys())
            raise serializers.ValidationError("Payload type must be one of: %s" % types)
        return value


class PayloadFieldSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    value = PayloadValueFieldSerializer(required=True)


class OperationFieldSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    method = serializers.ChoiceField(required=True, choices=['update'])
    payload = serializers.CharField(required=True)


class OperationSerializer(serializers.Serializer):
    operations = OperationFieldSerializer(many=True, required=True)
    payloads = PayloadFieldSerializer(many=True, required=True)


    def validate_operations(self, value):
        for operation in value:
            payload_id = operation['payload']
            # Validate the operation's payload exists
            if not self.find_payload(payload_id):
                error = "Payload %s cannot be found in the `payloads` list"
                raise serializers.ValidationError(error % payload_id)
            # Validate the operation's payload data
            serializer = self.payload_serializer_from_operation(operation)
            serializer.is_valid(raise_exception=True)
        return value


    def find_payload(self, id):
        try:
            payloads = self.get_initial().get('payloads', [])
            return next(p for p in payloads if p['id'] == id)
        except StopIteration:
            return None


    def find_payload_view(self, id):
        payload = self.find_payload(id)
        if payload:
            type = payload['value']['data']['type']
            if type in MODEL_VIEWS_MAPPING:
                return MODEL_VIEWS_MAPPING[type]
        return None


    def parse_payload_value(self, payload, pk = None):
        payload_value = payload['value']
        payload_view = self.find_payload_view(payload['id'])
        payload_value['data']['id'] = pk
        context = { 'request': self.context['request'], 'view': payload_view }
        stream = BytesIO(json.dumps(payload_value).encode("utf-8"))
        return JSONParser().parse(stream, None, context)


    def payload_instance(self, payload, pk, raise_exception=False):
        payload_id = payload['id']
        payload_view = self.find_payload_view(payload_id)
        instanciated_view = payload_view(request=self.context['request'])
        try:
            return instanciated_view.get_queryset().get(pk=pk)
        except instanciated_view.get_queryset().model.DoesNotExist:
            if not raise_exception:
                return None
            raise exceptions.NotFound('The resource cannot be found')

    def payload_serializer_from_operation(self, operation):
        payload = self.find_payload(operation['payload'])
        payload_view = self.find_payload_view(operation['payload'])

        request = self.context['request']
        context = { 'request': request, 'view': payload_view }
        instance_pk = operation['id']

        payload_data = self.parse_payload_value(payload, instance_pk)
        payload_instance = self.payload_instance(payload, instance_pk, raise_exception=True)
        payload_view().check_object_permissions(request, payload_instance)
        return payload_view.serializer_class(payload_instance, data=payload_data, context=context)

    def create(self, validated_data):
        for operation in validated_data['operations']:
            serializer = self.payload_serializer_from_operation(operation)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return {}

class OperationViewSet(viewsets.GenericViewSet):
    """
    To create bulk operations. Each operation is defined by a list of
    `operations` and a list of `payloads` to apply to resources. Each resource
    is identified in the `operations` attribute with and `id` and each `payload`
    uses an arbitrary id as well.

    **Currently this endpoint only supports `update` operations.**
    """
    serializer_class = OperationSerializer
    resource_name = 'Operation'
    http_method_names = ['post', 'head']
    permission_classes = [IsAuthenticated]


    def create(self, request):
        context = {'request': request, 'view': self}
        serializer = OperationSerializer(data=request.data, many=False, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data)
