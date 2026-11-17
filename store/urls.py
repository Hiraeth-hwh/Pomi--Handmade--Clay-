from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('about/',views.about,name='about'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name="register"),
    path('product/<int:pk>',views.product,name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('product/<int:pk>/',views.product,name='product'),
    path('sales/',views.sales_list,name='sales_list'),
    path('sales/<int:pk>',views.sales_detail,name='sales'),
    path('newest/',views.newest_items,name='newest_items'),
    path('newest/<int:pk>',views.newest_detail,name='newest'),
    path('checkout/',views.checkout,name='checkout'),
    path('place_order/',views.place_order,name='place_order'),
    path('my-orders/',views.order_history,name='order_history'),
    path('add-to-wishlist/<int:product_id>/',views.add_to_wish,name='add_to_wishlist'),
    path('wishlist/',views.wishlist_view,name='wishlist_view'),
    path('remove_from_wishlist/<int:product_id>',views.remove_from_wishlist,name='remove_from_wishlist'),
    path('contact/',views.contact,name='contact'),

    
]

