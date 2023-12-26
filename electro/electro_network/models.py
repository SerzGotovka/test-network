from django.db import models
from mptt.models import MPTTModel
from django.utils.translation import gettext as _
from mptt.fields import TreeForeignKey
from django.contrib.auth.models import User


class Address(models.Model):
    """ Address model. """

    country = models.CharField(null=True, blank=True, max_length=100)
    city = models.CharField(null=True, blank=True, max_length=100)
    street = models.CharField(null=True, blank=True, max_length=100)
    house = models.PositiveSmallIntegerField(null=True, blank=True)
   
    

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адрес'

    def __str__(self):
        return f'{self.country}{self.city}{self.street}{self.house}'

class Staff(models.Model):
    name = models.CharField(max_length=255, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    networks = models.ForeignKey("Network", on_delete=models.CASCADE, related_name='staff')

    class Meta:
        verbose_name = 'Сотрудники'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.name}'

class Contacts(models.Model):
    """ Contacts model. """

    email = models.EmailField(blank=True, null=True, unique=True, max_length=256)
    contact = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='contacts')
    

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f'{self.contact} - email:{self.email}'
    


class Network(MPTTModel):
    """ Network model. """

    FACTORY_TYPE = "Завод"
    DISTRIBUTOR_TYPE = "Дистрибьютор"
    DEALER_TYPE = "Дилерский центр"
    RETAIK_TYPE = "Крупная розничная сеть"
    ENTEPRENEUR_TYPE = "Индивидуальный предприниматель"
        
    type_choises = [
        (FACTORY_TYPE, _("Завод")),
        (DISTRIBUTOR_TYPE, _("Дистрибьютор")),
        (DEALER_TYPE, _("Дилерский центр")),
        (RETAIK_TYPE, _("Крупная розничная сеть")),
        (ENTEPRENEUR_TYPE, _("Индивидуальный предприниматель"))
    ]

    
    type = models.CharField(max_length=50, choices=type_choises)
    name = models.CharField(max_length=50, blank=True)
    products = models.ManyToManyField("Product", default=None, related_name='entity', blank=True)
    parent = TreeForeignKey('self',  on_delete=models.SET_NULL, null=True, blank=True, related_name='provider_network')
    debt = models.DecimalField(default=0, null=True, blank=True, max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    contacts = models.OneToOneField(Contacts, on_delete=models.CASCADE, null=True, blank=True, related_name='contact_network')

    class MPTTMeta:
        verbose_name = "Звено сети"
        verbose_name_plural = "Звено сети"


    def products_list(self):
        return len([product for product in self.products.all()]) if [product for product in self.products.all()] else 0
    
    

    def __str__(self):
        return f'{self.type}'


    
class Product(models.Model):
    """ Product model. """

    name = models.CharField(null=True, blank=True, max_length=256)
    model = models.CharField(null=True, blank=True, max_length=256)
    date_release = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Продукты'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.name} {self.model}'    
