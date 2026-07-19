from django.shortcuts import render
from menu.models import FoodItem, Category


def home(request):

    featured_foods = (
        FoodItem.objects
        .filter(is_available=True)
        .select_related("category")
        .order_by("-created_at")[:8]
    )

    categories = Category.objects.all()

    context = {

        "featured_foods": featured_foods,

        "categories": categories,

    }

    return render(
        request,
        "core/home.html",
        context,
    )
