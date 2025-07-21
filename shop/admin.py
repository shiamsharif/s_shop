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

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0
    readonly_fields = ('user', 'rating','comment' , 'created')
    #show_facets = admin.ShowFacets.ALWAYS
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available', 'created', 'updated')
    list_filter = ('category', 'available', 'created', 'updated')
    list_editable = ('price', 'stock', 'available')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    ordering = ('-created',)
    inlines = [RatingInline]
    show_facets = admin.ShowFacets.ALWAYS
    

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at',)
    list_filter = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    ordering = ('-created_at',)
    inlines = [CartItemInline]
    show_facets = admin.ShowFacets.ALWAYS