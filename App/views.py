from django.shortcuts import render, redirect
from . models import *
from django.contrib.auth.models import User, auth
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def home(request):
    products=Product.objects.all().order_by("?")
    mobiles=Product.objects.filter(category="M").order_by("?")
    laptops=Product.objects.filter(category="L").order_by("?")
    mfashion=Product.objects.filter(category="MF").order_by("?")
    wfashion=Product.objects.filter(category="WF").order_by("?")
    grocery=Product.objects.filter(category="G").order_by("?")
    home=Product.objects.filter(category="H").order_by("?")
    electronics=Product.objects.filter(category="E").order_by("?")
    toys=Product.objects.filter(category="T").order_by("?")
    medicine=Product.objects.filter(category="Md").order_by("?")
    fashion=mfashion | wfashion
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
    return render(request, 'home.html',{'products':products,'mobiles':mobiles,'laptops':laptops,'electronics':electronics,'mfashion':mfashion,'wfashion':wfashion,'grocery':grocery,'home':home,'toys':toys,'medicine':medicine,'fashion':fashion,'product_count_in_cart':product_count_in_cart})

def product_detail(request,title):
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
    products=Product.objects.filter(title = title)
    allprod = Product.objects.all()
    index_prod = {'allprod':allprod,'products':products,'product_count_in_cart':product_count_in_cart}
    return render(request, 'productdetail.html', index_prod)


@login_required(login_url="/login")
def add_to_cart(request,pk):
    user=request.user
    product_id=request.GET.get("prod_id")
    product=Product.objects.get(pk=product_id)
    Cart(user=user,product=product).save()
    products=Product.objects.filter(pk = pk)
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=1
    product=Product.objects.get(pk=pk)
    response = render(request, 'productdetail.html',{'products':products,'product_count_in_cart':product_count_in_cart})
    response = render(request, 'addtocart.html')
    messages.success(request, product.title + ' added to cart successfully!')
    response = redirect(f"/cart")
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids=="":
            product_ids=str(pk)
        else:
            product_ids=product_ids+"|"+str(pk)
        response.set_cookie('product_ids', product_ids)
    else:
        response.set_cookie('product_ids', pk)
    return response

def cart_view(request):
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
        
    products=None
    product_price=0
    total_price=0
    shipping_price=0
    final_price=0
    saving_price=0
    discount_pct=0
    coupon_price=0
    coupon=0
    coupon_code=0
    coupon_code2=Coupon.objects.all()
    cp_code=0
    applied_c_price=0
    final_saving_price=0
    if request.user.is_authenticated:
            user=request.user
            products=Cart.objects.filter(user=user)
            for p in products:
                total_price=(total_price+(p.product.discounted_price))
                product_price=(product_price+(p.product.selling_price))
            if total_price<=99:
                shipping_price=99
            elif total_price<=199:
                shipping_price=95
            elif total_price<=299:
                shipping_price=89
            elif total_price<=399:
                shipping_price=85
            elif total_price<=499:
                shipping_price=79
            elif total_price==500:
                shipping_price=75
            elif total_price<=799:
                shipping_price=70
            elif total_price<=999:
                shipping_price=55
            elif total_price==1000:
                shipping_price=50
            elif total_price<=1499:
                shipping_price=25
            elif total_price<=1999:
                shipping_price=19
            else:
                shipping_price=0
            if request.method == 'POST':  
                coupon = request.POST['coupon'] 
                cp_code=Coupon.objects.filter(code=coupon)
                if cp_code:
                    for p in Coupon.objects.filter(code=coupon):
                        print(p.discount)
                        print(int((p.discount*10/100)+p.discount))
                        print(total_price)
                        if int((p.discount*10/100)+p.discount)>(total_price):
                            messages.error(request,f"Add item worth Rs.{int((p.discount*10/100)+p.discount)-total_price} in your Cart for Applying Coupon {coupon}")
                        else:
                            coupon_price=(p.discount)
                            coupon_code=(p.code)
                            messages.success(request,f"Coupon {coupon} has been Successfully Appied")
                            
                else:
                    coupon_price=0
                    coupon_code=0
                    messages.error(request,f"Coupon {coupon} has been Invalid")
            final_price=total_price+shipping_price-coupon_price 
            saving_price=product_price-total_price
            final_saving_price=product_price-total_price+coupon_price
            discount_pct=125/45*100
    print(final_price)
    context={'products':products,'saving_price':saving_price,'product_price':product_price, 'total_price':total_price,'shipping_price':shipping_price,'final_price':final_price,'coupon_price':coupon_price,'discount_pct':discount_pct,'applied_c_price':applied_c_price,'product_count_in_cart':product_count_in_cart,'coupon':coupon,'coupon_code':coupon_code,'coupon_code2':coupon_code2,'cp_code':cp_code,'final_saving_price':final_saving_price}
    return render(request,'addtocart.html',context)
 
 
def remove_from_cart(request,pk):
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        product_id_in_cart=product_ids.split('|')
        product_id_in_cart=list(set(product_id_in_cart))
        user=request.user
        product_id=request.GET.get("prod_id")
        product=Product.objects.get(pk=product_id)
        Cart.objects.filter(user=user,product=product).delete()
        products=Cart.objects.all().filter(id__in = product_id_in_cart)
        products=Cart.objects.filter(user=user)
        for p in products:
            total=total+p.product.discounted_price
            print(p.product.discounted_price)
        value=""
        for i in range(len(product_id_in_cart)):
            if i==0:
                value=value+product_id_in_cart[0]
            else:
                value=value+"|"+product_id_in_cart[i]
        product=Product.objects.all().get(pk=pk)
        response = render(request, 'addtocart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})
        if total==0:
            messages.success(request,'Cart is now empty... Add your Favourites Items on Cart!')
            response = redirect("/cart")
        else:
            messages.success(request, product.title + ' Removed to Cart Successfully!')
            response = redirect("/cart")
        if value=="":
            response.delete_cookie('product_ids')
        response.set_cookie('product_ids',value)
        return response 
    
@login_required(login_url="/login")
def buy_now(request):
    user=request.user
    Cart.objects.filter(user=request.user).delete()
    product_id=request.GET.get("prod_id2")
    product=Product.objects.get(pk=product_id)
    Cart(user=user,product=product).save()
    return redirect ("/checkout")

@login_required(login_url="/login")
def profile(request):
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
    if request.method == 'POST':
        inputName = request.POST.get("inputName","default")
        inputEmail = request.POST.get("inputEmail","default")
        inputAddress = request.POST.get("inputAddress","default")
        inputAddress2 = request.POST.get("inputAddress2","default")
        inputCity = request.POST.get("inputCity","default")
        inputState = request.POST.get("inputState","default")
        inputZip = request.POST.get("inputZip","default")
        inputGender = request.POST.get("inputGender","default")
        inputPhone = request.POST.get("inputPhone","default")
        inputAge = request.POST.get("inputAge","default")
        inputType = request.POST.get("inputType","default")
        if inputAge=='':
            inputAge=0
 
        if Customer.objects.filter(email=inputEmail).exists():
            messages.error(request,"You already added this Email!") 
        elif Customer.objects.filter(phone=inputPhone).exists():
            messages.error(request,"You already added this Mobile Number!") 
        elif len(inputName)==0:
            messages.error(request, "Please Add Your Name!")  
        elif len(inputEmail)==0:
            messages.error(request, "Please Add Your Email!")  
        elif len(inputAddress)==0:
            messages.error(request, "Please Add Your Address!")  
        elif len(inputCity)==0:
            messages.error(request, "Please Add Your City!")    
        elif len(inputZip)==0:
            messages.error(request, "Please Add Your Pincode!")   
        elif len(inputName)<3:
            messages.error(request, "Your Name cannot be less than 3 Characters!")
        elif len(inputName)>40:
            messages.error(request, "Your Name cannot be greater than 40 Characters!")
        elif len(inputEmail)<5:
            messages.error(request, "Your Email cannot be less than 5 Characters!")
        elif len(inputEmail)>50:
            messages.error(request, "Your Email cannot be greater than 50 Characters!")
        elif len(inputCity)<3:
            messages.error(request, "Your City cannot be less than 3 Characters!")
        elif len(inputCity)>50:
            messages.error(request, "Your City cannot be greater than 50 Characters!")
        elif len(inputAddress)<3:
            messages.error(request, "Your Address cannot be less than 3 Characters!")
        elif len(inputAddress)>200:
            messages.error(request, "Your Address cannot be greater than 200 Characters!")
        elif len(inputAddress2)>200:
            messages.error(request, "Your Landmark cannot be greater than 200 Characters!")
        elif len(inputZip)<6:
            messages.error(request, "Your Pincode must be only 6 Characters!")
        elif len(inputZip)>6:
            messages.error(request, "Your Pincode must be only 6 Characters!")
        elif len(inputPhone)<10:
            messages.error(request, "Your Mobile Number must be only 10 Digits!")
        elif len(inputPhone)>10:
            messages.error(request, "Your Mobile Number must be only 10 Digits!")
        else:
            myuser = Customer.objects.create(user=request.user, name=inputName, email=inputEmail, locality=inputAddress, landmark=inputAddress2, city=inputCity, state=inputState, zipcode=inputZip, gender=inputGender, phone=inputPhone, age=inputAge, address=inputType)
            messages.success(request, f"Congratulations...{inputName}! Your Address has been Updated Sucessfully!")
            myuser.save()
            return redirect("/address")
    return render(request, 'profile.html',{'product_count_in_cart':product_count_in_cart,'active':'btn-primary'})


@login_required(login_url="/login")
def address(request):
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
    profile=Customer.objects.filter(user=request.user)
    return render(request, 'address.html',{'profile':profile,'product_count_in_cart':product_count_in_cart})


def address_del(request,pk):
    customer=Customer.objects.get(pk=pk)
    customer.delete()
    messages.success(request, "Your Address has been Deleted Sucessfully!")
    return redirect("/")


@login_required(login_url="/login")
def orders(request):
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
    op=OrderPlaced.objects.filter(user=request.user).order_by("ordered_date").reverse
    return render(request, 'orders.html',{'product_count_in_cart':product_count_in_cart,'op':op})


@login_required(login_url="/login")
def change_password(request):
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepassword.html',{'product_count_in_cart':product_count_in_cart,'form': form})


def mobile(request,data=None):
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
       
    mob_brand= data=='Oneplus' or data=='Apple' or data=='Samsung' or data=='Vivo' or data=='Oppo' or data=='Redmi' or data=='Realme' or data=='Google'    
    if data==None:
        mobiles=Product.objects.filter(category="M").order_by('?').reverse()   
    elif mob_brand:
        mobiles=Product.objects.filter(category="M").filter(brand=data)
    elif data=='low_to_high':
        mobiles=Product.objects.filter(category="M").order_by('discounted_price')
    elif data=='high_to_low':
        mobiles=Product.objects.filter(category="M").order_by('discounted_price').reverse()
    elif data=='customer_rating':
        mobiles=Product.objects.filter(category="M").order_by('rating').reverse()
    elif data=='customer_review':
        mobiles=Product.objects.filter(category="M").order_by('review').reverse()
    elif data=='below_10000':
        mobiles=Product.objects.filter(category="M").filter(discounted_price__lt=10000).order_by('discounted_price').reverse()
    elif data=='below_20000':
        mobiles=Product.objects.filter(category="M").filter(discounted_price__lte=20000).order_by('discounted_price').reverse()
    elif data=='below_30000':
        mobiles=Product.objects.filter(category="M").filter(discounted_price__lte=30000).order_by('discounted_price').reverse()
    elif data=='below_50000':
        mobiles=Product.objects.filter(category="M").filter(discounted_price__lt=50000).order_by('discounted_price').reverse()
    else:
        mobiles=Product.objects.filter(category="M").filter(discounted_price__gt=50000).order_by('discounted_price')   
    return render(request, 'mobile.html',{'mobiles':mobiles,'product_count_in_cart':product_count_in_cart})


def laptop(request,data=None):
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
    lap_brand= data=='Acer' or data=='Apple' or data=='HP' or data=='Lenovo' or data=='Asus' or data=='Dell' or data=='MSI' or data=='Samsung'    
    if data==None:
        laptops=Product.objects.filter(category="L").order_by('?').reverse()
    elif lap_brand:
        laptops=Product.objects.filter(category="L").filter(brand=data)
    elif data=='low_to_high':
        laptops=Product.objects.filter(category="L").order_by('discounted_price')
    elif data=='high_to_low':
        laptops=Product.objects.filter(category="L").order_by('discounted_price').reverse()
    elif data=='customer_rating':
        laptops=Product.objects.filter(category="L").order_by('rating').reverse()
    elif data=='customer_review':
        laptops=Product.objects.filter(category="L").order_by('review').reverse()
    elif data=='below_20000':
        laptops=Product.objects.filter(category="L").filter(discounted_price__lt=20000).order_by('discounted_price').reverse()
    elif data=='below_30000':
        laptops=Product.objects.filter(category="L").filter(discounted_price__lte=30000).order_by('discounted_price').reverse()
    elif data=='below_40000':
        laptops=Product.objects.filter(category="L").filter(discounted_price__lte=40000).order_by('discounted_price').reverse()
    elif data=='below_50000':
        laptops=Product.objects.filter(category="L").filter(discounted_price__lt=50000).order_by('discounted_price').reverse()
    else:
        laptops=Product.objects.filter(category="L").filter(discounted_price__gt=50000).order_by('discounted_price')
    return render(request, 'laptop.html',{'laptops':laptops,'product_count_in_cart':product_count_in_cart})


def fashion_mens(request,data=None):
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
    mf_cat= data=='T-Shirts' or data=='Shirts' or data=='Winter_Wears' or data=='Blazers' or data=='Suits' or data=='Jeans' or data=='Trousers' or data=='Trackpants' or data=='Shoes' or data=='Slippers' or data=='Wallets' or data=='Watches' or data=='Sunglasses' or data=='Belts' or data=='Jewellery'   
    if data==None:
        mens=Product.objects.filter(category="MF").order_by('?').reverse()
    elif mf_cat:
        mens=Product.objects.filter(category="MF").filter(type=data)
    elif data=='low_to_high':
        mens=Product.objects.filter(category="MF").order_by('discounted_price')
    elif data=='high_to_low':
        mens=Product.objects.filter(category="MF").order_by('discounted_price').reverse()
    elif data=='customer_rating':
        mens=Product.objects.filter(category="MF").order_by('rating').reverse()
    elif data=='customer_review':
        mens=Product.objects.filter(category="MF").order_by('review').reverse()
    elif data=='below_100':
        mens=Product.objects.filter(category="MF").filter(discounted_price__lt=100).order_by('discounted_price').reverse()
    elif data=='below_200':
        mens=Product.objects.filter(category="MF").filter(discounted_price__lte=200).order_by('discounted_price').reverse()
    elif data=='below_500':
        mens=Product.objects.filter(category="MF").filter(discounted_price__lte=500).order_by('discounted_price').reverse()
    elif data=='below_1000':
        mens=Product.objects.filter(category="MF").filter(discounted_price__lt=1000).order_by('discounted_price').reverse()
    elif data=='below_2000':
        mens=Product.objects.filter(category="MF").filter(discounted_price__lt=2000).order_by('discounted_price').reverse()
    else:
        mens=Product.objects.filter(category="MF").filter(discounted_price__gt=2000).order_by('discounted_price')
    return render(request, 'fashion_mens.html', {'mens':mens,'product_count_in_cart':product_count_in_cart})


def fashion_womens(request,data=None):
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
    wf_cat= data=='T-Shirts' or data=='Sarees' or data=='Winter_Wears' or data=='Tops' or data=='Kurtas' or data=='Jeans' or data=='Trousers' or data=='Trackpants' or data=='Shoes' or data=='Slippers' or data=='Purse' or data=='Watches' or data=='Sunglasses' or data=='Belts' or data=='Jewellery'   
    if data==None:
        womens=Product.objects.filter(category="WF").order_by('?').reverse()
    elif wf_cat:
        womens=Product.objects.filter(category="WF").filter(type=data)
    elif data=='low_to_high':
        womens=Product.objects.filter(category="WF").order_by('discounted_price')
    elif data=='high_to_low':
        womens=Product.objects.filter(category="WF").order_by('discounted_price').reverse()
    elif data=='customer_rating':
        womens=Product.objects.filter(category="WF").order_by('rating').reverse()
    elif data=='customer_review':
        womens=Product.objects.filter(category="WF").order_by('review').reverse()
    elif data=='below_100':
        womens=Product.objects.filter(category="WF").filter(discounted_price__lt=100).order_by('discounted_price').reverse()
    elif data=='below_200':
        womens=Product.objects.filter(category="WF").filter(discounted_price__lte=200).order_by('discounted_price').reverse()
    elif data=='below_500':
        womens=Product.objects.filter(category="WF").filter(discounted_price__lte=500).order_by('discounted_price').reverse()
    elif data=='below_1000':
        womens=Product.objects.filter(category="WF").filter(discounted_price__lt=1000).order_by('discounted_price').reverse()
    elif data=='below_2000':
        womens=Product.objects.filter(category="WF").filter(discounted_price__lt=2000).order_by('discounted_price').reverse()
    else:
        womens=Product.objects.filter(category="WF").filter(discounted_price__gt=2000).order_by('discounted_price')
    return render(request, 'fashion_womens.html',{'womens':womens,'product_count_in_cart':product_count_in_cart})


def grocery(request,data=None):
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
    g_cat= data=='Snacks_&_Beverages' or data=='Packaged_Food' or data=='Personal_&_Baby_Care' or data=='Household_Care' or data=='Dairy_Products' or data=='Home_&_Kitchen' or data=='Foodgrains' 
    if data==None:
        grocery=Product.objects.filter(category="G").order_by('?').reverse()
    elif g_cat:
        grocery=Product.objects.filter(category="G").filter(type=data)
    elif data=='low_to_high':
        grocery=Product.objects.filter(category="G").order_by('discounted_price')
    elif data=='high_to_low':
        grocery=Product.objects.filter(category="G").order_by('discounted_price').reverse()
    elif data=='customer_rating':
        grocery=Product.objects.filter(category="G").order_by('rating').reverse()
    elif data=='customer_review':
        grocery=Product.objects.filter(category="G").order_by('review').reverse()
    elif data=='below_50':
        grocery=Product.objects.filter(category="G").filter(discounted_price__lt=50).order_by('discounted_price').reverse()
    elif data=='below_100':
        grocery=Product.objects.filter(category="G").filter(discounted_price__lte=100).order_by('discounted_price').reverse()
    elif data=='below_200':
        grocery=Product.objects.filter(category="G").filter(discounted_price__lt=200).order_by('discounted_price').reverse()
    elif data=='below_300':
        grocery=Product.objects.filter(category="G").filter(discounted_price__lt=300).order_by('discounted_price').reverse()
    elif data=='below_500':
        grocery=Product.objects.filter(category="G").filter(discounted_price__lte=500).order_by('discounted_price').reverse()
    else:
        grocery=Product.objects.filter(category="G").filter(discounted_price__gt=500).order_by('discounted_price')
    return render(request, 'grocery.html',{'grocery':grocery,'product_count_in_cart':product_count_in_cart})


def home_appliances(request,data=None):
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
    h_cat= data=='Home_Decor' or data=='Furniture' or data=='Lightings' or data=='Tools'  
    if data==None:
        home=Product.objects.filter(category="H").order_by('?').reverse()
    elif h_cat:
        home=Product.objects.filter(category="H").filter(type=data)
    elif data=='low_to_high':
        home=Product.objects.filter(category="H").order_by('discounted_price')
    elif data=='high_to_low':
        home=Product.objects.filter(category="H").order_by('discounted_price').reverse()
    elif data=='customer_rating':
        home=Product.objects.filter(category="H").order_by('rating').reverse()
    elif data=='customer_review':
        home=Product.objects.filter(category="H").order_by('review').reverse()
    elif data=='below_100':
        home=Product.objects.filter(category="H").filter(discounted_price__lt=100).order_by('discounted_price').reverse()
    elif data=='below_200':
        home=Product.objects.filter(category="H").filter(discounted_price__lte=200).order_by('discounted_price').reverse()
    elif data=='below_500':
        home=Product.objects.filter(category="H").filter(discounted_price__lte=500).order_by('discounted_price').reverse()
    elif data=='below_1000':
        home=Product.objects.filter(category="H").filter(discounted_price__lt=1000).order_by('discounted_price').reverse()
    elif data=='below_2000':
        home=Product.objects.filter(category="H").filter(discounted_price__lt=2000).order_by('discounted_price').reverse()
    else:
        home=Product.objects.filter(category="H").filter(discounted_price__gt=2000).order_by('discounted_price')
    return render(request, 'home_appliance.html',{'home':home,'product_count_in_cart':product_count_in_cart})


def electric_appliances(request,data=None):
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
    e_cat= data=='Audio' or data=='Gaming' or data=='Laptop_Accessories' or data=='Camera_Accessories' or data=='Television' or data=='Air_Conditioner' or data=='Refrigerator' or data=='Washing_Machine' or data=='Others'
    if data==None:
        elect=Product.objects.filter(category="E").order_by('?').reverse()
    elif e_cat:
        elect=Product.objects.filter(category="E").filter(type=data)
    elif data=='low_to_high':
        elect=Product.objects.filter(category="E").order_by('discounted_price')
    elif data=='high_to_low':
        elect=Product.objects.filter(category="E").order_by('discounted_price').reverse()
    elif data=='customer_rating':
        elect=Product.objects.filter(category="E").order_by('rating').reverse()
    elif data=='customer_review':
        elect=Product.objects.filter(category="E").order_by('review').reverse()
    elif data=='below_100':
        elect=Product.objects.filter(category="E").filter(discounted_price__lt=100).order_by('discounted_price').reverse()
    elif data=='below_200':
        elect=Product.objects.filter(category="E").filter(discounted_price__lte=200).order_by('discounted_price').reverse()
    elif data=='below_500':
        elect=Product.objects.filter(category="E").filter(discounted_price__lte=500).order_by('discounted_price').reverse()
    elif data=='below_1000':
        elect=Product.objects.filter(category="E").filter(discounted_price__lt=1000).order_by('discounted_price').reverse()
    elif data=='below_2000':
        elect=Product.objects.filter(category="E").filter(discounted_price__lt=2000).order_by('discounted_price').reverse()
    elif data=='below_5000':
        elect=Product.objects.filter(category="E").filter(discounted_price__lt=5000).order_by('discounted_price').reverse()
    elif data=='below_10000':
        elect=Product.objects.filter(category="E").filter(discounted_price__lt=10000).order_by('discounted_price').reverse()
    elif data=='below_25000':
        elect=Product.objects.filter(category="E").filter(discounted_price__lt=25000).order_by('discounted_price').reverse()
    else:
        elect=Product.objects.filter(category="E").filter(discounted_price__gt=25000).order_by('discounted_price')
    return render(request, 'electric_appliance.html',{'elect':elect,'product_count_in_cart':product_count_in_cart})


def toys(request,data=None):
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
    t_cat= data=='Soft_Toys' or data=='Remote_Control_Toys' or data=='Puzzles' or data=='Board_Games' or data=='Learning_Toys' or data=='Baby_Toys' 
    if data==None:
        toy=Product.objects.filter(category="T").order_by('?').reverse()
    elif t_cat:
        toy=Product.objects.filter(category="T").filter(type=data)
    elif data=='low_to_high':
        toy=Product.objects.filter(category="T").order_by('discounted_price')
    elif data=='high_to_low':
        toy=Product.objects.filter(category="T").order_by('discounted_price').reverse()
    elif data=='customer_rating':
        toy=Product.objects.filter(category="T").order_by('rating').reverse()
    elif data=='customer_review':
        toy=Product.objects.filter(category="T").order_by('review').reverse()
    elif data=='below_100':
        toy=Product.objects.filter(category="T").filter(discounted_price__lt=100).order_by('discounted_price').reverse()
    elif data=='below_200':
        toy=Product.objects.filter(category="T").filter(discounted_price__lte=200).order_by('discounted_price').reverse()
    elif data=='below_500':
        toy=Product.objects.filter(category="T").filter(discounted_price__lte=500).order_by('discounted_price').reverse()
    elif data=='below_1000':
        toy=Product.objects.filter(category="T").filter(discounted_price__lt=1000).order_by('discounted_price').reverse()
    elif data=='below_2000':
        toy=Product.objects.filter(category="T").filter(discounted_price__lt=2000).order_by('discounted_price').reverse()
    else:
        toy=Product.objects.filter(category="T").filter(discounted_price__gt=2000).order_by('discounted_price')
    return render(request, 'toy.html',{'toy':toy,'product_count_in_cart':product_count_in_cart})


def login(request):
    if request.method == 'POST':  
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = auth.authenticate(username = loginusername, password = loginpassword)
        if user is not None:
            auth.login(request,user)
            messages.success(request, f"Successfully Logged In.. Welcome {loginusername}!")
            return redirect("/")
        else:
            messages.error(request,"Invalid Credentials!")
            return redirect("/login")
    return render(request, 'login.html')


def customerregistration(request):
    if request.method == 'POST':
        fname = request.POST.get("fname","default")
        lname = request.POST.get("lname","default")
        username = request.POST.get("username","default")
        email = request.POST.get("email","default")
        pass1 = request.POST.get("pass1","default")
        pass2 = request.POST.get("pass2","default")
        if pass1==pass2:
            if User.objects.filter(username = username).exists():
                messages.error(request,"Username has been already taken!")
                return redirect("/registration")
            elif User.objects.filter(email = email).exists():
                messages.error(request,"Email has been already taken!")
                return redirect("/registration")
            elif len(username)==0:
                messages.error(request, "Your Username cannot be Empty!")
                return redirect('/registration')
            elif len(fname)==0:
                messages.error(request, "Your First Name cannot be Empty!")
                return redirect('/registration')
            elif len(lname)==0:
                messages.error(request, "Your Last Name cannot be Empty!")
                return redirect('/registration')
            elif len(email)==0:
                messages.error(request, "Your Email cannot be Empty!")
                return redirect('/registration')
            elif len(pass1)==0:
                messages.error(request, "Your Password cannot be Empty!")
                return redirect('/registration')
            elif len(username)<3:
                messages.error(request, "Your Username cannot be less than 3 Characters!")
                return redirect('/registration')
            elif len(username)>15:
                messages.error(request, "Your Username must be under 15 Characters!")
                return redirect('/registration')
            elif not username.isalnum():
                messages.error(request, "Special Characters are not allowed!")
                return redirect('/registration')
            elif len(fname)>30:
                messages.error(request, "Your First Name must be under 30 Characters!")
                return redirect('/registration')
            elif len(fname)<2:
                messages.error(request, "Your First Name must be atleast 2 Characters!")
                return redirect('/registration')
            elif len(lname)>30:
                messages.error(request, "Your Last Name must be under 30 Characters!")
                return redirect('/registration')
            elif len(lname)<2:
                messages.error(request, "Your Last Name must be atleast 2 Characters!")
                return redirect('/registration')
            elif len(email)<6:
                messages.error(request, "Your Email must be atleast 6 Characters!")
                return redirect('/registration')
            elif len(email)>100:
                messages.error(request, "Your Email must be under 100 Characters!")
                return redirect('/registration')
            elif len(pass1)<6:
                messages.error(request, "Your Password must be atleast 6 Characters!")
                return redirect('/registration')
            elif len(pass1)>20:
                messages.error(request, "Your Password must be atmost 20 Characters!")
                return redirect('/registration')
            else:
                myuser = User.objects.create_user(username=username, email=email, password=pass1, first_name=fname, last_name=lname)
                messages.success(request, f"Congratulations...{fname} {lname}! Your Account has been Created Sucessfully!")
                myuser.save()
                myuser = auth.authenticate(username = username, password = pass1)
                auth.login(request,myuser)
                return redirect("/")
        else:
            messages.error(request,"Password do not Match!")
            return redirect("/registration")
    return render(request, 'customerregistration.html')


def logout(request):
    try:
        auth.logout(request)
        messages.success(request, f"You have Successfully Logged Out!")
        return redirect('/')
    except:
        return redirect("/")
   
    
def checkout(request):
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
    user=request.user
    add=Customer.objects.filter(user=user) 
    cart=Cart.objects.filter(user=user) 
    products=None
    product_price=0
    total_price=0
    shipping_price=0
    final_price=0
    saving_price=0
    coupon_price=0
    coupon=0
    coupon_code=0
    cp_code=0
    applied_c_price=0
    final_saving_price=0
    if request.user.is_authenticated:
            user=request.user
            products=Cart.objects.filter(user=user)
            coupons2=Coupon.objects.filter(code=coupon)
             
            for p in products:
                total_price=(total_price+(p.product.discounted_price))
                product_price=(product_price+(p.product.selling_price))
            for p in coupons2:
                coupon_price=(p.discount)
            if total_price<=99:
                shipping_price=99
            elif total_price<=199:
                shipping_price=95
            elif total_price<=299:
                shipping_price=89
            elif total_price<=399:
                shipping_price=85
            elif total_price<=499:
                shipping_price=79
            elif total_price==500:
                shipping_price=75
            elif total_price<=799:
                shipping_price=70
            elif total_price<=999:
                shipping_price=55
            elif total_price==1000:
                shipping_price=50
            elif total_price<=1499:
                shipping_price=25
            elif total_price<=1999:
                shipping_price=19
            else:
                shipping_price=0
            if request.method == 'POST':  
                coupon = request.POST['coupon'] 
                cp_code=Coupon.objects.filter(code=coupon)
                if cp_code:
                    for p in Coupon.objects.filter(code=coupon):
                        print(p.discount)
                        print(int((p.discount*10/100)+p.discount))
                        print(total_price)
                        if int((p.discount*10/100)+p.discount)>(total_price):
                            messages.error(request,f"Add item worth Rs.{int((p.discount*10/100)+p.discount)-total_price} in your Cart for Applying Coupon {coupon}")
                        else:
                            coupon_price=(p.discount)
                            coupon_code=(p.code)
                            messages.success(request,f"Coupon {coupon} has been Successfully Appied")
                            
                else:
                    coupon_price=0
                    coupon_code=0
                    messages.error(request,f"Coupon {coupon} has been Invalid")
            final_price=total_price+shipping_price-coupon_price 
            saving_price=product_price-total_price
            final_saving_price=product_price-total_price+coupon_price
    context={'product_count_in_cart':product_count_in_cart,'add':add,'cart':cart,'saving_price':saving_price,'product_price':product_price, 'total_price':total_price,'shipping_price':shipping_price,'final_price':final_price,'coupon_price':coupon_price,'applied_c_price':applied_c_price,'product_count_in_cart':product_count_in_cart,'coupon':coupon,'coupon_code':coupon_code,'cp_code':cp_code,'final_saving_price':final_saving_price}        
    return render(request, 'checkout.html',context)


def payment(request):
    user=request.user
    custid=request.GET.get("custid")
    customer=Customer.objects.get(pk=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product).save()
        c.delete()
    return redirect("/orders")


def search(request):
    if request.user.is_authenticated:
        product_count_in_cart=len(Cart.objects.filter(user=request.user))
    else:
        product_count_in_cart=0
    query = request.GET['query']
    if len(query)==0:
        messages.error(request, "Your Search Result cannot be Empty!")
        return redirect('/')
    elif len(query)<3:
        messages.error(request, "Your Search Query cannot be less than 3 Characters!")
        return redirect('/')
    elif len(query)>30:
        messages.error(request, "Your Search Query cannot be more than 30 Characters!")
        return redirect('/')
    search_prod = Product.objects.filter(title__icontains = query).order_by('discounted_price') or Product.objects.filter(description__icontains = query) or Product.objects.filter(brand__icontains = query) or Product.objects.filter(category__icontains = query) or Product.objects.filter(type__icontains = query)
    
    search_results = {'search_prod': search_prod,'query':query,'product_count_in_cart':product_count_in_cart}
    
    return render(request,"search.html", search_results)

def about(request):
    return render(request,"about.html")

def contact(request):
    if request.method=="POST":
        firstName=request.POST['firstName']
        lastName=request.POST['lastName']
        email=request.POST['email']
        massage =request.POST['massage']
        if len(firstName)==0:
            messages.error(request, "Your First Name cannot be Empty!")
            return redirect('/contact')
        elif len(lastName)==0:
            messages.error(request, "Your Last Name cannot be Empty!")
            return redirect('/contact')
        elif len(email)==0:
            messages.error(request, "Your Email cannot be Empty!")
            return redirect('/contact')
        elif len(massage)==0:
            messages.error(request, "Your Message Box cannot be Empty!")
            return redirect('/contact')
        elif len(firstName)>30:
            messages.error(request, "Your First Name must be under 30 Characters!")
            return redirect('/contact')
        elif len(firstName)<3:
            messages.error(request, "Your First Name must be atleast 3 Characters!")
            return redirect('/contact')
        elif len(lastName)>30:
            messages.error(request, "Your Last Name must be under 30 Characters!")
            return redirect('/contact')
        elif len(lastName)<3:
            messages.error(request, "Your Last Name must be atleast 3 Characters!")
            return redirect('/contact')
        elif len(email)<6:
            messages.error(request, "Your Email must be atleast 6 Characters!")
            return redirect('/contact')
        elif len(email)>50:
            messages.error(request, "Your Email must be under 50 Characters!")
            return redirect('/contact')
        elif len(massage)<4:
            messages.error(request, "Please fill atleast 4 Characters in Message Box")
            return redirect('/contact')
        elif len(massage)>1000:
            messages.error(request, "Your Message must be under 1000 Characters!")
            return redirect('/contact')
        else:
            contact=Contact(firstName=firstName, email=email, lastName=lastName, massage=massage)
            contact.save()
            messages.success(request, "Your Message has been Successfully sent!")
            return redirect('/')      
    return render(request, "contact.html")

def terms(request):
    return render(request,"terms.html")

def privacy(request):
    return render(request,"privacy.html")
    