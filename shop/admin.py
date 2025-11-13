from django.contrib import admin
from .models import Category, Product, Rating, Cart, CartItem, Order, OrderItem
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display= ['name', 'slug']
    prepopulated_fields = {'slug' :('name',)}

class RatingInline(admin.TabularInline):
    model = Rating
    extra = 0
    readonly_fields = ['user','rating','comment','created']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug', 'price', 'stock', 'available', 'created', 'updated']
    list_editable = ['available', 'price','stock']
    prepopulated_fields = {'slug' :('name',)}
    inlines= [RatingInline]

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'updated']
    inlines = [CartItemInline]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    exclude = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','first_name', 'last_name', 'email','paid','unpaid','created','status']
    list_filter = ['paid','created','status']
    search_fields = ['first_name','last_name','email']
    inlines = [OrderItemInline]

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user','product','rating', 'created']
    list_filter =['rating','created']