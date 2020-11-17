from django.db import transaction
from rest_framework import serializers

from online_store.models import Doc, DocGoods


class DocGoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocGoods
        fields = '__all__'


class DocSerializer(serializers.ModelSerializer):
    docgoods = DocGoodsSerializer(source='docgoods_set', many=True)

    class Meta:
        model = Doc
        fields = '__all__'


class DocCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doc
        fields = '__all__'

    def create(self, validated_data):
        with transaction.atomic():
            request = self.context.get('request')

            validated_data.update({'owner': request.user})
            instance = super().create(validated_data)

            docgoods = request.data.pop('docgoods', [])
            for item in docgoods:
                item.update({'doc': instance.id})

            dgs = DocGoodsSerializer(data=docgoods, many=True)
            dgs.is_valid(raise_exception=True)
            docgoods = dgs.save()

        return instance

    def update(self, instance, validated_data):

        with transaction.atomic():
            request = self.context.get('request')

            validated_data.update({'owner': request.user})
            instance = super().update(instance, validated_data)
            instance.refresh_from_db()

            docgoods = request.data.pop('docgoods', [])
            for item in docgoods:
                item.update({'doc': instance.id})

                dg_instance = DocGoods.objects.get(id=item.get('id'))

                serializer = DocGoodsSerializer(dg_instance, data=item, partial=self.partial)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        return instance
