

from django.shortcuts import render,redirect,get_object_or_404
from .models import CartItem
from store.models import Product,Newest,Sales
from django.contrib.auth.decorators import login_required


# Create your views here.
def cart_summary(request):
   cart_items = CartItem.objects.filter(user=request.user)
   total_quantity = 0
   grand_total = 0
   quantities = {}

   
   for item in cart_items:
            total_quantity += item.quantity
            if item.product:
                grand_total += item.product.price * item.quantity
                quantities[str(item.product.id)] = item.quantity
            elif  item.newest:
                 grand_total += item.newest.price * item.quantity
                 quantities[str(item.newest.id)] = item.quantity
            elif item.sales:
                 grand_total += item.sales.price * item.quantity
                 quantities[str(item.sales.id)] = item.quantity     
   context = {
            'cart_items':cart_items,
            'total_quantity' : total_quantity,
            'grand_total': grand_total,
            'quantities':quantities,

        } 
          

   return render(request, 'cart_summary.html', context)
   
@login_required (login_url='login')  
def cart_add(request,product_id):
   if not request.user.is_authenticated:
       return redirect('login')
   item_type = request.GET.get('type','product')
   
   if item_type == 'newest':
       item = get_object_or_404(Newest,id=product_id)
       cart_item,created = CartItem.objects.get_or_create(
              user = request.user,
              newest=item,
              defaults={'quantity':1}
          )  
   elif item_type == 'sales' :
       item = get_object_or_404(Sales,id=product_id)
       cart_item,created = CartItem.objects.get_or_create(
              user = request.user,
               sales=item,
              defaults={'quantity':1}
          )  
   else : 
       item = get_object_or_404(Product,id=product_id)  
       cart_item,created = CartItem.objects.get_or_create(
              user = request.user,
              product=item,
              defaults={'quantity':1}
          )  
   
   if not created:
       cart_item.quantity += 1
       cart_item.save()
   return redirect ('cart_summary')
    
    
   
@login_required(login_url='login')  
def cart_update(request,product_id):
       if request.method == 'POST':
           cart_item = get_object_or_404(
               CartItem,
               id=product_id,
               user=request.user

           )
           quantity = int(request.POST.get('product_qty',1))
           if quantity >= 1:
               cart_item.quantity = quantity
               cart_item.save()
       return redirect ('cart_summary')       
@login_required(login_url='login')                    
def cart_delete(request, product_id):
   print("Delete ID:",product_id)
   print("Current User",request.user)
   cart_item = CartItem.objects.filter(
       id=product_id,
       user=request.user
   ).first()
   print ("Found Cart Item:",cart_item)
   if cart_item:
       cart_item.delete()
       print("Cart item deleted successfully")
   else:
       print("Cart item not found")   

       
   
   return redirect('cart_summary')
