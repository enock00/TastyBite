from decimal import Decimal

from menu.models import FoodItem


class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get("cart")

        if cart is None:
            cart = self.session["cart"] = {}

        self.cart = cart

    def add(self, food, quantity=1, override_quantity=False):
        food_id = str(food.id)

        if food_id not in self.cart:
            self.cart[food_id] = {
                "quantity": 0,
                "price": str(food.price),
            }

        if override_quantity:
            self.cart[food_id]["quantity"] = quantity
        else:
            self.cart[food_id]["quantity"] += quantity

        if self.cart[food_id]["quantity"] <= 0:
            del self.cart[food_id]

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, food):
        food_id = str(food.id)

        if food_id in self.cart:
            del self.cart[food_id]
            self.save()

    def __iter__(self):
        food_ids = list(self.cart.keys())

        print("Food IDs:", food_ids)

        foods = FoodItem.objects.filter(id__in=food_ids)

        print("Foods Found:", list(foods.values("id", "name")))

        cart = self.cart.copy()

        for food in foods:
            print("Attaching:", food.id)
            cart[str(food.id)]["food"] = food

        for item in cart.values():
            print("ITEM BEFORE:", item)

            if "food" not in item:
                print("Missing food object!")
                continue

            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]

            yield item

    def __len__(self):
        return sum(
            item["quantity"]
            for item in self.cart.values()
        )

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def clear(self):
        self.session["cart"] = {}
        self.save()