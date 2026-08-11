from django.contrib import admin

from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "price",
        "stock",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    list_filter = (
        "stock",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "customer_name",
        "email",
        "phone",
        "total_amount",
        "created_at",
    )

    search_fields = (
        "customer_name",
        "email",
        "phone",
    )

    list_filter = (
        "created_at",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product",
        "quantity",
        "price",
        "item_total",
    )

    search_fields = (
        "order__customer_name",
        "product__name",
    )