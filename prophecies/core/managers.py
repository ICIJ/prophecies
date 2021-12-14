from actstream.managers import ActionManager, stream
from django.contrib.contenttypes.models import ContentType

class ExtendedActionManager(ActionManager):

    def filter_actor_params(self, actor):
        content_type = ContentType.objects.get_for_model(actor)
        id = actor.id
        return dict(actor_content_type=content_type, actor_object_id=id)

    def filter_target_params(self, target):
        content_type = ContentType.objects.get_for_model(target)
        id = target.id
        return dict(target_content_type=content_type, target_object_id=id)

    def filter_action_object_params(self, action_object):
        content_type = ContentType.objects.get_for_model(action_object)
        id = action_object.id
        return dict(action_object_content_type=content_type, action_object_object_id=id)

    @stream
    def filter_actor(self, actor):
        return self.filter(**self.filter_actor_params(actor))

    @stream
    def filter_target(self, target):
        return self.filter(**self.filter_target_params(target))

    @stream
    def filter_action_object(self, action_object):
        return self.filter(**self.filter_action_object_params(action_object))

    @stream
    def filter_actor_content_type(self, content_type_filter):
        content_types = ContentType.objects.filter(model=content_type_filter)
        if len(content_types) == 1:
            return self.filter(actor_content_type = content_types[0])
        raise ValueError("Illegal argument value %s" % content_type_filter)