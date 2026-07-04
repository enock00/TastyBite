from django.urls import path
from . import views

app_name = "menu"

urlpatterns = [
    path("", views.MenuListView.as_view(), name="menu"),
    path("cart/add/<int:food_id>/", views.AddToCartView.as_view(), name="add_to_cart"),
    path("<slug:slug>/", views.FoodDetailView.as_view(), name="food_detail"),
]