from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from menu.models import FoodItem

from .cart import Cart


def cart_detail(request):
    cart = Cart(request)

    for item in cart:
        print("ITEM:", item)
        print("KEYS:", item.keys())
        print("FOOD:", item.get("food"))
        print("FOOD ID:", getattr(item.get("food"), "id", None))

    return render(
        request,
        "cart/cart.html",
        {"cart": cart}
    )


def cart_add(request, food_id):

    cart = Cart(request)

    food = get_object_or_404(
        FoodItem,
        id=food_id
    )

    cart.add(food)

    return redirect("cart:cart_detail")


def cart_remove(request, food_id):

    cart = Cart(request)

    food = get_object_or_404(
        FoodItem,
        id=food_id
    )

    cart.remove(food)

    return redirect("cart:cart_detail")

def cart_increase(request, food_id):

    cart = Cart(request)

    food = get_object_or_404(FoodItem, id=food_id)

    cart.add(food)

    return redirect("cart:cart_detail")


def cart_decrease(request, food_id):

    cart = Cart(request)

    food = get_object_or_404(FoodItem, id=food_id)

    food_id = str(food.id)

    if food_id in cart.cart:
        quantity = cart.cart[food_id]["quantity"] - 1
        cart.add(food, quantity=quantity, override_quantity=True)

    return redirect("cart:cart_detail")