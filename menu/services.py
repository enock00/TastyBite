from django.db.models import Q

from .models import FoodItem


class MenuService:

    @staticmethod
    def get_foods(request):

        queryset = (
            FoodItem.objects
            .filter(is_available=True)
            .select_related("category")
        )

        # ------------------------
        # Category Filter
        # ------------------------

        category = request.GET.get("category")

        if category:

            queryset = queryset.filter(
                category__slug=category
            )

        # ------------------------
        # Search
        # ------------------------

        search = request.GET.get("search")

        if search:

            queryset = queryset.filter(

                Q(name__icontains=search) |
                Q(description__icontains=search)

            )

        # ------------------------
        # Sorting
        # ------------------------

        sort = request.GET.get("sort")

        if sort == "price":

            queryset = queryset.order_by("price")

        elif sort == "-price":

            queryset = queryset.order_by("-price")

        elif sort == "newest":

            queryset = queryset.order_by("-created_at")

        elif sort == "popular":

            queryset = queryset.order_by("-orders")

        return queryset


class FoodService:

    @staticmethod
    def related(food):

        return (
            FoodItem.objects
            .filter(
                category=food.category,
                is_available=True
            )
            .exclude(pk=food.pk)[:4]
        )