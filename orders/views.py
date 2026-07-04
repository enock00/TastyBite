from decimal import Decimal

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from cart.cart import Cart
from customers.models import Customer

from .forms import CheckoutForm
from .models import DeliveryZone, Order, OrderItem


def checkout(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect("cart:cart_detail")

    form = CheckoutForm(request.POST or None)

    delivery_fee = Decimal("0.00")

    if request.method == "POST":

        if form.is_valid():

            zone = form.cleaned_data.get("delivery_zone")

            if zone:
                delivery_fee = zone.delivery_fee

            grand_total = cart.get_total_price() + delivery_fee

            # Split customer name into first and last names
            full_name = form.cleaned_data["customer_name"].strip()
            name_parts = full_name.split(maxsplit=1)

            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""

            # Find or create customer
            customer, created = Customer.objects.get_or_create(
                phone=form.cleaned_data["phone"],
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": form.cleaned_data["email"],
                    "address": form.cleaned_data["address"],
                },
            )

            # Update customer details
            customer.first_name = first_name
            customer.last_name = last_name
            customer.email = form.cleaned_data["email"]
            customer.address = form.cleaned_data["address"]
            customer.save()

            # Create order
            order = form.save(commit=False)
            order.customer = customer
            order.total_price = grand_total
            order.save()

            # Save ordered items
            for item in cart:

                OrderItem.objects.create(
                    order=order,
                    food=item["food"],
                    price=item["price"],
                    quantity=item["quantity"],
                )

            # Clear cart
            cart.clear()

            return redirect(
                "orders:order_success",
                order_id=order.id,
            )

    grand_total = cart.get_total_price() + delivery_fee

    return render(
        request,
        "orders/checkout.html",
        {
            "form": form,
            "cart": cart,
            "delivery_fee": delivery_fee,
            "grand_total": grand_total,
        },
    )


def order_success(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    return render(
        request,
        "orders/order_success.html",
        {
            "order": order,
        },
    )


def get_delivery_fee(request, zone_id):

    zone = get_object_or_404(DeliveryZone, id=zone_id)

    return JsonResponse(
        {
            "fee": float(zone.delivery_fee),
        }
    )