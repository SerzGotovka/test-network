from django.contrib import admin, messages
from django.urls import reverse
from django.utils.safestring import mark_safe
from mptt.admin import MPTTModelAdmin
from .models import Address, Staff, Contacts, Product, Network
from .tasks import async_clear_debt

@admin.register(Network)
class NetworkAdmin(MPTTModelAdmin):
    list_display = ['id', 'type','name', 'products_list', 'provider_link', 'debt', 'date_created', 'contacts']
    list_display_links = ['type','name', 'products_list', 'provider_link']
    actions = ['clear_debt']
    readonly_fields = ['provider_link']

    def provider_link(self, obj):
        if obj.parent:
            url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.parent.id])
            link = '<a href="%s">%s</a>' % (url, obj.parent)
            return mark_safe(link)
        return None

    provider_link.short_description = 'Поставщик'
    
    
    admin.action(description='Очиcтить задолженность перед поставщиком')
    def clear_debt(modeladmin, request, queryset):
        if len(queryset) > 20:
            async_clear_debt.delay(list(queryset.values('id')))
            return
        queryset.update(debt=0)

    

@admin.register(Address)
class AdressAdmin(admin.ModelAdmin):
    list_display = ['id', 'country', 'city']
    list_filter = ('city',)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'networks']


@admin.register(Product)
class productAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'model', 'date_release']

@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ['id', 'email','contact']

