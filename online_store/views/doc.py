import datetime
from django.db import transaction
from django.http import Http404, HttpResponseBadRequest
from rest_framework import viewsets, permissions, status as http_status
from rest_framework.response import Response

from online_store.models import Doc
from online_store.serializers.doc import DocSerializer, DocCreateUpdateSerializer


class DocViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocSerializer
    queryset = Doc.objects.all()

    def get_serializer_class(self):
        if self.request.method not in ['PUT', 'PATCH']:
            return super().get_serializer_class()
        return DocCreateUpdateSerializer

    def list(self, request, *args, **kwargs):
        qwhere, qparam = [], []

        try:
            start_date = request.query_params.get('start_date', None)
            if start_date:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
                qwhere.append('doc.date >= %s')
                qparam.append(start_date)

            end_date = request.query_params.get('end_date', None)
            if end_date:
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
                qwhere.append('doc.date <= %s')
                qparam.append(end_date)

        except Exception as ex:
            return HttpResponseBadRequest(ex)

        doc_type_id = request.query_params.get('type', None)
        if doc_type_id:
            qwhere.append('doc.type_id = %s')
            qparam.append(doc_type_id)

        shop_id = request.query_params.get('shop', None)
        if shop_id:
            qwhere.append('doc.shop_id = %s')
            qparam.append(shop_id)

        user_id = request.query_params.get('user', None)
        if user_id:
            qwhere.append('doc.owner_id = %s')
            qparam.append(user_id)

        query = 'SELECT * FROM online_store_doc AS doc'
        if qwhere:
            query = ' '.join([query] + ['WHERE'] + [' AND '.join(qwhere)])

        queryset = Doc.objects.raw(query, qparam)

        serializer = DocSerializer(queryset, many=True)
        data = serializer.data
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        doc = Doc.objects.raw('SELECT * FROM online_store_doc WHERE online_store_doc.id = %s', [kwargs.get('pk')])
        if len(doc) == 0:
            raise Http404('No %s matches the given query.' % Doc._meta.object_name)

        serializer = DocSerializer(doc[0])
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = DocCreateUpdateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        doc = serializer.save()
        return Response(DocSerializer(doc).data, status=http_status.HTTP_201_CREATED)
