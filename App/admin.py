from django.contrib import admin
from .models import *

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display =['name','user','address']
    
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display =['title','category','type']
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display =['user','product']
    
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display =['customer','user','product','ordered_date','status']
    
@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    list_display =['firstName','lastName','timeStamp']
    

admin.site.register(Coupon)