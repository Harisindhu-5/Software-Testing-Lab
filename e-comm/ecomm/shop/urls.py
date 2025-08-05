from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('orders/', views.orders_view, name='orders'),
    path('seller/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/add/', views.product_create, name='product_create'),
    path('seller/edit/<int:product_id>/', views.product_edit, name='product_edit'),
    path('checkout/', views.checkout, name='checkout'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.product_list, name='search'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
    path('invoice/<int:order_id>/', views.invoice_view, name='invoice'),
    path('profile/', views.user_profile, name='user_profile'),
] 