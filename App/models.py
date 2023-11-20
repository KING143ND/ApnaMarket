from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime

STATE_CHOICES = (
   ("unknown","unknown"),
   ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
   ("Andhra Pradesh","Andhra Pradesh"),
   ("Arunachal Pradesh","Arunachal Pradesh"),
   ("Assam","Assam"),
   ("Bihar","Bihar"),
   ("Chhattisgarh","Chhattisgarh"),
   ("Chandigarh","Chandigarh"),
   ("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),
   ("Daman and Diu","Daman and Diu"),
   ("Delhi","Delhi"),
   ("Goa","Goa"),
   ("Gujarat","Gujarat"),
   ("Haryana","Haryana"),
   ("Himachal Pradesh","Himachal Pradesh"),
   ("Jammu and Kashmir","Jammu and Kashmir"),
   ("Jharkhand","Jharkhand"),
   ("Karnataka","Karnataka"),
   ("Kerala","Kerala"),
   ("Ladakh","Ladakh"),
   ("Lakshadweep","Lakshadweep"),
   ("Madhya Pradesh","Madhya Pradesh"),
   ("Maharashtra","Maharashtra"),
   ("Manipur","Manipur"),
   ("Meghalaya","Meghalaya"),
   ("Mizoram","Mizoram"),
   ("Nagaland","Nagaland"),
   ("Odisha","Odisha"),
   ("Punjab","Punjab"),
   ("Pondicherry","Pondicherry"),
   ("Rajasthan","Rajasthan"),
   ("Sikkim","Sikkim"),
   ("Tamil Nadu","Tamil Nadu"),
   ("Telangana","Telangana"),
   ("Tripura","Tripura"),
   ("Uttar Pradesh","Uttar Pradesh"),
   ("Uttarakhand","Uttarakhand"),
   ("West Bengal","West Bengal"),
)
Gender_choices = (
    ("unknown","unknown"),
    ("Male","Male"),
    ("Female","Female"),
    ("Not Specified","Not Specified"),
)
Address_choices = (
    ("unknown","unknown"),
    ("Home","Home"),
    ("Work","Work")
)
class Customer (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100,null=True)
    phone = models.CharField(null=True, max_length=13)
    locality= models.CharField(max_length=200)
    gender = models.CharField(choices=Gender_choices, max_length=15,default="unknown")
    city= models.CharField(max_length=50)
    zipcode= models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50,default="unknown")
    landmark = models.CharField(max_length=50,null=True)
    age = models.PositiveIntegerField(default=0)
    address = models.CharField(choices=Address_choices, max_length=15,default="unknown")
    
    def __str__(self):
        return str(self.name)


CATEGORY_CHOICES = (
    ('M', 'Mobiles'),
    ('L', 'Laptops'),
    ('MF', 'MensFashion'),
    ('WF', 'WomensFashion'),
    ('G', 'Grocery'),
    ('H','HomeAppliances'),
    ('E', 'Electronics'),
    ('T','Toys'),
    ('Md','Medicine')
)
TYPE_CHOICES = (
    ('Unknown', 'Unknown'),
    ('T-Shirts', 'T-Shirts'),
    ('Shirts', 'Shirts'),
    ('Winter_Wears', 'Winter_Wears'),
    ('Blazers', 'Blazers'),
    ('Suits', 'Suits'),
    ('Jeans','Jeans'),
    ('Trousers', 'Trousers'),
    ('Trackpants','Trackpants'),
    ('Shoes','Shoes'),
    ('Slippers','Slippers'),
    ('Wallets','Wallets'),
    ('Watches','Watches'),
    ('Sunglasses','Sunglasses'),
    ('Belts','Belts'),
    ('Jewellery','Jewellery'),
    ('Sarees','Sarees'),
    ('Tops','Tops'),
    ('Kurtas','Kurtas'),
    ('Purse','Purse'),
    ('Snacks_&_Beverages','Snacks_&_Beverages'),
    ('Packaged_Food','Packaged_Food'),
    ('Personal_&_Baby_Care','Personal_&_Baby_Care'),
    ('Household_Care','Household_Care'),
    ('Dairy_Products','Dairy_Products'),
    ('Home_&_Kitchen','Home_&_Kitchen'),
    ('Foodgrains','Foodgrains'),
    ('Home_Decor','Home_Decor'),
    ('Furniture','Furniture'),
    ('Lightings','Lightings'),
    ('Tools','Tools'),
    ('Audio','Audio'),
    ('Gaming','Gaming'),
    ('Laptop_Accessories','Laptop_Accessories'),
    ('Camera_Accessories','Camera_Accessories'),
    ('Television','Television'),
    ('Air_Conditioner','Air_Conditioner'),
    ('Refrigerator','Refrigerator'),
    ('Washing_Machine','Washing_Machine'),
    ('Others','Others'),
    ('Soft_Toys','Soft_Toys'),
    ('Remote_Control_Toys','Remote_Control_Toys'),
    ('Puzzles','Puzzles'),
    ('Board_Games','Board_Games'),
    ('Learning_Toys','Learning_Toys'),
    ('Baby_Toys','Baby_Toys'),
)
class Product (models.Model):
    title= models.CharField(max_length=300)
    quantity=models.PositiveIntegerField(default=0)
    selling_price = models.PositiveIntegerField()
    discounted_price = models.PositiveIntegerField()
    description = models.TextField()
    rating = models.FloatField()
    review = models.PositiveIntegerField()
    brand= models.CharField(max_length=100)
    category= models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    type= models.CharField(choices=TYPE_CHOICES,max_length=113,default="Unknown")
    product_image = models.ImageField()
    offer_1 = models.CharField(max_length=255,default="Bank Offer 5% Unlimited Cashback on Axis Bank Credit")
    offer_2 = models.CharField(max_length=255,default="Special Price Get extra ₹3000 off (price inclusive of discount)")
    offer_3 = models.CharField(max_length=255,default="No cost EMI ₹1,999/month. Standard EMI also available")
    offer_4 = models.CharField(max_length=255,default="Partner Offer ₹2000 ApnaMarket Gift Card on Every 1000th Transaction with a new Visa Debit/Credit Card")
    
    def __str__(self):
        return str(self.title)
  
    
class Coupon (models.Model):
    code = models.CharField(max_length=50, unique=True, null=False,default="Code" )
    active = models.BooleanField(default=True)
    discount = models.PositiveIntegerField(default=0)
    amount = models.PositiveIntegerField(default=500)

    def __str__(self):
        return self.code
     
    
class Cart (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL , null=True , blank=True)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.user)
    
    
STATUS_CHOICES =(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)
class OrderPlaced (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=20, unique=True, editable=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    def save(self, *args, **kwargs):
        if not self.order_id:
            now = datetime.datetime.now()
            self.order_id = now.strftime("OD%Y%m%dID%H%M%S")

        super().save(*args, **kwargs)
    def __str__(self):
        return str(self.user)
    

class Contact(models.Model):
    firstName= models.CharField(max_length=100)
    lastName= models.CharField(max_length=100)
    email= models.EmailField(max_length=100)
    massage= models.TextField()
    timeStamp=models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.firstName  