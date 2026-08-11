from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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
# REGISTER
# =====================================================

def register_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )

        if not username or not email or not password:
            messages.error(
                request,
                "Please fill all required fields."
            )

            return render(
                request,
                "register.html"
            )

        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return render(
                request,
                "register.html"
            )

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return render(
                request,
                "register.html"
            )

        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Email is already registered."
            )

            return render(
                request,
                "register.html"
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()

        messages.success(
            request,
            "Account created successfully! Please login."
        )

        return redirect("login")

    return render(
        request,
        "register.html"
    )


# =====================================================
# LOGIN
# =====================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            messages.success(
                request,
                f"Welcome back, {user.username}!"
            )

            return redirect("home")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "login.html"
    )


# =====================================================
# ADD TO CART
# =====================================================

def add_to_cart(request, product_id):

    product = Product.objects.get(
        id=product_id
    )

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(product_id)

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

def remove_from_cart(
    request,
    product_id
):

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

def increase_quantity(
    request,
    product_id
):

    cart = request.session.get(
        "cart",
        {}
    )

    product_id = str(product_id)

    if product_id in cart:

        cart[product_id] += 1

    request.session["cart"] = cart

    request.session.modified = True

    return redirect("cart")


# =====================================================
# DECREASE QUANTITY
# =====================================================

def decrease_quantity(
    request,
    product_id
):

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

    if not cart_items:

        return redirect("home")

    # =============================================
    # PLACE ORDER
    # =============================================

    if request.method == "POST":

        customer_name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        address = request.POST.get(
            "address",
            ""
        ).strip()

        city = request.POST.get(
            "city",
            ""
        ).strip()

        pincode = request.POST.get(
            "pincode",
            ""
        ).strip()

        if not all(
            [
                customer_name,
                email,
                phone,
                address,
                city,
                pincode,
            ]
        ):

            messages.error(
                request,
                "Please fill all customer details."
            )

            return render(
                request,
                "checkout.html",
                {
                    "cart_items": cart_items,
                    "total": total,
                }
            )

        order = Order.objects.create(
            customer_name=customer_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            pincode=pincode,
            total_amount=total,
        )

        for item in cart_items:

            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["product"].price,
                item_total=item["item_total"],
            )

        request.session["cart"] = {}

        request.session.modified = True

        messages.success(
            request,
            "Your order has been placed successfully!"
        )

        return redirect("orders")

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

    if not request.user.is_authenticated:

        messages.info(
            request,
            "Please login to view your orders."
        )

        return redirect("login")

    user_email = request.user.email

    orders_data = Order.objects.filter(
        email=user_email
    ).prefetch_related(
        "items__product"
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "orders.html",
        {
            "orders": orders_data
        }
    )


# =====================================================
# LOGOUT
# =====================================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("home")