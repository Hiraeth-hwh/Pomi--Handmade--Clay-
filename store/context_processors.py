from .models import Wishlist
from cart.models import CartItem
from django.db.models import Sum

def wishlist_count(request):
    count = 0
    if request.user.is_authenticated:
        count = Wishlist.objects.filter(user=request.user).count()
    else:
        wishlist = request.session.get('wishlist',[])   
        count = len(wishlist) 
    return {'wishlist_count':count}    
def cart_count (request):
    count = 0
    if request.user.is_authenticated:
        count = CartItem.objects.filter(
            user=request.user
        ).aggregate(total=Sum('quantity'))['total'] or 0
        return {'cart_count':count}   
