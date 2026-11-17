from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Category,Customer,Order,OrderItem,Newest,Sales
from django.contrib.auth.decorators import login_required
from django.contrib.auth  import login, authenticate, logout
from django.contrib  import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from .forms import SignUpForm
from .models import Review
from .models import Wishlist
from .models import Sales
from .models import Newest
from django.db import models


# Create your views here.
import urllib.parse
def category(request,foo):
     foo = urllib.parse.unquote(foo)
     foo = foo.replace('-',' ').strip()
     try:
          category = Category.objects.get(name__iexact=foo)
          products = Product.objects.filter(category=category)
          context = {"products":products,"category":category}
          return render(request,'category.html',context)
     except Category.DoesNotExist:
          messages.warning(request,"That Category does not exist")
          return redirect('index')


def product(request,pk):
     product = Product.objects.get(id=pk)
     if request.method == 'POST':
          if not request.user.is_authenticated:
               
            messages.warning(request,"Please login first before giving review")
            return redirect('login')
          rating = request.POST.get('rating')
          comment = request.POST.get('comment')
          Review.objects.create(
               product=product,
               user=request.user,
               rating=rating,
               comment=comment
          )
          messages.success(request,"Giving review is successful")
          return redirect('product',pk=pk)
     reviews = product.reviews.all().order_by('-date_added')
     context = {
          "product":product,
          "reviews":reviews,
          "item_type" : "product",
          }
     return render(request, 'product.html',context)


def index(request):
    products = Product.objects.all()
    wishlist_count = 0 
    if request.user.is_authenticated:
         wishlist_count = Wishlist.objects.filter(user=request.user).count()
    else:
         wishlist_count = len(request.session.get('wishlist',[]))     

   
    search_query = request.GET.get('search')
    category_id = request.GET.get('category')
    sort_by = request.GET.get('sort')
    if search_query:
         products = Product.objects.filter(name__icontains=search_query)
    else:  
        products = Product.objects.all()
    
    if category_id:
         products = products.filter(category_id=category_id)
    if sort_by == 'price_low' :
         products = products.order_by('price') 
    elif sort_by == 'price_high'   :
         products = products.order_by('-price') 
    elif sort_by == 'newest'   :
         products = products.order_by('-id')
    categories = Category.objects.all()         

    context = {"products":products,"categories":categories,"search_query":search_query,"current_category":category_id,"current_sort": sort_by,'wishlist_count':wishlist_count}      
    return render(request, 'index.html',context)
     

def about(request):
    products = Product.objects.all()
    return render(request, 'about.html',{
         'products' : products
    })
def sales_list(request):
     products = Sales.objects.all()
     context ={"products":products}
     return render(request,'sales.html', context)
def sales_detail(request,pk):
     product = get_object_or_404(Sales, pk = pk)
     context ={"product":product,"item_type":"sales"}
     return render(request, 'product.html',context)
def newest_items(request):
     products = Newest.objects.all().order_by('-id')[:10]
     context = {'products':products}
     return render(request,'newest_items.html',context)
def newest_detail(request,pk):
     product =   get_object_or_404(Newest, pk = pk)
     context ={"product":product,"item_type":"newest"}
     return render(request, 'product.html',context)
     
def login_user(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in!")
            return redirect("/index/")
        return render(request,"login.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request,user)
            messages.success(request, "Login Successfully")
            return redirect("/index/")
        else:
            messages.error(request, "Invalid credential")
            return redirect("/login/")

def logout_user(request):
   logout(request)
   messages.success(request, "Logout successfully")
   return redirect("/index/")
def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, "You have registered Successfully")
            return redirect('index')
        else:
             messages.warning(request, " There was a problem,Please try again!!")
             return redirect('index')
    else:
            return render(request, 'register.html',{"form":form})
@login_required(login_url='login')  
def checkout(request) :
    return render(request,'checkout.html')  
@login_required(login_url='login') 
def place_order(request):
    if request.method == 'POST':
        address = request.POST.get('address') or ''
        phone = request.POST.get('phone') or ''
        receipt_file = request.FILES.get('payment_receipt')
    try:
        customer=Customer.objects.get(email=request.user.email)
    except Customer.DoesNotExist:
        customer = Customer.objects.create(
        First_name = request.user.username,
        Last_name = '',

        email=request.user.email,
        phone = phone if phone else ''
        )
    cart = request.session.get('cart',{})
    if not cart:
            return redirect('cart_summary')
    grand_total = 0
    product_ids=cart.keys()
    cart_products=Product.objects.filter(id__in=product_ids)
    for product in cart_products:
                 quantity = cart.get(str(product_ids),0)
                 grand_total+= product.price * quantity

    new_order = Order.objects.create(
         customer=customer,address=address,phone=phone,total_price=grand_total,payment_receipt=receipt_file)
    for product in cart_products:
        quantity = cart.get(str(product_ids),0)  
        OrderItem.objects.create(
             order=new_order,
             product=product,
             quantity=quantity,
             price=product.price
             )            
    
        request.session['cart']  = {}
        request.session.modified = True
        return render(request,'order_success.html')
    return redirect('index')
@login_required(login_url='login')
def order_history(request):
    try:
        customer = Customer.objects.get(email=request.user.email)
        orders = Order.objects.filter(customer=customer).order_by('-date')
    except Customer.DoesNotExist:
        orders = []
    return render(request,'order_history.html',{'orders':orders})
@login_required(login_url='login')
def add_to_wish(request,product_id):
     
     try:
          product = Product.objects.get(id=product_id)
          Wishlist.objects.get_or_create(user=request.user,product=product,newest=None,sales=None)
          return redirect(request.META.get('HTTP_REFERER','index')) 
     except Product.DoesNotExist:
          try:
               newest_item = Newest.objects.get(id=product_id)    
               Wishlist.objects.get_or_create(user=request.user,newest=newest_item,product=None,sales=None) 
               return redirect(request.META.get('HTTP_REFERER','index')) 
          except Newest.DoesNotExist:
               try:
                  sales_item =  Sales.objects.get(id=product_id)    
                  Wishlist.objects.get_or_create(user=request.user,sales=sales_item,product=None,newest=None)
                  return redirect(request.META.get('HTTP_REFERER','index')) 
               except Sales.DoesNotExist: 
                    pass
               return redirect(request.META.get('HTTP_REFERER','index')) 
               
    
     
  
@login_required(login_url='login')  
def wishlist_view(request):
     my_wishlist = Wishlist.objects.filter(user=request.user)
     return render(request,'wishlist.html',{'my_wishlist':my_wishlist})
@login_required(login_url='login')
def remove_from_wishlist(request,product_id):
      try:
               wishlist_item = Wishlist.objects.filter(
                    user=request.user
               ).filter(
                    models.Q(product_id=product_id) |
                    models.Q(newest_id=product_id) |
                    models.Q(sales_id=product_id)
               )
               wishlist_item.delete()
      except Exception as e: 
           print("Error removing from wishlist:",e)        
      return redirect(request.META.get('HTTP_REFERER','wishlist_view'))
def contact(request):
    if request.method == 'POST':
         user_name=request.POST.get('name')
         user_phone=request.POST.get('phone')
         user_email=request.POST.get('email')
         user_message=request.POST.get('message')
         messages.objects.create(
              name=user_name,
              phone=user_phone,
              email=user_email,
              message=user_message
         )
         messages.success(request,"We received your messages")
    return render(request,'contact.html')     

     
     
        
    
      


    


