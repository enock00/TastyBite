from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Avg
from django.db.models.functions import TruncDate

from .forms import FoodItemForm, CategoryForm
from menu.models import FoodItem, Category
from orders.models import Order, OrderItem
from customers.models import Customer
from django.db.models import Sum, Avg, Count


# =====================================================
# Dashboard Home
# =====================================================

def dashboard_home(request):

    total_orders = Order.objects.count()

    pending_orders = Order.objects.filter(status="pending").count()
    confirmed_orders = Order.objects.filter(status="confirmed").count()
    preparing_orders = Order.objects.filter(status="preparing").count()
    ready_orders = Order.objects.filter(status="ready").count()
    delivered_orders = Order.objects.filter(status="delivered").count()
    cancelled_orders = Order.objects.filter(status="cancelled").count()

    revenue = (
        Order.objects.filter(status="delivered")
        .aggregate(total=Sum("total_price"))["total"] or 0
    )

    menu_items = FoodItem.objects.count()

    available_items = FoodItem.objects.filter(
        is_available=True
    ).count()

    featured_items = FoodItem.objects.filter(
        is_featured=True
    ).count()

    categories = Category.objects.count()

    recent_orders = Order.objects.order_by("-created_at")[:5]

    # Best-selling foods
    best_sellers = (
        FoodItem.objects.annotate(
            total_sold=Sum("order_items__quantity")
        )
        .order_by("-total_sold")[:6]
    )

    context = {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "confirmed_orders": confirmed_orders,
        "preparing_orders": preparing_orders,
        "ready_orders": ready_orders,
        "delivered_orders": delivered_orders,
        "cancelled_orders": cancelled_orders,
        "revenue": revenue,
        "menu_items": menu_items,
        "available_items": available_items,
        "featured_items": featured_items,
        "categories": categories,
        "recent_orders": recent_orders,
        "best_sellers": best_sellers,
    }

    return render(request, "dashboard/dashboard.html", context)


# =====================================================
# Orders
# =====================================================

def orders(request):

    orders = Order.objects.order_by("-created_at")

    return render(
        request,
        "dashboard/orders.html",
        {
            "orders": orders
        }
    )


def update_order_status(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":

        new_status = request.POST.get("status")

        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()

            messages.success(
                request,
                "Order status updated successfully."
            )

    return redirect("dashboard:orders")


def order_detail(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    return render(
        request,
        "dashboard/order_detail.html",
        {
            "order": order
        }
    )


# =====================================================
# Menu Management
# =====================================================

def menu_list(request):

    foods = (
        FoodItem.objects
        .select_related("category")
        .order_by("name")
    )

    return render(
        request,
        "dashboard/menu.html",
        {
            "foods": foods
        }
    )


def add_food(request):

    if request.method == "POST":

        form = FoodItemForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Food added successfully."
            )

            return redirect("dashboard:menu")

    else:

        form = FoodItemForm()

    return render(
        request,
        "dashboard/add_food.html",
        {
            "form": form,
            "title": "Add Food"
        }
    )


def edit_food(request, food_id):

    food = get_object_or_404(
        FoodItem,
        id=food_id
    )

    if request.method == "POST":

        form = FoodItemForm(
            request.POST,
            request.FILES,
            instance=food
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Food updated successfully."
            )

            return redirect("dashboard:menu")

    else:

        form = FoodItemForm(instance=food)

    return render(
        request,
        "dashboard/food_form.html",
        {
            "form": form,
            "title": "Edit Food"
        }
    )


def delete_food(request, food_id):

    food = get_object_or_404(
        FoodItem,
        id=food_id
    )

    if request.method == "POST":

        food.delete()

        messages.success(
            request,
            "Food deleted successfully."
        )

        return redirect("dashboard:menu")

    return render(
        request,
        "dashboard/delete_food.html",
        {
            "food": food
        }
    )


# =====================================================
# Categories
# =====================================================

def category_list(request):

    categories = Category.objects.order_by("name")

    return render(
        request,
        "dashboard/categories.html",
        {
            "categories": categories
        }
    )


def add_category(request):

    if request.method == "POST":

        form = CategoryForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Category added successfully."
            )

            return redirect("dashboard:categories")

    else:

        form = CategoryForm()

    return render(
        request,
        "dashboard/category_form.html",
        {
            "form": form,
            "title": "Add Category",
        },
    )


def edit_category(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id
    )

    if request.method == "POST":

        form = CategoryForm(
            request.POST,
            request.FILES,
            instance=category,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Category updated successfully."
            )

            return redirect("dashboard:categories")

    else:

        form = CategoryForm(
            instance=category
        )

    return render(
        request,
        "dashboard/category_form.html",
        {
            "form": form,
            "title": "Edit Category",
        },
    )


def delete_category(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id,
    )

    if request.method == "POST":

        category.delete()

        messages.success(
            request,
            "Category deleted."
        )

        return redirect("dashboard:categories")

    return render(
        request,
        "dashboard/delete_category.html",
        {
            "category": category
        }
    )


def reports(request):

    delivered_orders = Order.objects.filter(status="delivered")

    # ===============================
    # Summary Statistics
    # ===============================

    total_revenue = (
        delivered_orders.aggregate(
            total=Sum("total_price")
        )["total"] or 0
    )

    average_order = (
        delivered_orders.aggregate(
            avg=Avg("total_price")
        )["avg"] or 0
    )

    total_orders = Order.objects.count()

    total_customers = Customer.objects.count()

    total_foods = FoodItem.objects.count()

    pending_orders = Order.objects.filter(
        status="pending"
    ).count()

    confirmed_orders = Order.objects.filter(
        status="confirmed"
    ).count()

    preparing_orders = Order.objects.filter(
        status="preparing"
    ).count()

    ready_orders = Order.objects.filter(
        status="ready"
    ).count()

    delivered_count = delivered_orders.count()

    cancelled_orders = Order.objects.filter(
        status="cancelled"
    ).count()

    # ===============================
    # Daily Revenue
    # ===============================

    daily_sales = (
        delivered_orders
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(total=Sum("total_price"))
        .order_by("day")
    )

    # ===============================
    # Best Selling Foods
    # ===============================

    best_foods = (
        OrderItem.objects
        .values(
            "food__id",
            "food__name",
            "food__image",
            "food__price",
        )
        .annotate(
            quantity_sold=Sum("quantity"),
            total_orders=Count("order"),
        )
        .order_by("-quantity_sold")[:5]
    )

    # ===============================
    # Category Performance
    # ===============================

    category_sales = (
        OrderItem.objects
        .values(
            "food__category__name",
        )
        .annotate(
            quantity=Sum("quantity"),
        )
        .order_by("-quantity")
    )

    # ===============================
    # Recent Orders
    # ===============================

    recent_orders = (
        Order.objects
        .select_related(
            "customer",
            "delivery_zone",
        )
        .order_by("-created_at")[:5]
    )

    context = {

        "total_revenue": total_revenue,

        "average_order": average_order,

        "total_orders": total_orders,

        "total_customers": total_customers,

        "total_foods": total_foods,

        "pending_orders": pending_orders,

        "confirmed_orders": confirmed_orders,

        "preparing_orders": preparing_orders,

        "ready_orders": ready_orders,

        "delivered_orders": delivered_count,

        "cancelled_orders": cancelled_orders,

        "daily_sales": daily_sales,

        "best_foods": best_foods,

        "category_sales": category_sales,

        "recent_orders": recent_orders,

    }

    return render(
        request,
        "dashboard/reports.html",
        context,
    )