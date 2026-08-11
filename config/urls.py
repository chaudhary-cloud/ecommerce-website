from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from store import views


urlpatterns = [

    # =========================
    # ADMIN
    # =========================

    path(
        "admin/",
        admin.site.urls
    ),


    # =========================
    # HOME
    # =========================

    path(
        "",
        views.home,
        name="home"
    ),


    # =========================
    # CART
    # =========================

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


    # =========================
    # CHECKOUT
    # =========================

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),


    # =========================
    # ORDERS
    # =========================

    path(
        "orders/",
        views.orders,
        name="orders"
    ),


    # =========================
    # LOGOUT
    # =========================

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

]


# =========================
# MEDIA FILES
# =========================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )