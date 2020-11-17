from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _

User = get_user_model()


# Create your models here.


class NameMixin(models.Model):
    name = models.CharField(_('Наименование'), max_length=255, null=False, blank=False, default=None)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class GoodUnits(NameMixin, TimeStampedModel):
    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'


class Good(NameMixin, TimeStampedModel):
    unit = models.ForeignKey(GoodUnits, verbose_name='Единаца измерения', on_delete=models.deletion.CASCADE)

    #  Штрихкода товара
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Shop(NameMixin, TimeStampedModel):
    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class DocType(NameMixin, TimeStampedModel):
    class Meta:
        verbose_name = 'Тип документа'
        verbose_name_plural = 'Типы документов'


class Doc(TimeStampedModel):
    shop = models.ForeignKey(Shop, verbose_name='Магазин', on_delete=models.deletion.CASCADE)
    date = models.DateField(_('Дата'), blank=True, null=True, auto_now_add=True)
    type = models.ForeignKey(DocType, verbose_name='Тип документа', on_delete=models.deletion.CASCADE)
    owner = models.ForeignKey(User, verbose_name='Владелец', null=True, on_delete=models.deletion.CASCADE)

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'


class DocGoods(TimeStampedModel):
    doc = models.ForeignKey(Doc, verbose_name='Документ', on_delete=models.deletion.CASCADE)
    good = models.ForeignKey(Good, verbose_name='Товар', on_delete=models.deletion.CASCADE)
    quantity = models.IntegerField(null=True)

    class Meta:
        verbose_name = verbose_name_plural = 'Товары в документа'
