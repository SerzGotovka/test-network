from rest_framework import serializers
from .models import Network, Address, Contacts, Staff, Product
from django.core.exceptions import ValidationError
from datetime import date


class AddressSerializer(serializers.ModelSerializer):
    """Серилизатор для модели адрес(Adress)"""
    class Meta:
        model = Address
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    """Серилизатор для модели сотрудники(Staff)"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Staff
        fields = ['name', 'user']

class ContactsSerializer(serializers.ModelSerializer):
    """Серилизатор для модели контакты(Contacts)"""
    contact = AddressSerializer()

    class Meta:
        model = Contacts
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """Серилизатор для модели продукты(Product)"""

    def validate_release_date(self, value):
        if value > date.today():
            raise ValidationError("Некорректная дата выхода продукта на рынок.")
        return value
    
    def validate(self, attrs):
        """ Validates or not incoming name length. """

        if len(attrs['name']) > 25:
            raise ValidationError({"detail": "Entity's name should contains maximum 25 symbols."})

        return attrs

    class Meta:
        model = Product
        fields = ['name', 'model', 'date_release']

    
class NetworkSerializer(serializers.ModelSerializer):
    """Серилизатор для модели сеть(Network)"""
    contacts = ContactsSerializer(many=False)
    products = ProductSerializer(many=True)
    staff = StaffSerializer(many=False)
    parent = serializers.PrimaryKeyRelatedField(queryset=Network.objects.all())

    class Meta:
        model = Network
        fields = ['id', 'type','name', 'products', 'parent', 'debt', 'staff', 'date_created', 'contacts']
        extra_kwargs = {
            "type": {
                "required": True
            },
            "name": {
                "required": True
            },
           
            "date_created": {
                "read_only": True
            }
        }

class NetworkCreateSerializer(serializers.ModelSerializer):
    """Серилизатор для модели сеть(Network)"""
    
    def validate_name(self, value):
        if len(value) > 50:
            raise serializers.ValidationError("Название сети должно содержать не более 50 символов.")
        return value

    contacts = ContactsSerializer(many=False, read_only=True)
    products = ProductSerializer(many=False, read_only=True)
    staff = StaffSerializer(many=False, read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Network.objects.all())

    
    class Meta:
        model = Network
        fields = ['id', 'type','name', 'products', 'parent', 'debt', 'staff', 'date_created', 'contacts']
        extra_kwargs = {
            "type": {
                "required": True
            },
            "name": {
                "required": True
            },
            "debt": {
                "read_only": True
            },
            "date_created": {
                "read_only": True
            }
        }
    