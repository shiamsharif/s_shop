from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Cart, Order, CartItem, OrderItem, Rating
from .forms import RegistrationForm, RatingForm, CheckoutForm
from django.contrib import messages
from django.db.models import Min, Max, Count, Avg
form django.db.models import Q


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