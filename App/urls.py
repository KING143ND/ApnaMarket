from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = "App"

urlpatterns = [
    path("", views.home, name="home"),
    path('product-detail/<str:title>/', views.product_detail, name='product-detail'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart,name='add-to-cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart,name='remove-from-cart'), 
    path('remove/<int:pk>/', views.cart_view,name='remove-from-cart'), 
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('address/remove/<int:pk>/', views.address_del, name='address_del'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', views.change_password, name='changepassword'),
    path('login/', views.login, name='login'),
    path('registration/', views.customerregistration, name='customerregistration'),
    path('logout/', views.logout, name="Logout"),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/filter=<str:data>', views.mobile, name='mobile_data'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/filter=<str:data>', views.laptop, name='laptop_data'),
    path('fashion/mens/', views.fashion_mens, name='fashion_mens'),
    path('fashion/mens/filter=<str:data>', views.fashion_mens, name='fashion_mens'),
    path('fashion/womens/', views.fashion_womens, name='fashion_womens'),
    path('fashion/womens/filter=<str:data>', views.fashion_womens, name='fashion_womens'),
    path('grocery/', views.grocery, name='grocery'),
    path('grocery/filter=<str:data>', views.grocery, name='grocery'),
    path('homeappliances/', views.home_appliances, name='home_appliances'),
    path('homeappliances/filter=<str:data>', views.home_appliances, name='home_appliances'),
    path('electricappliances/', views.electric_appliances, name='electric_appliances'),
    path('electricappliances/filter=<str:data>', views.electric_appliances, name='electric_appliances'),
    path('toys/', views.toys, name='toys'),
    path('toys/filter=<str:data>', views.toys, name='toys'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('search/', views.search, name="Search"),
    path('about/', views.about, name="Search"),
    path('contact/', views.contact, name="Search"),
    path('terms/', views.terms, name="Search"),
    path('privacy/', views.privacy, name="Search"),
    path('orders/download-invoice/<int:pk>/', views.download_invoice_view,name='download-invoice')
]
