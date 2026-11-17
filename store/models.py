from django.db import models
import datetime
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True,null=True,blank=True)
    def __str__(self):
        return self.name
    
class Customer(models.Model) :
    First_name = models.CharField(max_length=50)  
    Last_name = models.CharField(max_length=50)  
    phone = models.CharField(max_length=10) 
    email = models.EmailField(max_length=100) 
    password = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.First_name} {self.Last_name}'
    

class Product(models.Model):
    PRODUCT_TYPE = [
        
        ('art','Art & Craft'),
        
    ]
       
    
    product_type = models.CharField(max_length=200,choices=PRODUCT_TYPE,null=True,blank=True)
    image = models.ImageField(upload_to='product_images',null=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    price = models.IntegerField(null=True)
    description = models.TextField(blank=True,null=True)
    is_sale = models.BooleanField(default=False)
    sale_price = models.IntegerField(null=True)
    
    def __str__(self):
        return f"{self.name} ({self.category})"
class Sales(models.Model):
    PRODUCT_TYPE = [
            
            ('art','Art & Craft'),
            
        ]
    
    product_type = models.CharField(max_length=200,choices=PRODUCT_TYPE,null=True,blank=True)
    image = models.ImageField(upload_to='product_images',null=True)
    name = models.CharField(max_length=200)
    
    price = models.IntegerField(null=True)
    description = models.TextField(blank=True,null=True)
    is_sale = models.BooleanField(default=False)
    sale_price = models.IntegerField(null=True)
    
    def __str__(self):
        return f"{self.name} ({self.image})"
class Newest(models.Model) :
    PRODUCT_TYPE = [
            ('art','Art & Craft'),
    ] 
    product_type = models.CharField(max_length=200,choices=PRODUCT_TYPE,null=True,blank=True) 
    image = models.ImageField(upload_to='product_images',null=True) 
    name = models.CharField(max_length=200)
    price = models.IntegerField(null=True)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        return f"{self.name} ({self.image})"

class ArtDetail(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE,related_name='art_info') 
   
    material = models.CharField(max_length=100) 
    is_handmade = models.BooleanField(default=True) 

class Order(models.Model):
    
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='customer_name')
    
    address = models.CharField(max_length=100,default='',blank=True)
    phone = models.CharField(max_length=10,blank=True,default='')
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    date = models.DateField(default=datetime.date.today)
    status = models.BooleanField(default=False)
    payment_receipt = models.ImageField(upload_to='receipts/',null=True,blank=True)
    def __str__(self):
        return f"Order {self.id} by {self.customer.First_name} {self.customer.Last_name}"
    
class OrderItem(models.Model) :
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00) 
    def __str__(self):
        return f"{self.product.name} (quantity: {self.quantity}) " 

class CartItem(models.Model)  :
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True) 
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='store_cart_items')
    quantity = models.IntegerField(default=1)  
    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
class Review(models.Model) :
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews') 
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    rating = models.IntegerField(default=5)
    comment = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
       
        return f"{self.user.username} - {self.product.name} ({self.rating} Stars)"
class Wishlist(models.Model) :
    user = models.ForeignKey(User,on_delete=models.CASCADE) 
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True) 
    newest = models.ForeignKey(Newest,on_delete=models.CASCADE,null=True,blank=True)
    sales = models.ForeignKey(Sales,on_delete=models.CASCADE,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True) 
    class Meta:
        unique_together =('user','product')
    def __str__(self) :
        return f"{self.user.username} - {self.product.name}"   
class Contact(models.Model)  :
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)
    email=models.EmailField(max_length=100)
    messages=models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} -{self.email}"
   
    