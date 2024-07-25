from django.contrib import admin
from . models import Order, OrderItem



class OrderAdminSite(admin.ModelAdmin):
    model = Order

    list_display = ('user', 'payment_mode', 'tracking_no' ,'status')


    actions = ['out_for_shipping', 'pending']

    def out_for_shipping(self,request,queryset):
        queryset.update(status='out for shipping')

    def pending(self,request,queryset):
        queryset.update(status='pending')

# Register your models here.
admin.site.register(Order, OrderAdminSite)
admin.site.register(OrderItem)
