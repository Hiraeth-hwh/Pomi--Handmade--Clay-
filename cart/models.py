from django.db import models
from django.contrib.auth.models import User
from store.models import Product,Newest,Sales

   


# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='cart_items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True,related_name='cart_product_items')
    newest = models.ForeignKey(Newest,on_delete=models.CASCADE,null=True,blank=True)
    sales = models.ForeignKey(Sales,on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
     if self.product:
        return f"{self.product.name} {self.quantity}"
     elif self.newest:
        return f"{self.newest.name} {self.quantity}"
     elif self.sales:
        return f"{self.sales.name} {self.quantity}"
     return f"Cart Item{self.id}"
     

