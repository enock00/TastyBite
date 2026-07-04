from django.shortcuts import render
from menu.models import FoodItem


def home(request):
    featured_foods = (
        FoodItem.objects
        .filter(
            is_featured=True,
            is_available=True
        )
        .select_related("category")
        .order_by("-created_at")[:8]
    )

    context = {
        "featured_foods": featured_foods,
    }

    return render(request, "core/home.html", context)
