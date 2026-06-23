import datetime
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .models import *
from .utils import cartData, guestOrder


def register(request):
    if request.user.is_authenticated:
        return redirect("store")

    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user, name=user.username, email=user.email)
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("store")
        else:
            messages.error(request, "Please correct the errors below.")

    data = cartData(request)
    context = {"form": form, "cartItems": data["cartItems"]}
    return render(request, "store/register.html", context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect("store")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get("next")
            return redirect(next_url or "store")
        else:
            messages.error(request, "Invalid email or password.")

    data = cartData(request)
    context = {"cartItems": data["cartItems"]}
    return render(request, "store/login.html", context)


def logoutUser(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("store")


def store(request):
    data = cartData(request)
    cartItems = data["cartItems"]

    products = Product.objects.all()
    categories = Category.objects.all()

    # Search
    query = request.GET.get("q", "")
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Category filter
    category_slug = request.GET.get("category", "")
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Pagination
    page = request.GET.get("page", 1)
    paginator = Paginator(products, 9)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        "products": products,
        "cartItems": cartItems,
        "categories": categories,
        "current_category": category_slug,
        "query": query,
    }
    return render(request, "store/store.html", context)


def productDetail(request, product_id):
    data = cartData(request)
    cartItems = data["cartItems"]

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect("store")

    context = {"product": product, "cartItems": cartItems}
    return render(request, "store/product.html", context)


def cart(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]
    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/cart.html", context)


def checkout(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]
    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/checkout.html", context)


@login_required
def orders(request):
    data = cartData(request)
    cartItems = data["cartItems"]

    customer, _ = Customer.objects.get_or_create(
        user=request.user,
        defaults={"name": request.user.username, "email": request.user.email},
    )
    completed_orders = Order.objects.filter(customer=customer, complete=True).order_by(
        "-date_ordered"
    )

    context = {"orders": completed_orders, "cartItems": cartItems}
    return render(request, "store/orders.html", context)


def updateItem(request):
    try:
        data = json.loads(request.body)
        productId = data.get("productId")
        action = data.get("action")

        if not productId or action not in ("add", "remove"):
            return JsonResponse({"error": "Invalid request"}, status=400)

        if not request.user.is_authenticated:
            return JsonResponse({"error": "User is not authenticated"}, status=401)

        customer, _ = Customer.objects.get_or_create(
            user=request.user,
            defaults={
                "name": request.user.username,
                "email": request.user.email,
            },
        )

        product = Product.objects.get(id=productId)
        order, _ = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(
            order=order, product=product
        )

        if action == "add":
            # Stock enforcement: check if adding would exceed available stock
            new_qty = orderItem.quantity + 1
            if product.stock is not None and new_qty > product.stock:
                return JsonResponse(
                    {
                        "error": f"Only {product.stock} available in stock (you already have {orderItem.quantity} in cart).",
                    },
                    status=400,
                )
            orderItem.quantity = new_qty
        elif action == "remove":
            orderItem.quantity -= 1

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse(
            {
                "success": True,
                "cartItems": order.get_cart_items,
                "cartTotal": order.get_cart_total,
                "stock": product.stock,
            }
        )

    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def processOrder(request):
    try:
        transaction_id = datetime.datetime.now().timestamp()
        data = json.loads(request.body)

        if request.user.is_authenticated:
            customer, _ = Customer.objects.get_or_create(
                user=request.user,
                defaults={
                    "name": request.user.username,
                    "email": request.user.email,
                },
            )
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False
            )
        else:
            customer, order = guestOrder(request, data)

        total = float(data["form"]["total"])
        order.transaction_id = transaction_id

        if abs(total - order.get_cart_total) < 0.01:
            order.complete = True
        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data["shipping"]["address"],
                city=data["shipping"]["city"],
                state=data["shipping"]["state"],
                zipcode=data["shipping"]["zipcode"],
                phone_number=data["shipping"].get("phone_number", ""),
            )

        return JsonResponse({"success": True, "message": "Payment submitted.."})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
