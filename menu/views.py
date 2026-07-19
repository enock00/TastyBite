from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404, redirect

from .models import FoodItem, Category
from .services import MenuService, FoodService

from cart.cart import Cart


class MenuListView(ListView):
    model = FoodItem
    template_name = "menu/menu.html"
    context_object_name = "foods"

    def get_queryset(self):
        """
        Return the filtered list of available foods.
        """
        return (
            MenuService.get_foods(self.request)
            .select_related("category")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = (
            Category.objects
            .prefetch_related("food_items")
            .filter(food_items__is_available=True)
            .distinct()
        )

        return context


class FoodDetailView(DetailView):
    model = FoodItem
    template_name = "menu/food_detail.html"
    context_object_name = "food"

    def get_queryset(self):
        return (
            FoodItem.objects
            .select_related("category")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["related_foods"] = (
            FoodService.related(self.object)
            .select_related("category")
        )

        return context


class AddToCartView(View):

    def get(self, request, food_id):
        food = get_object_or_404(
            FoodItem,
            id=food_id,
            is_available=True
        )

        cart = Cart(request)
        cart.add(food)

        return redirect("cart:cart_detail")

class CategoryMenuView(ListView):

    model = FoodItem

    template_name = "menu/menu.html"

    context_object_name = "foods"

    def dispatch(self, request, *args, **kwargs):

        self.category = get_object_or_404(
            Category,
            slug=self.kwargs["slug"]
        )

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):

        return (
            FoodItem.objects
            .filter(
                category=self.category,
                is_available=True,
            )
            .select_related("category")
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["category"] = self.category

        context["categories"] = (
            Category.objects
            .prefetch_related("food_items")
            .filter(food_items__is_available=True)
            .distinct()
        )

        return context