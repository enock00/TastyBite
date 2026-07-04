from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    image = models.ImageField(
        upload_to="categories/"
    )

    description = models.TextField(
        blank=True
    )

    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional Font Awesome icon (e.g. fa-pizza-slice)"
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Remove this method if you don't have a
        URL named 'menu:category'.
        """
        return reverse(
            "menu:category",
            kwargs={"slug": self.slug}
        )


class FoodItem(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="food_items"
    )

    name = models.CharField(
        max_length=200
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to="foods/"
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    original_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        blank=True,
        null=True
    )

    discount_percent = models.PositiveIntegerField(
        default=0
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=5.0
    )

    preparation_time = models.PositiveIntegerField(
        default=30,
        help_text="Preparation time in minutes"
    )

    calories = models.PositiveIntegerField(
        default=0
    )

    stock = models.PositiveIntegerField(
        default=100
    )

    ingredients = models.TextField(
        blank=True
    )

    nutrition = models.TextField(
        blank=True
    )

    is_available = models.BooleanField(
        default=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_popular = models.BooleanField(
        default=False
    )

    is_new = models.BooleanField(
        default=False
    )

    is_spicy = models.BooleanField(
        default=False
    )

    is_vegetarian = models.BooleanField(
        default=False
    )

    is_vegan = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "-is_featured",
            "-is_popular",
            "-created_at",
            "name",
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Automatically generate a slug
        if one hasn't been provided.
        """
        if not self.slug:
            self.slug = slugify(self.name)

        # Automatically calculate discount percentage
        if (
            self.original_price
            and self.original_price > self.price
        ):
            self.discount_percent = round(
                (
                    (self.original_price - self.price)
                    / self.original_price
                ) * 100
            )
        else:
            self.discount_percent = 0

        # Automatically mark unavailable if out of stock
        self.is_available = self.stock > 0

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "menu:food_detail",
            kwargs={"slug": self.slug}
        )

    @property
    def has_discount(self):
        return (
            self.original_price is not None
            and self.original_price > self.price
        )

    @property
    def amount_saved(self):
        if self.has_discount:
            return self.original_price - self.price
        return 0

    @property
    def display_discount(self):
        if self.discount_percent > 0:
            return f"{self.discount_percent}% OFF"
        return ""

    @property
    def formatted_price(self):
        return f"KSh {self.price}"

    @property
    def formatted_original_price(self):
        if self.original_price:
            return f"KSh {self.original_price}"
        return ""