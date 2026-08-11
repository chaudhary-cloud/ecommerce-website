from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages

from .models import Product, Order, OrderItem


# =====================================================
# HOME
# =====================================================

def home(request):

    search = request.GET.get("search")

    products = Product.objects.all()

    if search:
        products = products.filter(
            name__icontains=search
        )

    return render(
        request,
        "home.html",
        {
            "products": products
        }
    )


# =====================================================
# ADD TO CART
# =====================================================

def add_to_cart(request, product_id):

    product = Product.objects.get(id=product_id)

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    current_quantity = cart.get(product_id, 0)

    # Check stock
    if current_quantity >= product.stock:

        messages.error(
            request,
            "Sorry, this product is out of stock."
        )

        return redirect("home")

    if product_id in cart:

        cart[product_id] += 1

    else:

        cart[product_id] = 1

    request.session["cart"] = cart
    request.session.modified = True

    messages.success(
        request,
        f"{product.name} added to your cart!"
    )

    return redirect("home")


# =====================================================
# CART
# =====================================================

def cart(request):

    cart_data = request.session.get(
        "cart",
        {}
    )

    cart_items = []

    total = 0

    for product_id, quantity in list(
        cart_data.items()
    ):

        try:

            product = Product.objects.get(
                id=product_id
            )

        except Product.DoesNotExist:

            del cart_data[product_id]

            continue

        # If cart quantity is greater than available stock
        if quantity > product.stock:

            quantity = product.stock

            if quantity <= 0:

                del cart_data[product_id]

                continue

            cart_data[product_id] = quantity

        item_total = (
            product.price * quantity
        )

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "item_total": item_total,
            }
        )

        total += item_total

    request.session["cart"] = cart_data
    request.session.modified = True

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "total": total,
        }
    )


# =====================================================
# REMOVE FROM CART
# =====================================================

def remove_from_cart(request, product_id):

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(product_id)

    if product_id in cart:

        del cart[product_id]

        request.session["cart"] = cart
        request.session.modified = True

        messages.success(
            request,
            "Product removed from cart."
        )

    return redirect("cart")


# =====================================================
# INCREASE QUANTITY
# =====================================================

def increase_quantity(request, product_id):

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(product_id)

    if product_id in cart:

        try:

            product = Product.objects.get(
                id=product_id
            )

            if cart[product_id] < product.stock:

                cart[product_id] += 1

            else:

                messages.error(
                    request,
                    "No more stock available."
                )

        except Product.DoesNotExist:

            del cart[product_id]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


# =====================================================
# DECREASE QUANTITY
# =====================================================

def decrease_quantity(request, product_id):

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(product_id)

    if product_id in cart:

        if cart[product_id] > 1:

            cart[product_id] -= 1

        else:

            del cart[product_id]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


# =====================================================
# CHECKOUT
# =====================================================

def checkout(request):

    cart_data = request.session.get(
        "cart",
        {}
    )

    cart_items = []

    total = 0

    for product_id, quantity in list(
        cart_data.items()
    ):

        try:

            product = Product.objects.get(
                id=product_id
            )

        except Product.DoesNotExist:

            del cart_data[product_id]

            continue

        # Check stock before checkout
        if quantity > product.stock:

            messages.error(
                request,
                f"Only {product.stock} item(s) of "
                f"{product.name} are available."
            )

            cart_data[product_id] = product.stock

            request.session["cart"] = cart_data
            request.session.modified = True

            return redirect("cart")

        item_total = (
            product.price * quantity
        )

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "item_total": item_total,
            }
        )

        total += item_total

    request.session["cart"] = cart_data
    request.session.modified = True

    # Empty cart
    if not cart_items:

        return redirect("home")

    # =================================================
    # PLACE ORDER
    # =================================================

    if request.method == "POST":

        customer_name = request.POST.get(
            "name"
        )

        email = request.POST.get(
            "email"
        )

        phone = request.POST.get(
            "phone"
        )

        address = request.POST.get(
            "address"
        )

        city = request.POST.get(
            "city"
        )

        pincode = request.POST.get(
            "pincode"
        )

        # Create Order
        order = Order.objects.create(

            customer_name=customer_name,

            email=email,

            phone=phone,

            address=address,

            city=city,

            pincode=pincode,

            total_amount=total,
        )

        # Create Order Items
        for item in cart_items:

            product = item["product"]

            quantity = item["quantity"]

            OrderItem.objects.create(

                order=order,

                product=product,

                quantity=quantity,

                price=product.price,

                item_total=item["item_total"],
            )

            # Decrease product stock
            product.stock -= quantity

            product.save()

        # Empty cart
        request.session["cart"] = {}

        request.session.modified = True

        messages.success(
            request,
            "Your order has been placed successfully!"
        )

        return redirect("orders")

    # Checkout page
    return render(
        request,
        "checkout.html",
        {
            "cart_items": cart_items,
            "total": total,
        }
    )


# =====================================================
# ORDERS
# =====================================================

def orders(request):

    orders = Order.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "orders.html",
        {
            "orders": orders
        }
    )


# =====================================================
# LOGOUT
# =====================================================

def logout_view(request):

    logout(request)

    return redirect("home")