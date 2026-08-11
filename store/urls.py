from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path("", views.home, name="home"),

    # ADD TO CART
    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    # CART
    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    # REMOVE FROM CART
    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    # INCREASE QUANTITY
    path(
        "cart/increase/<int:product_id>/",
        views.increase_quantity,
        name="increase_quantity"
    ),

    # DECREASE QUANTITY
    path(
        "cart/decrease/<int:product_id>/",
        views.decrease_quantity,
        name="decrease_quantity"
    ),

    # ORDERS
    path(
        "orders/",
        views.orders,
        name="orders"
    ),

    # LOGOUT
    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),


    path(
    "checkout/",
    views.checkout,
    name="checkout"
),
]