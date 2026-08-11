from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from store import views


urlpatterns = [

    # Admin
    path(
        "admin/",
        admin.site.urls
    ),

    # Home
    path(
        "",
        views.home,
        name="home"
    ),

    # Authentication
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

    # Cart
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

    # Checkout
    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    # Orders
    path(
        "orders/",
        views.orders,
        name="orders"
    ),
]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )