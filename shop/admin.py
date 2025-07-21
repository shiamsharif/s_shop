from django.contrib import admin
from .models import Category, Product, Rating, Cart, Order, CartItem, OrderItem

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('name',)
    show_facets = admin.ShowFacets.ALWAYS
