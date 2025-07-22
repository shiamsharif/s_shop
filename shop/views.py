from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Cart, Order, CartItem, OrderItem, Rating
from .forms import RegistrationForm, RatingForm, CheckoutForm
from django.contrib import messages
from django.db.models import Min, Max, Count, Avg
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# ---------------- Part 1 ----------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop:register')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'shop/login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')    
            return redirect('shop:login')
        else:
            print(form.errors)  # 🔍 ফর্ম ভুল হলে সেটা কনসোলে দেখতে পারবেন
    else:
        form = RegistrationForm()
    return render(request, 'shop/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('shop:login')


# ---------------- Part 2 ----------------

def home(request):
    featured_products = Product.objects.filter(available=True).order_by('-created_at')[:8]
    categories = Category.objects.all()
    
    
    return render(request, 'shop/home.html', {
        'featured_products': featured_products,
        'categories': categories
    })
    
    
def product_detail(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    min_price = products.aggregate(Min('price'))['price__min']
    max_price = products.aggregate(Max('price'))['price__max']
    
    if request.GET.get('min_price'):
        products = products.filter(price__gte=request.GET.get('min_price'))
        
    if request.GET.get('max_price'):
        products = products.filter(price__lte=request.GET.get('max_price'))
        
    if request.GET.get('rating'):
        min_rating = int(request.GET.get('rating'))
        products = products.annotate(avg_rating=Avg('ratings__rating')).filter(avg_rating__gte=min_rating)
        
    if request.GET.get('search'):
        query = request.GET.get('search')
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )
        
    return render(request, 'shop/product_detail.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'min_price': min_price,
        'max_price': max_price,
    })
    

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    user_rating = None
    
    if request.user.is_authenticated: 
        try:
            user_rating = Rating.objects.get(user=request.user, product=product)
        except Rating.DoesNotExist:
            #user_rating = None
            pass
    
    rating_form = RatingForm(instance=user_rating) #or None
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'rating_form': rating_form,
        'user_rating': user_rating,
    })
    
    
@login_required
def cart_detail(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
        
    return render(request, 'shop/cart_detail.html', {'cart': cart})


@login_required
def cart_add(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
    
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        
    messages.success(request, f'{product.name} has been added to your cart.')
    return redirect('shop:cart_detail')


@login_required
def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
    messages.success(request, f'{product.name} has been removed from your cart.')
    return redirect('shop:cart_detail')


@login_required
def cart_update(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    
    quentity = int(request.POST.get('quantity', 1))
    
    if quentity > 0:
        cart_item.quantity = quentity
        cart_item.save()
        messages.success(request, f'Quantity of {product.name} has been updated.')
    else:
        cart_item.quantity = quentity
        cart_item.save()
        messages.error(request, 'Cart update successfully!')

    return redirect('shop:cart_detail')
