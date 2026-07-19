from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard_home, name="home"),
    path("orders/", views.orders, name="orders"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
    path("orders/<int:order_id>/status/", views.update_order_status, name="update_order_status"),
    path("menu/", views.menu_list, name="menu"),
    path("menu/add/", views.add_food, name="add_food"),
    path("menu/<int:food_id>/edit/", views.edit_food, name="edit_food"),
    path("menu/<int:food_id>/delete/", views.delete_food, name="delete_food"),
    path("categories/", views.category_list, name="categories"),
    path("categories/add/", views.add_category, name="add_category"),
    path("categories/<int:category_id>/edit/", views.edit_category, name="edit_category"),
    path("categories/<int:category_id>/delete/", views.delete_category, name="delete_category"),
    path("reports/", views.reports, name="reports"),
]