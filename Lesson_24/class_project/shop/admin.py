from django.contrib import admin

from .models import Category, Product, Sale


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("id", "name")
	search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "price", "category")
	list_filter = ("category",)
	search_fields = ("name",)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
	list_display = ("id", "product", "quantity", "total_price", "created_at")
	list_filter = ("created_at", "product")
