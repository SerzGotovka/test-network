from .serializers import NetworkSerializer, ProductSerializer, ContactsSerializer, NetworkCreateSerializer
from .models import Network, Product, Contacts
from rest_framework import generics, permissions
from django.db.models import Avg
from rest_framework import viewsets

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .tasks import generate_qr_code_and_send_email

class NetworkListView(generics.ListAPIView):
    serializer_class = NetworkSerializer

    def get_queryset(self):
        return Network.objects.all()



class NetworCountrykListView(generics.ListAPIView):
    serializer_class = NetworkSerializer

    def get_queryset(self):
        country = self.request.query_params.get('country', None)
        name = self.request.query_params.get('name', None)

        queryset = Network.objects.all()

        if country:
            queryset = queryset.filter(contacts__contact__country=country)
        if name:
            queryset = queryset.filter(name=name)

        return queryset


class HighDebtNetworksView(generics.ListAPIView):
    serializer_class = NetworkSerializer

    def get_queryset(self):
        avg_debt = Network.objects.aggregate(avg_debt=Avg('debt'))['avg_debt']
        return Network.objects.filter(debt__gt=avg_debt)
    
class NetworkProductView(generics.ListAPIView):
    serializer_class = NetworkSerializer

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id', None)
        
        if product_id:
            queryset = Network.objects.filter(products__id=product_id)
        else:
            queryset = Network.objects.all()
        
        return queryset


class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkCreateSerializer
    http_method_names = ['post', 'delete', 'put']
    # permission_classes = (IsAuthenticated,)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['post', 'delete', 'put']
    # permission_classes = (IsAuthenticated,)


class NetworkDetail(generics.RetrieveAPIView):
    serializer_class = NetworkSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Network.objects.filter(staff__user=user)


class QRCodeAPIView(APIView):
    def post(self, request):
        serializer = ContactsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        contact_email = serializer.validated_data['email']
        contact_data = str(serializer.validated_data['contact'])

        # Вызвать задачу для генерации QR-кода и отправки его на электронную почту
        # generate_qr_code_and_send_email.delay(contact_email, contact_data)
        generate_qr_code_and_send_email(contact_email, contact_data)

        return Response({'message': 'QR-код будет отправлен на указанную электронную почту.'})

