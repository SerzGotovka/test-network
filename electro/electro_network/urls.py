from django.urls import path, include
from .views import NetworkListView, NetworCountrykListView, NetworkProductView, ProductViewSet, NetworkDetail, HighDebtNetworksView, NetworkViewSet #QRCodeAPIView
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'network-edit', NetworkViewSet)
router.register(r'product-edit', ProductViewSet)


urlpatterns = [
    path('networks/', NetworkListView.as_view(), name='network-list'),  #URL для получения информации по всем объектам сети
    path('network/<int:pk>/', NetworkDetail.as_view(), name='network-detail'), # URL для обновления сети
    path('networks-country/', NetworCountrykListView.as_view(), name='networks-country-list'),  #URL для Информацию об объектах определённой страны (фильтр по названию)
    #http://127.0.0.1:8000/networks-country/?country=Беларусь

    path('networks-product/', NetworkProductView.as_view(), name='networks-product-list'), # URL для Все объекты сети, где можно встретить определенный продукт (фильтр по id продукта)
    #http://127.0.0.1:8000/networks-product/?product_id=1
   
    
    path('network-hightdebt/', HighDebtNetworksView.as_view(), name='networks-hightdebt'), # URL для просмотра статистики об объектах, задолженность которых превышает среднюю задолженность всех объектов 
    path('', include(router.urls)),
    #path('qrcode/', QRCodeAPIView.as_view(), name='create-qr-code'),
     

]