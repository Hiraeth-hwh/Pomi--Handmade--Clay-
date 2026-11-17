from  store.models import Product
from .models import CartItem
from django.db.models import Sum

def cart_counter(request):
    
    total_quantity = 0
    grand_total = 0
    cart_items = CartItem.objects.none()
    if request.user.is_authenticated:
      cart_items = CartItem.objects.filter(user=request.user).select_related('product','newest','sales')
      total_quantity = cart_items.aggregate(
         total=Sum('quantity')
      )['total']or 0 
    
    
    for item in cart_items:
       if item.product_id:
          grand_total += item.product.price * item.quantity
       elif item.newest_id:
          grand_total += item.newest.price * item.quantity
       elif item.sales_id:
          grand_total += item.sales.price * item.quantity   
             
    return {'cart_count': total_quantity, 'grand_total': grand_total}    