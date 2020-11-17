from django.contrib import admin
from online_store.models import GoodUnits, Good, Doc, DocType, Shop, DocGoods

# Register your models here.

admin.site.register(Shop)


@admin.register(GoodUnits)
class GoodUnitsAdmin(admin.ModelAdmin):
    """ Единицы измерения товара
    """
    list_display = ('pk', 'name')

    def get_name(self, obj):
        return obj.name


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    """ Товар
    """
    list_display = ('pk', 'name', 'unit')

    def get_unit(self, obj):
        return obj.unit


@admin.register(DocType)
class DocTypeAdmin(admin.ModelAdmin):
    """ Единицы измерения товара
    """
    list_display = ('pk', 'name')

    def get_name(self, obj):
        return obj.name


@admin.register(DocGoods)
class DocGoodsAdmin(admin.ModelAdmin):
    """ Товары в документе
    """
    list_display = ('id', 'doc', 'good', 'quantity')

    def get_doc(self, obj):
        return obj.type


class DocGoodsAdminInline(admin.TabularInline):
    model = DocGoods
    extra = 0
    fields = ('doc', 'good', 'quantity')
    can_delete = False
    show_change_link = True


@admin.register(Doc)
class DocAdmin(admin.ModelAdmin):
    """ Документы
    """
    list_display = ('id', 'shop', 'date', 'type', 'owner')
    inlines = [DocGoodsAdminInline]
