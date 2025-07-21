from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Cart, Order, CartItem, OrderItem, Rating
from .forms import RegistrationForm, RatingForm, CheckoutForm
from django.contrib import messages


# Create your views here.
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