from django.urls import path

from . import views


urlpatterns = [

    # =========================================
    # HOME
    # =========================================

    path(
        "",
        views.home,
        name="home"
    ),


    # =========================================
    # AUTHENTICATION
    # =========================================

    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),


    # =========================================
    # CART
    # =========================================

    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),

    path(
        "cart/increase/<int:product_id>/",
        views.increase_quantity,
        name="increase_quantity"
    ),

    path(
        "cart/decrease/<int:product_id>/",
        views.decrease_quantity,
        name="decrease_quantity"
    ),


    # =========================================
    # CHECKOUT
    # =========================================

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),


    # =========================================
    # ORDERS
    # =========================================

    path(
        "orders/",
        views.orders,
        name="orders"
    ),
]