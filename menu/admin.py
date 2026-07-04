from django.contrib import admin
from .models import Category, FoodItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
        "price",
        "is_available",
        "is_featured",
    )

    list_filter = (
        "category",
        "is_available",
        "is_featured",
    )

    search_fields = (
        "name",
        "description",
    )

    list_editable = (
        "is_available",
        "is_featured",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }