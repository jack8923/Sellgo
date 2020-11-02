import logging

from django.db import models
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

logger = logging.getLogger(__name__)


# class TimeStampable(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     created_by = models.CharField(max_length=256)
#     modified_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         abstract = True


class CreateRetrieveUpdateListModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, and `list()` actions.
    """
    pass


class RetrieveModelViewSet(
    mixins.RetrieveModelMixin,
    GenericViewSet,
):
    """
    A viewset that provides default `retrieve()` action.
    """
    pass


"""
Mixin to dynamically select only a subset of fields per DRF resource.
"""


class DynamicFieldsMixin(object):
    """
    A serializer mixin that takes an additional `omit_fields` argument that controls
    which fields should be displayed.
    """

    @property
    def fields(self):
        """
        Filters the fields according to the `omit_fields` context.
        Only for GET Requests.
        """
        logger.debug("In DynamicFieldsMixin")
        fields = super(DynamicFieldsMixin, self).fields

        if not hasattr(self, '_context'):
            # We are being called before a request cycle
            return fields

        # If request is not given or method is not `GET`, we return.
        request = self.context.get('request', None)
        if request is None or request.method != 'GET':
            return fields

        # Only filter if this is the root serializer, or if the parent is the
        # root serializer with many=True
        is_root = self.root == self
        parent_is_list_root = self.parent == self.root and getattr(self.parent, 'many', False)
        if not (is_root or parent_is_list_root):
            return fields

        # Retrieve omit_fields from context
        omit_fields = self.context.get('omit_fields')

        # Return if omit_fields is not given in context
        if omit_fields is None:
            return fields

        logger.debug("omit_fields: {omit_fields}".format(omit_fields=omit_fields))

        existing = set(fields.keys())
        omitted = set(filter(None, omit_fields))

        # Drop any fields that are in the `omit_fields` argument.
        for field in existing:
            if field in omitted:
                fields.pop(field, None)

        return fields