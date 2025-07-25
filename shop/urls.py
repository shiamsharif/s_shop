from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('products/<slug:category_slug>/', views.product_list, name='products_by_category'),
    
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('payment/process/', views.payment_process, name='payment_process'),
    path('payment/success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment/fail/<int:order_id>/', views.payment_fail, name='payment_fail'),
    path('payment/cancel/<int:order_id>/', views.payment_cancel, name='payment_cancel'),
    
    path('profile/', views.profile, name='profile'),
    path('rate/<int:product_id>/', views.rate_product, name='rate_product'),
]
