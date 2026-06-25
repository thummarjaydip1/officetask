from django.contrib import admin
from .models import Category, Product, Contact, Cart, CartItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'created_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'price', 'stock', 'status')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_quantity', 'grand_total', 'updated_at')
    readonly_fields = ('total_quantity', 'grand_total', 'created_at', 'updated_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'total_price')
    readonly_fields = ('total_price',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'user', 'created_at')
    search_fields = ('name', 'email', 'subject', 'user__username')
    readonly_fields = ('created_at',)
