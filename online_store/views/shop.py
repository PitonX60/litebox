from rest_framework import permissions, status as http_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from online_store.models import Shop
from online_store.serializers.shop import ShopSerializer


# Create your views here.

class ShopView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            shop = get_object_or_404(Shop.objects.all(), pk=pk)
            return Response(ShopSerializer(shop).data)

        query = request.query_params.get('q', '')
        qs = Shop.objects.filter(name__icontains=query)
        return Response(ShopSerializer(qs, many=True).data)

    def post(self, request):
        serializer = ShopSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)
        shop = serializer.save()
        return Response(ShopSerializer(shop).data, status=http_status.HTTP_201_CREATED)

    def put(self, request, pk):
        serializer = ShopSerializer(
            instance=get_object_or_404(Shop.objects.all(), pk=pk),
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        shop = serializer.save()
        return Response(ShopSerializer(shop).data)

    def delete(self, request, pk):
        shop = get_object_or_404(Shop.objects.all(), pk=pk)
        shop.delete()
        return Response(status=http_status.HTTP_204_NO_CONTENT)
