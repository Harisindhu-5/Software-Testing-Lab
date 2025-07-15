from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Product, Cart, CartItem, Wishlist, WishlistItem, Order, OrderItem, Shop, User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth import get_user_model
from django.forms import ModelForm

# Create your views here.

# Product listing and sorting
def product_list(request):
    sort = request.GET.get('sort', 'name')
    if sort == 'price':
        products = Product.objects.all().order_by('price')
    else:
        products = Product.objects.all().order_by('name')
    return render(request, 'shop/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        if 'add_to_cart' in request.POST:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                item.quantity += 1
                item.save()
            messages.success(request, 'Added to cart!')
        elif 'add_to_wishlist' in request.POST:
            wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
            WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
            messages.success(request, 'Added to wishlist!')
    return render(request, 'shop/product_detail.html', {'product': product})

# Cart
@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product')
    total_price = sum(item.product.price * item.quantity for item in items)
    if request.method == 'POST':
        for item in items:
            if f'remove_{item.id}' in request.POST:
                item.delete()
            else:
                qty = request.POST.get(f'quantity_{item.id}')
                if qty:
                    item.quantity = int(qty)
                    item.save()
        return redirect('cart')
    return render(request, 'shop/cart.html', {'cart': cart, 'total_price': total_price})

# Wishlist
@login_required
def wishlist_view(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    items = wishlist.items.select_related('product')
    if request.method == 'POST':
        for item in items:
            if f'remove_{item.id}' in request.POST:
                item.delete()
            elif f'add_to_cart_{item.id}' in request.POST:
                cart, _ = Cart.objects.get_or_create(user=request.user)
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=item.product)
                if not created:
                    cart_item.quantity += 1
                    cart_item.save()
                item.delete()
        return redirect('wishlist')
    return render(request, 'shop/wishlist.html', {'wishlist': wishlist})

# Orders
@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'shop/orders.html', {'orders': orders})

# Seller dashboard
@login_required
def seller_dashboard(request):
    if request.user.role != 'seller':
        return redirect('product_list')
    products = Product.objects.filter(seller=request.user)
    return render(request, 'shop/seller_dashboard.html', {'products': products})

# Login, Signup, Logout
def signup_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'seller':
            return redirect('seller_dashboard')
        return redirect('product_list')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            with transaction.atomic():
                user = User.objects.create_user(username=username, email=email, password=password, role=role)
                if role == 'seller':
                    Shop.objects.create(name=f"{username}'s Shop", owner=user)
                login(request, user)
                if role == 'seller':
                    return redirect('seller_dashboard')
                else:
                    return redirect('product_list')
    return render(request, 'shop/signup.html')

def login_view(request):
    if request.user.is_authenticated:
        if request.user.role == 'seller':
            return redirect('seller_dashboard')
        return redirect('product_list')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'seller':
                return redirect('seller_dashboard')
            else:
                return redirect('product_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'shop/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']

@login_required
def product_create(request):
    if request.user.role != 'seller':
        return redirect('product_list')
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.shop = request.user.shop
            product.save()
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'shop/product_form.html', {'form': form, 'action': 'Add'})

@login_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_form.html', {'form': form, 'action': 'Edit'})

from django import forms
class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=255, widget=forms.Textarea(attrs={'rows': 2}))

@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product')
    if not items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            order = Order.objects.create(user=request.user, address=address)
            for item in items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            items.delete()
            messages.success(request, 'Order placed successfully!')
            return redirect('orders')
    else:
        form = CheckoutForm()
    total_price = sum(item.product.price * item.quantity for item in items)
    return render(request, 'shop/checkout.html', {'form': form, 'items': items, 'total_price': total_price})
