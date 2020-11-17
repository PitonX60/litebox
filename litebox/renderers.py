from rest_framework.renderers import JSONRenderer
from django.db.models.query import QuerySet, RawQuerySet


class JSONTotalRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if hasattr(data, 'serializer'):

            total = 1
            if isinstance(data.serializer.instance, QuerySet) or isinstance(data.serializer.instance, RawQuerySet):
                total = len(data.serializer.instance)

            data = {
                'data': data,
                'total': total
            }
        return super().render(data, accepted_media_type, renderer_context)
