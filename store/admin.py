from django.contrib import admin
from .models import Category,Customer,Product,Sales,Newest,Order,OrderItem
from .models import Review
from .models import Wishlist
# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Sales)
admin.site.register(Newest)
admin.site.register(Review)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product','quantity','price']
class OrderAdmin(admin.ModelAdmin) :
    list_display = ['id','customer','total_price','status','date'] 
    list_editable = ['status'] 
    inlines = [OrderItemInline]
    readonly_fields = ['payment_receipt'] 
admin.site.register(Order,OrderAdmin) 
admin.site.register (OrderItem)  
admin.site.register(Wishlist)
