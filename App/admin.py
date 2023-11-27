from django.contrib import admin
from .models import *

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display =['name','user','address']
    search_fields = ['name']
    
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display =['title','category','type']
    search_fields = ['title']
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display =['user','product']
    
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display =['customer','order_id','user','ordered_date','status']
    search_fields = ['order_id']
    
@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    list_display =['firstName','lastName','timeStamp']
    search_fields = ['firstName']

admin.site.register(Coupon)