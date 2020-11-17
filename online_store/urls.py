from django.urls import path
from rest_framework.routers import DefaultRouter
from online_store.views import auth, shop, goods, doc

# router = DefaultRouter()
# router.register(r'docs', doc.DocViewSet, basename='docs')

urlpatterns = [
    path('login/', auth.login),

    path('shops/', shop.ShopView.as_view(), name='shops'),
    path('shops/<int:pk>', shop.ShopView.as_view(), name='single_shops'),

    path('goods/', goods.GoodView.as_view(), name='goods'),
    path('goods/<int:pk>', goods.SingleGoodView.as_view(), name='single_goods'),


    path('docs/', doc.DocViewSet.as_view({
        'get': 'list',
        'post': 'create'

    }), name='docs'),
    path('docs/<int:pk>', doc.DocViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='single_docs'),
]
