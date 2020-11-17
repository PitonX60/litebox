from rest_framework import permissions
from rest_framework.generics import get_object_or_404, RetrieveUpdateDestroyAPIView, ListCreateAPIView

from online_store.models import Good, GoodUnits
from online_store.serializers.goods import GoodSerializer


class GoodView(ListCreateAPIView):
    serializer_class = GoodSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Good.objects.filter(name__icontains=query)

    def perform_create(self, serializer):
        unit = get_object_or_404(
            GoodUnits,
            id=self.request.data.get('unit')
        )
        return serializer.save(unit=unit)


class SingleGoodView(RetrieveUpdateDestroyAPIView):
    queryset = Good.objects.all()
    serializer_class = GoodSerializer
    permission_classes = [permissions.IsAuthenticated]
