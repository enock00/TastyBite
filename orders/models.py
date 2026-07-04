from django.db import models
from customers.models import Customer
from menu.models import FoodItem


class DeliveryZone(models.Model):
    name = models.CharField(max_length=100)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.name} (KSh {self.delivery_fee})"


class Order(models.Model):

    customer = models.ForeignKey(
    Customer,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="orders"
)

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("preparing", "Preparing"),
        ("ready", "Ready"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    delivery_zone = models.ForeignKey(
    DeliveryZone,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    food = models.ForeignKey(
    FoodItem,
    on_delete=models.CASCADE,
    related_name="order_items",
)

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.food.name} ({self.quantity})"

